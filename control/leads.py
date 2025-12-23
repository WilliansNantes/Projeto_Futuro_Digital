from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


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
    status_id = request.form.get("status_id")      
    valor_kwh_mes_01 = request.form.get("Valor KW/H mes 01")
    valor_kwh_mes_02 = request.form.get("Valor KW/H mes 02")
    valor_kwh_mes_03 = request.form.get("Valor KW/H mes 03")

     # Validação
    if not all([nome, email, contato, cidade, status_id, valor_kwh_mes_01, valor_kwh_mes_02, valor_kwh_mes_03]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    for valor in [valor_kwh_mes_01, valor_kwh_mes_02, valor_kwh_mes_03]:
        try:
            float(valor)
        except ValueError:
            return jsonify({"erro": "Os valores de KW/H devem ser numéricos"}), 400
    while True:
        try:
            status_id = int(status_id)
            break
        except ValueError:
            return jsonify({"erro": "O ID do status deve ser um número inteiro"}), 400


    #SQL
    sql = text("INSERT INTO leads (nome, email, contato, cidade, status_id, valor_kwh_mes_01, valor_kwh_mes_02, valor_kwh_mes_03) VALUES (:nome, :email, :contato, :cidade, :status_id, :valor_kwh_mes_01, :valor_kwh_mes_02, :valor_kwh_mes_03) RETURNING id_lead")
    dados = {"nome": nome, "email": email, "contato": contato, "cidade": cidade, "status_id": status_id, "valor_kwh_mes_01": valor_kwh_mes_01, "valor_kwh_mes_02": valor_kwh_mes_02, "valor_kwh_mes_03": valor_kwh_mes_03} #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_lead = result.fetchone()[0]
    dados['id_lead'] = id_lead


    return dados