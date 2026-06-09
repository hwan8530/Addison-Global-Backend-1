from pydantic import BaseModel

class Credentials(BaseModel):
  username: str
  password: str

class User(BaseModel):
  userid: str

class UserToken(BaseModel):
  token: str