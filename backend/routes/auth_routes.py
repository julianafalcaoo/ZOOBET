from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas, auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registrar", response_model=schemas.Token)
def registrar(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=auth_service.gerar_hash(usuario.senha)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    token = auth_service.criar_token({"sub": novo.email})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login(dados: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    
    if not usuario or not auth_service.verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = auth_service.criar_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(usuario = Depends(auth_service.get_current_user)):
    return {
        "nome": usuario.nome,
        "email": usuario.email
    }