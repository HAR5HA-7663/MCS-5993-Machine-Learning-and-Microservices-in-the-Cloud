#!/bin/bash

# Enhanced Car Dealership API Seeder
# This script seeds data via your enhanced backend API

set -e

echo "🌱 Car Dealership API Seeder"
echo "=========================="

# Get backend IP
echo "🔍 Finding your backend service..."

# Get backend service task ARN
BACKEND_TASK_ARN=$(aws ecs list-tasks \
  --cluster vroomm-cluster-99 \
  --service-name vroomm-backend-task-service-ebkia29y \
  --region us-east-2 \
  --query 'taskArns[0]' \
  --output text 2>/dev/null)

if [ "$BACKEND_TASK_ARN" = "None" ] || [ -z "$BACKEND_TASK_ARN" ]; then
  echo "❌ Backend service not found or not running"
  echo "Please make sure your backend service is deployed and running"
  exit 1
fi

# Get backend IP
BACKEND_IP=$(aws ecs describe-tasks \
  --cluster vroomm-cluster-99 \
  --tasks $BACKEND_TASK_ARN \
  --region us-east-2 \
  --query 'tasks[0].attachments[0].details[?name==`publicIPv4Address`].value' \
  --output text 2>/dev/null)

if [ -z "$BACKEND_IP" ] || [ "$BACKEND_IP" = "None" ]; then
  echo "❌ Could not get backend IP address"
  exit 1
fi

echo "✅ Found backend at: http://$BACKEND_IP:5000"

# Test API connectivity
echo "🔗 Testing API connection..."
if ! curl -s --max-time 10 "http://$BACKEND_IP:5000/health" > /dev/null; then
  echo "❌ Cannot connect to backend API"
  echo "Please ensure your backend service is healthy"
  exit 1
fi

echo "✅ API is responsive"

# Ask for confirmation
echo ""
read -p "🤔 How many cars would you like to add? (default: 20): " num_cars
num_cars=${num_cars:-20}

if ! [[ "$num_cars" =~ ^[0-9]+$ ]] || [ "$num_cars" -le 0 ]; then
  echo "❌ Invalid number. Using default: 20"
  num_cars=20
fi

if [ "$num_cars" -gt 100 ]; then
  echo "⚠️  Adding $num_cars cars will take a while..."
  read -p "Continue? (y/N): " confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "🚫 Cancelled"
    exit 0
  fi
fi

echo "📥 Adding $num_cars cars via API..."

# Sample car data arrays
brands=("Tesla" "Toyota" "Honda" "BMW" "Mercedes" "Ford" "Chevrolet" "Audi" "Lexus" "Nissan" "Hyundai" "Kia" "Mazda" "Subaru" "Volkswagen")

# Brand-specific models
declare -A brand_models
brand_models["Tesla"]="Model 3,Model S,Model X,Model Y"
brand_models["Toyota"]="Camry,Corolla,RAV4,Highlander,Prius,Tacoma"
brand_models["Honda"]="Civic,Accord,CR-V,Pilot,Fit,Ridgeline"
brand_models["BMW"]="3 Series,5 Series,X3,X5,X1,7 Series"
brand_models["Mercedes"]="C-Class,E-Class,GLC,GLE,A-Class,S-Class"
brand_models["Ford"]="F-150,Mustang,Explorer,Focus,Edge,Escape"
brand_models["Chevrolet"]="Malibu,Impala,Equinox,Tahoe,Silverado,Camaro"
brand_models["Audi"]="A4,Q5,A6,Q7,A3,e-tron"
brand_models["Lexus"]="ES,RX,NX,GX,LS,LC"
brand_models["Nissan"]="Altima,Sentra,Rogue,Pathfinder,Maxima,Frontier"
brand_models["Hyundai"]="Elantra,Sonata,Tucson,Santa Fe,Accent,Venue"
brand_models["Kia"]="Sorento,Sportage,Optima,Soul,Forte,Stinger"
brand_models["Mazda"]="CX-5,Mazda3,CX-9,MX-5 Miata,CX-30"
brand_models["Subaru"]="Outback,Forester,Impreza,Crosstrek,Legacy"
brand_models["Volkswagen"]="Jetta,Passat,Tiguan,Golf,Atlas"

