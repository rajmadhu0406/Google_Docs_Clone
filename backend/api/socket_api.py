from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
import logging
from .SocketManager import SocketManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/api/socket",
    tags=["socket"],
    responses={404: {"description": "Not found socket_api"}},
)

socketManager = SocketManager()

@router.get('/', status_code=status.HTTP_200_OK)
def signup_user():
    return {"Socket_API" : "Success"}


@router.websocket("/ws/{document_id}")
async def websocket_endpoint(websocket: WebSocket, document_id: str):
    await socketManager.connect(websocket, document_id)
    logger.debug("\nsocket connection success debug")
    try:
        while True:
            delta = await websocket.receive_text()
            logger.debug('\ndelta : ' + str(delta))
            
            #broadcast the delta changes to all the users current connected to the document except the one who sent the delta changes 
            await socketManager.broadcast(websocket, document_id, delta)
    except WebSocketDisconnect:
        socketManager.disconnect(websocket, document_id)
        
        