"""
EA Stream Service - Real-time Stock/Match Data Streaming Service
Tech Stack: FastAPI + WebSocket + Docker
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import json
import random
from datetime import datetime

app = FastAPI(title="EA Stream Service", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)


manager = ConnectionManager()


# Simulated stock data generator
STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corp."},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "AMZN", "name": "Amazon.com Inc."},
    {"symbol": "META", "name": "Meta Platforms Inc."},
    {"symbol": "TSLA", "name": "Tesla Inc."},
    {"symbol": "NVDA", "name": "NVIDIA Corp."},
    {"symbol": "EA", "name": "Electronic Arts Inc."},
]


def generate_stock_update():
    """Generate a random stock price update"""
    stock = random.choice(STOCKS)
    base_price = random.uniform(50, 500)
    change = random.uniform(-5, 5)
    
    return {
        "type": "stock_update",
        "data": {
            "symbol": stock["symbol"],
            "name": stock["name"],
            "price": round(base_price, 2),
            "change": round(change, 2),
            "change_percent": round((change / base_price) * 100, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
    }


def generate_match_update():
    """Generate a random sports match update"""
    teams = ["Lakers", "Warriors", "Celtics", "Heat", "Barcelona", "Real Madrid", "Manchester United", "Liverpool"]
    team_a, team_b = random.sample(teams, 2)
    score_a = random.randint(0, 5)
    score_b = random.randint(0, 5)
    
    return {
        "type": "match_update",
        "data": {
            "match_id": f"match_{random.randint(1000, 9999)}",
            "sport": random.choice(["basketball", "football", "soccer"]),
            "team_a": team_a,
            "team_b": team_b,
            "score_a": score_a,
            "score_b": score_b,
            "quarter": random.randint(1, 4),
            "timestamp": datetime.utcnow().isoformat()
        }
    }


async def stream_data():
    """Background task to stream data to all connected clients"""
    while True:
        # Alternate between stock and match updates
        if random.random() > 0.5:
            update = generate_stock_update()
        else:
            update = generate_match_update()
        
        await manager.broadcast(update)
        await asyncio.sleep(1)  # Stream every 1 second


@app.on_event("startup")
async def startup_event():
    """Start the background streaming task"""
    asyncio.create_task(stream_data())


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "EA Stream Service",
        "version": "1.0.0",
        "status": "running",
        "connections": len(manager.active_connections)
    }


@app.get("/api/stocks")
async def get_stocks():
    """Get list of available stocks"""
    return {"stocks": STOCKS}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, wait for messages
            data = await websocket.receive_text()
            # Echo back (can be used for ping/pong)
            await manager.send_personal_message({
                "type": "echo",
                "message": data
            }, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
