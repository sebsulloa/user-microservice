# User Management Service

This microservice provides a simple API for user management.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/SoloAWS/user-management-service.git
   cd user-management-service
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Service

To run the service locally:

```
uvicorn app.main:app --reload --port 8001
```

The service will be available at `http://localhost:8001`.

## API Endpoints

- `GET /`: Returns a "Hello World" message
- `GET /health`: Health check endpoint

## Docker

To build and run the Docker container:

```
docker build -t user-management-service .
docker run -p 8001:8001 user-management-service
```

Make sure to expose port 8001 in your Dockerfile:

```dockerfile
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```
