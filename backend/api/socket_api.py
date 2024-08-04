from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/socket",
    tags=["sockert"],
    responses={404: {"description": "Not found socket_api"}},
)


@router.get('/', status_code=status.HTTP_200_OK)
def signup_user():
    return {"Socket_API" : "Success"}


