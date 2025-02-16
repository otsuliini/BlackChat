from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            sender = websocket.client
            for client in clients:
                if client != websocket:
                    await client.send_text(f"{sender}: {message}")
    except WebSocketDisconnect:
        clients.remove(websocket)
    except Exception as e:
        clients.remove(websocket)
        print(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)