from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
import re

from conf.database import db


lead_bp = Blueprint('leads',__name__,url_prefix='/lead')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@lead_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    contato = request.form.get("contato")
    cidade = request.form.get("cidade")    
    valor01 = request.form.get("Valor KW/H mes 01")
    valor02 = request.form.get("Valor KW/H mes 02")
    valor03 = request.form.get("Valor KW/H mes 03")
    
    #calculando score
    score = 0

    campos_principais = [
        nome, email, contato, cidade,
        valor01, valor02, valor03
    ]
    
    # Validação do nome 
    if nome:
        sql_check_nome = text("""
            SELECT COUNT(*)
            FROM leads
            WHERE nome ILIKE :nome
        """)
        result = db.session.execute(sql_check_nome, {"nome": nome})

        if result.fetchone()[0] > 0:
            return jsonify({"erro": "Nome já cadastrado"}), 400

    # Validação do email 
    if email:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return jsonify({"erro": "E-mail inválido"}), 400

    # Validação do contato 
    if contato:
        contato = contato.replace(" ", "")
        if not contato.isdigit():
            return jsonify({
                "erro": "Numero de contato inválido;Colocar apenas numeros"
            }), 400
        
    #Verificando se os valores são numericos
    valores = []

    for valor in [valor01, valor02, valor03]:
        if valor:
            try:
                valores.append(float(valor))
            except ValueError:
                return jsonify({"erro": "Os valores de consumo devem ser numéricos"}), 400
            
    #calculando a média
    media_kwh_mes = None
    media_pago_mes = None

    if len(valores) == 3:
        media_kwh_mes = sum(valores) / 3
        media_pago_mes = media_kwh_mes * 0.5
    
    #SCORE base 
    if all(campos_principais):
        score += 50
    
    # BÔNUS DE SCORE 
    if media_pago_mes is not None:
        if media_pago_mes >= 500:
            score += 50
        if media_pago_mes >= 720:
            score += 50
    
    #Inserindo o status
    if score <= 50:
        status_id = 1 #Lead
    elif score <= 100:
        status_id = 2 #Cliente 
    else:
        status_id = 3 #Cliente Promissor
    
    #SQL
    sql = text("""
        INSERT INTO leads (
            nome, email, contato, cidade, score, status_id,
            "valor KW/H mes 01",
            "valor KW/H mes 02",
            "valor KW/H mes 03",
            "Media KW/H por mes",
            "Media pago/mes"
        )
        VALUES (
            :nome, :email, :contato, :cidade, :score, :status_id,
            :valor1, :valor2, :valor3, :media, :media_pago_mes
        )
        RETURNING id_lead
    """)

    dados = {
        "nome": nome,
        "email": email,
        "contato": contato,
        "cidade": cidade,
        "score": score,
        "status_id": status_id,
        "valor1": valores[0] if len(valores) > 0 else None,
        "valor2": valores[1] if len(valores) > 1 else None,
        "valor3": valores[2] if len(valores) > 2 else None,
        "media": media_kwh_mes,
        "media_pago_mes": media_pago_mes
    }

     #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_lead = result.fetchone()[0]
    return jsonify({
        "msg": "Lead criado com sucesso",
        "id_lead": id_lead,
        "score": score,
        "status_id": status_id
    }), 201