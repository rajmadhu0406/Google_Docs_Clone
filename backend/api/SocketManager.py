from fastapi import FastAPI, WebSocket
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

class SocketManager:
    def __init__(self):
        self.active_connections = dict()

    async def connect(self, websocket: WebSocket, documentId: str):
        await websocket.accept()
        document_connections = self.active_connections.get(documentId, set())
        document_connections.add(websocket)
        self.active_connections.update({documentId : document_connections})


    def disconnect(self, websocket: WebSocket, documentId: str):
        document_connections = self.active_connections.get(documentId, {})
        
        current_connections_count = len(document_connections)
        if(current_connections_count == 0):
            return
        elif(current_connections_count == 1):
            self.active_connections.pop(documentId) # Removes 'b' and returns its value; returns 'None' if 'b' is not found
        else:
            document_connections.remove(websocket)
            self.active_connections.update({documentId : document_connections})


    async def send_personal_message(self, websocket: WebSocket, message: str):
        try:   
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message to connection: {e}")


    async def broadcast(self, websocket: WebSocket, documentId: str, message: str):
        if documentId in self.active_connections:
            for connection in self.active_connections.get(documentId):
                if(connection == websocket):
                    continue
                try:   
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message to connection: {e}")
