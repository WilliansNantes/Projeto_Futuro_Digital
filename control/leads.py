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
    valor01 = request.form.get("Valor KW/H mes 01")
    valor02 = request.form.get("Valor KW/H mes 02")
    valor03 = request.form.get("Valor KW/H mes 03")

     # Validação
    if not all([nome, email, contato, cidade, status_id, valor01, valor02, valor03]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    #verifica se contato, status são numeros
    if not contato.isdigit() or not status_id.isdigit():
        return jsonify({"erro": "Contato e Status devem ser números"}), 400
        
    #Verificando se os valores são numericos
    try:    
        valor01 = float(valor01)
        valor02 = float(valor02)
        valor03 = float(valor03)
    except ValueError:
        return jsonify({"erro": "Os valores de consumo devem ser numéricos"}), 400

    try:
        status_id = int(status_id)
    except ValueError:
        return jsonify({"erro": "O ID do status deve ser um número inteiro"}), 400
    
    # Validação do email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    if not re.match(email_regex, email):
        return jsonify({"erro": "Email inválido"}), 400
    
    #calculando a média
    media_kwh_mes = (valor01 + valor02 + valor03) / 3
    
    #calculando a media paga mes
    media_pago_mes = media_kwh_mes * 0.5  # Exemplo de cálculo

    #Verificando se o status existe
    sql_status = text("SELECT id_status FROM status WHERE id_status = :status_id")
    resultado_status = db.session.execute(sql_status, {"status_id": status_id}).fetchone()

    if resultado_status is None:
        return jsonify({"erro": "Status não existente!"}), 400
    
    #SQL
    sql = text("""
        INSERT INTO leads (
            nome, email, contato, cidade, status_id,
            "valor KW/H mes 01",
            "valor KW/H mes 02",
            "valor KW/H mes 03",
            "Media KW/H por mes"
            "Media pago/mes"
        )
        VALUES (
            :nome, :email, :contato, :cidade, :status_id,
            :valor1, :valor2, :valor3, :media, :media_pago_mes
        )
        RETURNING id_lead
    """)

    dados = {
        "nome": nome,
        "email": email,
        "contato": contato,
        "cidade": cidade,
        "status_id": status_id,
        "valor1": valor01,
        "valor2": valor02,
        "valor3": valor03,
        "media": media_kwh_mes
        "media.pago.mes": media_pago_mes
    }

     #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_lead = result.fetchone()[0]
    dados['id_lead'] = id_lead


    return dados