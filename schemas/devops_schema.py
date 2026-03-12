from pydantic import BaseModel
from typing import List


class DevOpsFile(BaseModel):
    filename: str
    description: str
    content: str


class DevOpsOutput(BaseModel):
    files: List[DevOpsFile]