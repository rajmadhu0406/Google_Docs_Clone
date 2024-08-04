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


async def create_document(document: Document):
    try:    
        table.put_item(Item=document.dict())
        return True
    except Exception as e:
        logger.error(f"Error saving document {document.id}: {e.response['Error']['Message']}")
        return False
        
# Create a document
@router.post("/documents")
async def create_document_api(document: Document):
    try:
        # Put item in DynamoDB table
        success = await create_document(document)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to create document in database")
        
        return {"message": "Document created successfully", "document_id": document.id}
    
    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")



async def fetch_document_from_db(document_id: str):
    """Fetch document from DynamoDB by its ID."""
    try:
        response = table.get_item(Key={'id': document_id})
        if 'Item' not in response:
            logger.info(f"Document with ID {document_id} not found.")
            return None
        document = Document(**response['Item'])  
        return document.json()  
    except ClientError as e:
        logger.error(f"Error fetching document {document_id}: {e.response['Error']['Message']}")
        raise

# Get a document by id
@router.get("/documents/{document_id}")
async def get_document_api(document_id: str):
    """API endpoint to get a document by its ID."""
    try:
        document = await fetch_document_from_db(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except ClientError as e:
        logger.error(f"Client error while fetching document {document_id}: {e.response['Error']['Message']}")
        raise HTTPException(status_code=500, detail="Failed to get document from database")
    except Exception as e:
        logger.error(f"Unexpected error while fetching document {document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")