from fastapi import APIRouter, status
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/home",
    tags=["home"],
    responses={404: {"description": "Not found home_api"}},
)


@router.get('/test', status_code=status.HTTP_200_OK)
def signup_user():
    return {"Home Test 4.5" : "Success"}
