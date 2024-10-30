from pydantic import BaseModel


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True
