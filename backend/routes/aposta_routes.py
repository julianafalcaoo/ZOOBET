from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
import models, schemas
from services import aposta_service
import auth_service


router = APIRouter(prefix="/apostas", tags=["Apostas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ApostaResponse)
def criar_aposta(
    dados: schemas.ApostaCreate,
    db: Session = Depends(get_db),
    usuario = Depends(auth_service.get_current_user)
):
    aposta = aposta_service.registrar_aposta(
        db=db,
        usuario=usuario,
        tipo=dados.tipo,
        numero=dados.numero,
        valor=dados.valor
    )

    return aposta


@router.get("/", response_model=list[schemas.ApostaResponse])
def listar_apostas(
    db: Session = Depends(get_db),
    usuario = Depends(auth_service.get_current_user)
):
    apostas = db.query(models.Aposta).filter(
        models.Aposta.usuario_id == usuario.id
    ).all()

    return apostas


@router.post("/sortear")
def sortear(
    db: Session = Depends(get_db)
):
    resultado = aposta_service.processar_sorteio(db)
    return resultado