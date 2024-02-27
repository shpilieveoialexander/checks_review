from pydantic import BaseModel


class MsgResponse(BaseModel):
    """Schema for JSON Responses"""

    msg: str


class TMPTokenResponse(MsgResponse):
    """Schema for JSON Responses"""

    tmp_token: str
