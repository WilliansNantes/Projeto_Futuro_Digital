
from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
from funcao._perse_decimal     import _parse_decimal
import re


from conf.database import db


def _calcula_consumo( pessoa_id):
    
    dados = {}
    
    #Calculando a média de consumo e valor pago
    valores = []
    sql_media = text("""
        SELECT valor_consumo
        FROM consumo
        WHERE pessoa_id = :pessoa_id
        ORDER BY ano DESC, mes DESC
        LIMIT 3
    """)
    result = db.session.execute(sql_media, {"pessoa_id": pessoa_id})
    valores = [row[0] for row in result.fetchall()]
    
    
    quantidade_valores = len(valores)
    if quantidade_valores == 3:
        media_kwh_mes = sum(valores) / 3
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
    elif quantidade_valores == 2:
        media_kwh_mes = sum(valores) / 2
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
    elif quantidade_valores == 1:    
        media_kwh_mes = valores[0]
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
    else: 
        media_kwh_mes = None
        media_pago_mes = None
        
        
        
        dados["media_kwh_mes"] = media_kwh_mes
        
        dados["media_pago_mes"] = media_pago_mes
            
    return  dados           