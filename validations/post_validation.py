from pydantic import BaseModel, Field
from typing import Optional


class CreatePost(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Post content is required"
    )

    image: Optional[str] = Field(
        None,
        description="Optional image URL or file path"
    )