# Function to generate random VIN
generate_vin() {
  echo $(cat /dev/urandom | tr -dc 'A-Z0-9' | fold -w 17 | head -n 1)
}

# Function to get random element from array
get_random() {
  local arr=("$@")
  local rand_index=$((RANDOM % ${#arr[@]}))
  echo "${arr[$rand_index]}"
}

# Function to add a single car
add_car() {
  local brand="$1"
  local model="$2" 
  local year="$3"
  local mileage="$4"
  local price="$5"
  local vin="$6"
  
  local json_data="{
    \"vin\": \"$vin\",
    \"year\": $year,
    \"brand\": \"$brand\",
    \"model\": \"$model\", 
    \"mileage\": $mileage,
    \"price\": $price
  }"
  
  local response=$(curl -s -X POST "http://$BACKEND_IP:5000/cars" \
    -H "Content-Type: application/json" \
    -d "$json_data")
  
  if echo "$response" | grep -q "successfully"; then
    echo "  ✅ Added: $brand $model ($year) - \$$price"
    return 0
  else
    echo "  ❌ Failed: $brand $model - $(echo "$response" | jq -r '.error // "Unknown error"' 2>/dev/null || echo "API Error")"
    return 1
  fi
}

# Add cars
added_count=0
failed_count=0

echo ""
for ((i=1; i<=num_cars; i++)); do
  # Generate random car data
  brand=$(get_random "${brands[@]}")
  
  # Get models for this brand
  IFS=',' read -ra models <<< "${brand_models[$brand]}"
  model=$(get_random "${models[@]}")
  
  # Generate other attributes
  year=$((2015 + RANDOM % 10))  # 2015-2024
  mileage=$((5000 + RANDOM % 100000))  # 5k-105k miles
  
  # Generate realistic price based on brand and year
  case $brand in
    "Tesla"|"BMW"|"Mercedes"|"Audi"|"Lexus")
      base_price=$((40000 + RANDOM % 60000))  # 40k-100k
      ;;
    "Toyota"|"Honda"|"Nissan")
      base_price=$((20000 + RANDOM % 35000))  # 20k-55k
      ;;
    *)
      base_price=$((18000 + RANDOM % 40000))  # 18k-58k
      ;;
  esac
  
  # Apply depreciation
  age=$((2024 - year))
  depreciated_price=$((base_price - (age * 3000)))
  price=$((depreciated_price > 8000 ? depreciated_price : 8000))
  
  vin=$(generate_vin)
  
  echo "[$i/$num_cars] Adding car..."
  if add_car "$brand" "$model" "$year" "$mileage" "$price" "$vin"; then
    ((added_count++))
  else
    ((failed_count++))
  fi
  
  # Small delay to avoid overwhelming the API
  sleep 0.5
done

echo ""
echo "🎉 Seeding Complete!"
echo "==================="
echo "✅ Successfully added: $added_count cars"
if [ $failed_count -gt 0 ]; then
  echo "❌ Failed to add: $failed_count cars"
fi

# Show final statistics
echo ""
echo "📊 Getting updated statistics..."
stats_response=$(curl -s "http://$BACKEND_IP:5000/stats")

if [ $? -eq 0 ] && echo "$stats_response" | jq . >/dev/null 2>&1; then
  total_cars=$(echo "$stats_response" | jq -r '.total_cars // "N/A"')
  avg_price=$(echo "$stats_response" | jq -r '.average_price // "N/A"')
  
  echo "📈 Database Statistics:"
  echo "  Total Cars: $total_cars"
  echo "  Average Price: \$$(printf "%.0f" "$avg_price" 2>/dev/null || echo "N/A")"
else
  echo "⚠️  Could not retrieve statistics"
fi

echo ""
echo "🔗 Test your enhanced features:"
echo "  🌐 Frontend: Find your frontend IP in ECS"
echo "  📊 Stats API: http://$BACKEND_IP:5000/stats"
echo "  🔍 Search API: http://$BACKEND_IP:5000/search?q=Tesla"
echo "  💚 Health Check: http://$BACKEND_IP:5000/health"

echo ""
echo "✨ Happy car dealing! ✨"