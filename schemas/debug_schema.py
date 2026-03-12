from pydantic import BaseModel
from typing import List


class FixFile(BaseModel):
    filename: str
    description: str
    code: str


class DebugOutput(BaseModel):
    files: List[FixFile]