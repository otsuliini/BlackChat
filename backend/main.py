from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
clients = []  # List to store connected clients

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    clients.append(websocket)  # Add the new client to the list
    try:
        while True:
            message = await websocket.receive_text()  # Wait for a message
            for client in clients:
                if client != websocket:  # Send message to all other clients (exclude sender)
                    await client.send_text(message)  # Broadcast message
    except WebSocketDisconnect:
        clients.remove(websocket)  # Remove the client if it disconnects
    except Exception as e:
        clients.remove(websocket)  # Remove the client if an error occurs
        print(f"Error: {e}")
