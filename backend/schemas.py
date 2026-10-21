from pydantic import BaseModel


class CustomerCreate(BaseModel):
    company_name: str
    email: str
