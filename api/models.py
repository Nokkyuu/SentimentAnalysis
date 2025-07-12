from pydantic import BaseModel
from typing import List

class TextRequest(BaseModel):
    text: str

class BulkTextRequest(BaseModel):
    texts: List[str]