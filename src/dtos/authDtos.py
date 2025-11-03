from pydantic import BaseModel
class authDto(BaseModel):
    username: str
    password: str
