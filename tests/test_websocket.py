import pytest
import asyncio
import websockets
import pytest_asyncio

@pytest.mark.asyncio
async def test_websocket():
    uri = "ws://localhost:8000/ws"
    
    async with websockets.connect(uri) as websocket1, websockets.connect(uri) as websocket2:
        await websocket1.send("Hello from client 1")
        response1 = await websocket2.recv()
        assert "Hello from client 1" in response1
        
        await websocket2.send("Hello from client 2")
        response2 = await websocket1.recv()
        assert "Hello from client 2" in response2