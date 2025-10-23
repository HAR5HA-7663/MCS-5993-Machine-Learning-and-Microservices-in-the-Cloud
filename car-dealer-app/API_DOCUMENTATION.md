# Vroomm Vrommmm Car Dealership API Documentation

## Overview

This is the backend API for the Vroomm Vrommmm Car Dealership management system. It provides RESTful endpoints for managing car inventory, searching, and analytics.

## Base URL

- Local: `http://localhost:5000`
- Production: `http://your-backend-ip:5000`

## Endpoints

### 1. Get All Cars (Paginated with Sorting)

**GET** `/cars`

**Query Parameters:**

- `page` (int, optional): Page number (default: 1)
- `sort_by` (string, optional): Sort field - year, brand, model, price, mileage, added_at (default: year)
- `sort_order` (string, optional): ASC or DESC (default: DESC)

**Example:**

```
GET /cars?page=1&sort_by=price&sort_order=DESC
```

**Response:**

```json
{
  "page": 1,
  "per_page": 10,
  "total": 50,
  "sort_by": "price",
  "sort_order": "DESC",
  "cars": [
    {
      "vin": "ABC123DEF456GHI78",
      "year": 2024,
      "brand": "Tesla",
      "model": "Model S",
      "mileage": 5000,
      "price": 89999,
      "added_at": "2025-10-09T22:47:08.343937"
    }
  ]
}
```

### 2. Add New Car

**POST** `/cars`

**Request Body:**

```json
{
  "vin": "ABC123DEF456GHI78",
  "year": 2024,
  "brand": "Tesla",
  "model": "Model S",
  "mileage": 5000,
  "price": 89999
}
```

**Response (Success):**

```json
{
  "message": "Car added successfully",
  "vin": "ABC123DEF456GHI78"
}
```

**Response (Error - Duplicate VIN):**

```json
{
  "error": "Car with this VIN already exists"
}
```

### 3. Delete Multiple Cars

**DELETE** `/cars`

**Request Body:**

```json
{
  "vins": ["VIN1", "VIN2", "VIN3"]
}
```

**Response:**

```json
{
  "message": "Successfully deleted 3 car(s)",
  "count": 3
}
```

### 4. Get Car by VIN

**GET** `/cars/{vin}`

**Example:**

```
GET /cars/ABC123DEF456GHI78
```

**Response:**

```json
{
  "vin": "ABC123DEF456GHI78",
  "year": 2024,
  "brand": "Tesla",
  "model": "Model S",
  "mileage": 5000,
  "price": 89999,
  "added_at": "2025-10-09T22:47:08.343937"
}
```

### 5. Update Car

**PUT** `/cars/{vin}`

**Request Body:**

```json
{
  "year": 2023,
  "brand": "Tesla",
  "model": "Model S",
  "mileage": 15000,
  "price": 79999
}
```

**Response:**

```json
{
  "message": "Car updated successfully",
  "vin": "ABC123DEF456GHI78"
}
```

### 6. Search Cars

**GET** `/search`

**Query Parameters:**

- `q` (string, required): Search query (searches brand, model, VIN, year)
- `page` (int, optional): Page number (default: 1)

**Example:**

```
GET /search?q=Tesla&page=1
```

**Response:**

```json
{
  "query": "Tesla",
  "page": 1,
  "per_page": 10,
  "total": 4,
  "cars": [
    {
      "vin": "ABC123DEF456GHI78",
      "year": 2024,
      "brand": "Tesla",
      "model": "Model S",
      "mileage": 5000,
      "price": 89999,
      "added_at": "2025-10-09T22:47:08.343937"
    }
  ]
}
```

### 7. Get Statistics

**GET** `/stats`

**Response:**

```json
{
  "total_cars": 50,
  "average_price": 45678.9,
  "average_mileage": 65432,
  "most_expensive": {
    "brand": "Tesla",
    "model": "Model S",
    "price": 89999
  },
  "brands": [
    {
      "brand": "Toyota",
      "count": 8
    },
    {
      "brand": "Honda",
      "count": 6
    }
  ],
  "age_groups": [
    {
      "group": "New (2020+)",
      "count": 25
    },
    {
      "group": "Recent (2015-2019)",
      "count": 15
    },
    {
      "group": "Older (2010-2014)",
      "count": 8
    },
    {
      "group": "Classic (Pre-2010)",
      "count": 2
    }
  ]
}
```

### 8. Health Check

**GET** `/health`

**Response (Healthy):**

```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2025-10-09T22:47:08.343937"
}
```

**Response (Unhealthy):**

```json
{
  "status": "error",
  "database": "disconnected",
  "error": "Connection error details"
}
```

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200` - OK (Success)
- `201` - Created (Successfully added new resource)
- `400` - Bad Request (Invalid input/parameters)
- `404` - Not Found (Resource doesn't exist)
- `409` - Conflict (Duplicate resource, e.g., VIN already exists)
- `500` - Internal Server Error (Database or server error)

## Features

### 🔍 Advanced Search

- Search across VIN, brand, model, and year
- Case-insensitive partial matching
- Paginated results

### 📊 Real-time Statistics

- Total car count
- Average price and mileage
- Most expensive car information
- Brand distribution
- Age group analysis

### 🎯 Flexible Sorting

- Sort by any column (year, brand, model, price, mileage, date added)
- Ascending or descending order
- Maintains sort preferences across pagination

### 🗑️ Bulk Operations

- Delete multiple cars at once
- Batch operations with transaction safety

### 💾 Data Management

- Automatic timestamp tracking
- VIN uniqueness enforcement
- Data validation and error handling

## Database Schema

### Cars Table

```sql
CREATE TABLE cars (
    vin VARCHAR(20) PRIMARY KEY,
    year INT,
    brand TEXT,
    model TEXT,
    mileage INT,
    price INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
  - Format: `postgresql://username:password@host:port/database`
  - Default: `dbname=cardb user=caruser password=carpass host=db`

## Example Usage with curl

### Get cars:

```bash
curl "http://localhost:5000/cars?page=1&sort_by=price&sort_order=DESC"
```

### Add a car:

```bash
curl -X POST "http://localhost:5000/cars" \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "NEW123VIN456TEST",
    "year": 2024,
    "brand": "Tesla",
    "model": "Cybertruck",
    "mileage": 100,
    "price": 99999
  }'
```

### Search cars:

```bash
curl "http://localhost:5000/search?q=Tesla&page=1"
```

### Get statistics:

```bash
curl "http://localhost:5000/stats"
```
