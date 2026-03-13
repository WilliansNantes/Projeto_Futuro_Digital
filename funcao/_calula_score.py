from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
from funcao._calcula_consumo    import _calcula_consumo
import re


from conf.database import db

def _calcula_score(media_pago_mes, pessoa_id):
    
    
    score = text("""
        SELECT score
        FROM pessoas
        WHERE id_pessoa = :pessoa_id
    """)
    result = db.session.execute(score, {"pessoa_id": pessoa_id})
    score = result.fetchone()[0]   # Pega o score atual do cliente
    
     # BÔNUS DE SCORE
    
    if media_pago_mes is not None:
        if 500 <= media_pago_mes < 720:
            score += 50
        elif media_pago_mes >= 720:
            score += 100
            
    if score > 200:
        score = 200  # Limite máximo de score 
    
    
    return score

    
  

