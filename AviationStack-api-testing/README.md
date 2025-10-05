# AviationStack API Testing Interface

Interactive Swagger UI for testing all AviationStack API endpoints with your own access key.

## 📦 What's Included

This project provides **two ways** to test the AviationStack API:

1. **Option 1**: Direct Swagger UI (using Docker) - Test API endpoints directly
2. **Option 2**: FastAPI Proxy - Run a Python-based proxy server with Swagger UI

## 🚀 Quick Start

### Option 1: Swagger UI with Docker (Recommended for Quick Testing)

This runs Swagger UI directly pointing to the AviationStack API.

#### Prerequisites

- Docker installed on your machine

#### Steps

1. **Run with Docker:**

   ```bash
   docker run -p 8080:8080 -e SWAGGER_JSON=/foo/aviationstack.yaml -v ${PWD}:/foo swaggerapi/swagger-ui
   ```

   Or use Docker Compose:

   ```bash
   docker-compose up swagger-ui
   ```

2. **Open Swagger UI:**

   - Navigate to: http://localhost:8080

3. **Test the API:**
   - Expand any endpoint (e.g., `/flights`)
   - Click "Try it out"
   - Enter your AviationStack `access_key`
   - Add optional parameters (e.g., `dep_iata=JFK`)
   - Click "Execute"
   - View the live response from AviationStack

---

### Option 2: FastAPI Proxy (Recommended for Development)

This runs a Python FastAPI server that proxies requests to AviationStack and provides Swagger UI.

#### Prerequisites

- Python 3.8+ installed
- OR Docker installed

#### Method A: Run Locally with Python

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

   Or run directly:

   ```bash
   python main.py
   ```

3. **Open Swagger UI:**

   - Navigate to: http://localhost:8000/docs

4. **Test the API:**
   - Same process as Option 1
   - All requests are proxied through your local FastAPI server

#### Method B: Run with Docker

1. **Build and run:**

   ```bash
   docker-compose up fastapi-proxy
   ```

   Or build manually:

   ```bash
   docker build -t aviationstack-fastapi .
   docker run -p 8000:8000 aviationstack-fastapi
   ```

2. **Open Swagger UI:**
   - Navigate to: http://localhost:8000/docs

---

## 📋 Available Endpoints

All AviationStack API endpoints are included:

| Endpoint          | Description                             |
| ----------------- | --------------------------------------- |
| `/flights`        | Get real-time or historical flight data |
| `/routes`         | Get airline route information           |
| `/airports`       | Get airport details and search          |
| `/airlines`       | Get airline information                 |
| `/airplanes`      | Get specific aircraft details           |
| `/aircraft_types` | Get aircraft type information           |
| `/taxes`          | Get aviation tax data                   |
| `/cities`         | Get city data with IATA codes           |
| `/countries`      | Get country information                 |
| `/timetable`      | Get flight timetables for airports      |
| `/flightsfuture`  | Get future flight schedules             |

## 🔑 Getting Your API Key

If you don't have an AviationStack API key:

1. Visit: https://aviationstack.com/
2. Sign up for a free account
3. Get your API access key from the dashboard
4. Use it in the `access_key` parameter

## 💡 Example Queries

### Get flights from JFK airport:

- Endpoint: `/flights`
- Parameters:
  - `access_key`: YOUR_API_KEY
  - `dep_iata`: JFK

### Search for airports in New York:

- Endpoint: `/airports`
- Parameters:
  - `access_key`: YOUR_API_KEY
  - `search`: New York

### Get airline information:

- Endpoint: `/airlines`
- Parameters:
  - `access_key`: YOUR_API_KEY
  - `search`: American Airlines

## 🛠️ Project Structure

```
AviationStack-api-testing/
├── aviationstack.yaml      # OpenAPI specification
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
└── README.md               # This file
```

## 🔄 Choosing Between Options

**Use Option 1 (Direct Swagger UI) when:**

- You want the quickest setup
- You only need to test the API occasionally
- You want to see raw responses from AviationStack

**Use Option 2 (FastAPI Proxy) when:**

- You're building an application that uses AviationStack
- You want to add custom logic, caching, or logging
- You need to modify responses or add error handling
- You're learning FastAPI or building a microservice

## 🐛 Troubleshooting

### Port already in use

If port 8080 or 8000 is already in use, you can change the port:

**For Swagger UI:**

```bash
docker run -p 9090:8080 -e SWAGGER_JSON=/foo/aviationstack.yaml -v ${PWD}:/foo swaggerapi/swagger-ui
```

**For FastAPI:**

```bash
uvicorn main:app --port 9000
```

### API returns error

- Check that your `access_key` is valid
- Verify you haven't exceeded your API rate limit
- Check the AviationStack API status page

## 📚 Additional Resources

- [AviationStack API Documentation](https://aviationstack.com/documentation)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

## 📄 License

This is a testing interface for the AviationStack API. Please refer to AviationStack's terms of service for API usage.

---

**Happy Testing! ✈️**
