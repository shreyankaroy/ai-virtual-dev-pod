from pydantic import BaseModel
from typing import List


class UserStory(BaseModel):
    title: str
    description: str
    acceptance_criteria: List[str]


class UserStoriesOutput(BaseModel):
    stories: List[UserStory]