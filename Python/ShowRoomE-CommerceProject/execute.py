from pydantic import BaseModel

class ExecuteRequest(BaseModel):

    capability: str