from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    model_validator,
    field_validator,
)


class CustomerCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    email: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)


class CustomerUpdate(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    email: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)


class CustomerRegister(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    confirm_password: str = Field(min_length=12, max_length=128)

    # Preserve passwords exactly as entered.
    model_config = ConfigDict(str_strip_whitespace=False)

    @field_validator("company_name", mode="before")
    @classmethod
    def clean_company_name(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class CustomerLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    # Passwords must not be modified during login.
    model_config = ConfigDict(str_strip_whitespace=False)

class CustomerResponse(BaseModel):
    id: int
    company_name: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)