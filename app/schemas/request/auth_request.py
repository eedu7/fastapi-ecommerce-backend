from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class AuthBase(BaseModel):
    email: EmailStr = Field(
        ..., description="User email address used for login and account verification."
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class AuthRegister(AuthBase):
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Unique username for the user. Must be 3–30 characters long.",
        examples=["john_doe"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=32,
        description=(
            "Password for the account. Must be 8–32 characters and include at least "
            "one uppercase letter, one lowercase letter, one digit, and one special character."
        ),
        examples=["P@ssw0rd123!"],
    )

    @field_validator("password", mode="before")
    def password_strength(cls, v: str) -> str:
        if len(v) < 8 or len(v) > 32:
            raise ValueError("Password must be between 8 and 32 characters")

        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")

        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least one special character")

        return v


class AuthLogin(AuthBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=32,
        description="Password for the account. Must match the password used during registration.",
        examples=["P@ssw0rd123!"],
    )

    model_config = ConfigDict(extra="forbid")


class AuthLogout(BaseModel):
    access_token: str = Field(..., min_length=1, description="Access Token")
    refresh_token: str = Field(..., min_length=1, description="Refresh Token")
