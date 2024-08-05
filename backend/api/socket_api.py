from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
import logging
from .SocketManager import SocketManager
import json
from .database_api import fetch_or_create_document_from_db, update_document_in_db 
from schema.Document import Document

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
    
    logger.info("\n\nwebsocket is called!!!\n\n")
    
    await socketManager.connect(websocket, document_id)
    
    logger.debug("\nsocket connection success with document id : " + document_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            logger.debug('\ndatra : ' + str(message))
            
            key = message.get('key')
            value = message.get('value')
            
            if(key == 'get-document'):
                #send the document from database
                logger.debug(f"get document request received for document id : {document_id}")
                
                doc = await (fetch_or_create_document_from_db(value))
                logger.debug(type(doc))
                document_json = doc#.json()

                data_to_send = {
                    "key": "db-document",
                    "value": document_json
                }
                
                await socketManager.send_personal_message(websocket, json.dumps(data_to_send))
                
            if(key == 'changes-received'):
                
                logger.debug(f"changes broadcast request received for document id : {document_id}")

                #broadcast the delta changes to all the users current connected to the document except the one who sent the delta changes 
                data_to_send = {
                    "key": "update-document",
                    "value": value
                }
                await socketManager.broadcast(websocket, document_id, json.dumps(data_to_send))
            
            if(key == 'save-changes'):
                
                logger.debug(f"Save changes request received for document id : {document_id}")

                if(value != ""):
                    await update_document_in_db(document_id, value)
                

                
                
    except WebSocketDisconnect:
        socketManager.disconnect(websocket, document_id)
        
        