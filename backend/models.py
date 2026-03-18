from sqlalchemy import *
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String (100), nullable=False)
    saldo = Column(Float, default=1000.0, nullable=False)

class Aposta(Base):
    __tablename__ = "apostas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(String, nullable=False)  #grupo ou milhar
    numero = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    premio = Column(Float, nullable=False)
    status = Column(String, nullable=False)  #ganhou ou perdeu
    criacao = Column(DateTime(timezone=True), server_default=func.now())