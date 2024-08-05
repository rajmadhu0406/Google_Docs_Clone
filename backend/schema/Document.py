from pydantic import BaseModel, Field
import uuid
from typing import Optional

class Document(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    Data: object
