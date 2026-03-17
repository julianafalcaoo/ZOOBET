from pydantic import *

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str


class ApostaCreate(BaseModel):
    tipo: str 
    numero: int
    valor: float

    @field_validator("tipo")
    def validar_tipo (cls, v):
        if v not in ["grupo", "milhar"]:
            raise ValueError
        return v
    
    @field_validator("valor")
    def validar_valor(cls, v):
        if v<=0:
            raise ValueError ("Valor deve ser maior que 0")
        return v

class ApostaResponse(BaseModel):
    id: int
    tipo: str
    numero: int
    valor: float
    status: str
    premio: float

    class Config:
        orm_mode = True