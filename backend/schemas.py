from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CustomerCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    email: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)


class CustomerUpdate(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    email: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)