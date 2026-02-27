# Realtime Stream Service

Real-time Stock/Match Data Streaming Service

## Tech Stack

- **FastAPI** - Modern Python web framework
- **WebSocket** - Real-time bidirectional communication
- **Docker** - Containerized deployment

## Features

- Real-time stock price updates (simulated)
- Real-time sports match score updates (simulated)
- WebSocket endpoint for streaming data
- REST API for stock listing
- Docker support for easy deployment

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or just run the container
docker build -t realtime-stream-service .
docker run -p 8000:8000 realtime-stream-service
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/stocks` | List available stocks |
| WS | `/ws` | WebSocket for real-time updates |

## WebSocket Usage

Connect to `ws://localhost:8000/ws`

Example client:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

## Sample Output

```json
{
  "type": "stock_update",
  "data": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": 175.50,
    "change": 2.30,
    "change_percent": 1.33,
    "timestamp": "2026-02-27T10:30:00"
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DEBUG | false | Enable debug mode |
| PORT | 8000 | Server port |

## Deployment to Cloud

### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-west-2.amazonaws.com
docker build -t realtime-stream-service .
docker tag realtime-stream-service:latest ACCOUNT.dkr.ecr.us-west-2.amazonaws.com/realtime-stream-service:latest
docker push ACCOUNT.dkr.ecr.us-west-2.amazonaws.com/realtime-stream-service:latest
```

### GCP Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/realtime-stream-service
gcloud run deploy realtime-stream-service --image gcr.io/PROJECT_ID/realtime-stream-service --platform managed --region us-central1 --allow-unauthenticated
```

### Azure Container Instances

```bash
# Build and deploy
az acr build --registry myregistry --image realtime-stream-service:latest .
az container create --resource-group mygroup --name realtime-stream-service --image myregistry.azurecr.io/realtime-stream-service:latest --cpu 1 --memory 1 --port 8000
```

## License

MIT
