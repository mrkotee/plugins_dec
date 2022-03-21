from pydantic import BaseModel


class Plugin(BaseModel):
    name: str
    entrypoint: str
    before: bool = False
    after: bool = False
    enabled = bool
    filename: str
