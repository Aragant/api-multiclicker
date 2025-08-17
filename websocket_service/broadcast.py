async def broadcast(connected: set, message: str):
    for websocket in connected.copy():
        try:
            await websocket.send_text(message)
        except Exception:
            connected.remove(websocket)
