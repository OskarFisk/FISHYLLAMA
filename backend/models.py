from typing import Literal
from pydantic import BaseModel, Field
class Message(BaseModel): role: Literal["system","user","assistant"]; content: str
class ChatRequest(BaseModel): messages:list[Message]=Field(min_length=1); model:str="auto"; provider:str="auto"
class ChatResponse(BaseModel): content:str; provider:str; model:str
