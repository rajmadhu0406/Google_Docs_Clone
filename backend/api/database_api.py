from schema.Document import Document
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import logging
import os

# Load environment variables from .env file through docker-compose

# AWS_ACCESS_KEY_ID=your-access-key-id
# AWS_SECRET_ACCESS_KEY=your-secret-access-key
# AWS_DEFAULT_REGION=your-region

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_DEFAULT_REGION')

print(f"Region: {region}")
print(f"aws_access_key_id: {aws_access_key_id}")
print(f"aws_secret_access_key: {aws_secret_access_key}")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/database",
    tags=["database"],
    responses={404: {"description": "Not found database_api"}},
)


dynamodb = boto3.resource(
    'dynamodb',
    region_name=region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Reference the DynamoDB table
table = dynamodb.Table('SocketDocuments')


# Create a document
@router.post("/documents")
async def create_document(document: Document):
    try:
        # Put item in DynamoDB table
        table.put_item(Item=document.dict())
        return {"message": "Document created successfully", "document_id": document.id}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create document: {e.response['Error']['Message']}")



# Get a document by id
@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    try:
        response = table.get_item(Key={'id': document_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Document not found")
        return response['Item']
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document: {e.response['Error']['Message']}")
