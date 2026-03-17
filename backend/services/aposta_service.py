from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from services.bicho_service import descobrir_grupo, sortear_milhar


def validar_saldo(usuario, valor):
    if usuario.saldo < valor:
        raise HTTPException(
            status_code=400,
            detail="Saldo insuficiente"
        )


def validar_aposta(tipo, numero, valor):
    if tipo not in ["grupo", "milhar"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    if valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero")

    if tipo == "grupo":
        if numero < 1 or numero > 25:
            raise HTTPException(status_code=400, detail="Grupo inválido")

    if tipo == "milhar":
        if numero < 0 or numero > 9999:
            raise HTTPException(status_code=400, detail="Milhar inválida")


def registrar_aposta(db: Session, usuario, tipo, numero, valor):

    validar_aposta(tipo, numero, valor)
    validar_saldo(usuario, valor)

    try:
        aposta = models.Aposta(
            usuario_id=usuario.id,
            tipo=tipo,
            numero=numero,
            valor=valor,
            status = None
        )

        usuario.saldo -= valor

        db.add(aposta)
        db.commit()
        db.refresh(aposta)

        return aposta

    except Exception as e:
        db.rollback()
        raise e


def calcular_premio(aposta, milhar_sorteada):

    premio = 0

    resultado = descobrir_grupo(milhar_sorteada)
    grupo_sorteado = resultado["grupo"]

    if aposta.tipo == "milhar" and aposta.numero == milhar_sorteada:
        premio = aposta.valor * 4000

    if aposta.tipo == "grupo" and aposta.numero == grupo_sorteado:
        premio = aposta.valor * 18

    return premio



def processar_sorteio(db: Session):

    milhar = sortear_milhar()

    try:
        apostas = db.query(models.Aposta).filter(
            models.Aposta.status == None
        ).all()

        for aposta in apostas:
            usuario = db.query(models.Usuario).filter(
                models.Usuario.id == aposta.usuario_id
            ).first()

            premio = calcular_premio(aposta, milhar)

            if premio > 0:
                usuario.saldo += premio
                aposta.premio = premio
                aposta.status = "ganhou"
            else:
                aposta.premio = 0
                aposta.status = "perdeu"

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    return {"milhar_sorteada": milhar}