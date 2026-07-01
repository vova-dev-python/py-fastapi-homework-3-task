from pydantic import BaseModel, EmailStr, Field


class UserRegistrationRequestSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")


class UserRegistrationResponseSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserActivationRequestSchema(BaseModel):
    email: EmailStr
    token: str


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetCompleteSchema(BaseModel):
    email: EmailStr
    token: str
    password: str = Field(..., min_length=8)


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MessageResponseSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True


PasswordResetCompleteRequestSchema = PasswordResetCompleteSchema
UserLoginResponseSchema = TokenResponseSchema


class UserLoginRequestSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True


TokenRefreshResponseSchema = TokenResponseSchema
