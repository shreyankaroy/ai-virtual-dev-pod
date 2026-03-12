from pydantic import BaseModel
from typing import List


class Component(BaseModel):
    name: str
    description: str


class DataFlow(BaseModel):
    source: str
    target: str
    description: str


class SystemDesignOutput(BaseModel):

    architecture_summary: str

    components: List[Component]

    data_flow: List[DataFlow]