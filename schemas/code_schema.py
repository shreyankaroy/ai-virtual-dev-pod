from pydantic import BaseModel
from typing import List


class CodeFile(BaseModel):
    filename: str
    description: str
    code: str


class CodeOutput(BaseModel):
    files: List[CodeFile]