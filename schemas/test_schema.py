from pydantic import BaseModel
from typing import List


class TestFile(BaseModel):
    filename: str
    description: str
    code: str


class TestOutput(BaseModel):
    files: List[TestFile]