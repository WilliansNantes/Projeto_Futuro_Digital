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
    
    # Validação do campo cidade
    if not cidade:
        return jsonify({"erro": "Cidade é obrigatória"}), 400
        
    #Verificando se os valores são numericos
    valores = []
    campos_valor = [valor01, valor02, valor03]

    # Conta quantos campos foram preenchidos
    campos_preenchidos = [v for v in campos_valor if v]

    # REGRA:
    # - 0 preenchidos → ok
    # - 3 preenchidos → ok
    # - 1 ou 2 → erro
    
    if len(campos_preenchidos) not in (0, 3):
        return jsonify({
            "erro": "Preencha todos os campos de consumo"
        }), 400

    # Se os 3 foram preenchidos, valida e converte
    if len(campos_preenchidos) == 3:
        try:
            valores = [float(v) for v in campos_valor]
        except ValueError:
            return jsonify({
                "erro": "Os valores de consumo devem ser numéricos"
            }), 400

        media_kwh_mes = sum(valores) / 3
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
    else:
        media_kwh_mes = None
        media_pago_mes = None
        
        
    #SCORE base 
    total_campos = len(campos_principais)
    preenchidos = len([c for c in campos_principais if c])

    if preenchidos == total_campos:
        score += 50
    elif preenchidos > 0:
        score += 25
    
    # BÔNUS DE SCORE 
    if media_pago_mes is not None:
        if 500 <= media_pago_mes < 720:
            score += 50
        elif media_pago_mes >= 720:
            score += 100
    
    #Inserindo o status
    if score <= 50:
        status_id = 1 #Lead
    elif score > 50 and score <= 100:
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
    
    #Selects
#ver usuário/1
@lead_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM leads where id_lead = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os usuarios
@lead_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM leads ") 
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambiara pq cada linha é um objeto


        print(json)


        return json
    
    except Exception as e:
        return str(e)
    
#atualizar 
#update
@lead_bp.route("/<id>", methods=["PUT"])
def atualizar(id):

    # dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    contato = request.form.get("contato")
    cidade = request.form.get("cidade")    
    valor01 = request.form.get("Valor KW/H mes 01")#alterar nome 
    valor02 = request.form.get("Valor KW/H mes 02")
    valor03 = request.form.get("Valor KW/H mes 03")
    
    
    #verificando lead existe
    sql_check = text("SELECT * FROM leads WHERE id_lead = :id")
    lead_atual = db.session.execute(sql_check, {"id": id}).mappings().first()
    
    if not lead_atual:
        return jsonify({"erro": "Lead não encontrado"}), 404
    
    #calculando score
    score = 0
    
    campos_principais = [
        nome, email, contato, cidade,
        valor01, valor02, valor03
    ]

    #Verificando quais campos foram enviados
    campos = []
    dados = {"id": id}

    # Validação do nome (somente se alterado)
    if nome:
        sql_check_nome = text("""
            SELECT COUNT(*) 
            FROM leads 
            WHERE nome ILIKE :nome
            AND id_lead != :id
        """)
        result = db.session.execute(sql_check_nome, {
            "nome": nome,
            "id": id
        })

        if result.fetchone()[0] > 0:
            return jsonify({"erro": "Nome da Lead já cadastrado"}), 400

        campos.append("nome = :nome")
        dados["nome"] = nome

    # Validação do email (somente se alterado)
    if email:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return jsonify({"erro": "Email inválido"}), 400

        campos.append("email = :email")
        dados["email"] = email

    # Validação do contato (somente se alterado)
    if contato:
        contato = contato.replace(" ", "")

        if not contato.isdigit():
            return jsonify({
                "erro": "Numero de contato inválido;Colocar apenas numero"
            }), 400

        campos.append("contato = :contato")
        dados["contato"] = contato

    # Cidade (sem validação extra)
    if cidade:
        campos.append("cidade = :cidade")
        dados["cidade"] = cidade
    
    # Validação dos valores de consumo (somente se alterado)
    valores = []
    campos_valor = [valor01, valor02, valor03]
    valores_enviados = [v for v in campos_valor if v]   
    if len(valores_enviados) not in (0, 3):
        return jsonify({
            "erro": "Preencha todos os campos de consumo"
        }), 400
    if len(valores_enviados) == 3:
        try:
            valores = [float(v) for v in campos_valor]
        except ValueError:
            return jsonify({
                "erro": "Os valores de consumo devem ser numéricos"
            }), 400

        media_kwh_mes = sum(valores) / 3
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
        
        campos.append('"valor KW/H mes 01" = :valor1')
        campos.append('"valor KW/H mes 02" = :valor2')
        campos.append('"valor KW/H mes 03" = :valor3')
        campos.append('"Media KW/H por mes" = :media')
        campos.append('"Media pago/mes" = :media_pago_mes')
        campos.append("score = :score")
        campos.append("status_id = :status_id")

        dados["valor1"] = valores[0] if len(valores) > 0 else None
        dados["valor2"] = valores[1] if len(valores) > 1 else None
        dados["valor3"] = valores[2] if len(valores) > 2 else None
        dados["media"] = media_kwh_mes
        dados["media_pago_mes"] = media_pago_mes
        
        
    #SCORE BASE 
    total_campos = len(campos_principais)
    preenchidos = len([c for c in campos_principais if c])

    if preenchidos == total_campos:
        score += 50
    elif preenchidos > 0:
        score += 25 
        
    # BÔNUS DE SCORE 
    media_pago_mes = None
    if media_pago_mes is not None:
        if 500 <= media_pago_mes < 720:
            score += 50
        elif media_pago_mes >= 720:
            score += 100
    
    #Inserindo o status
    if score <= 50:
        status_id = 1 #Lead
    elif score > 50 and score <= 100:
        status_id = 2 #Cliente 
    else:
        status_id = 3 #Cliente Promissor
        
    dados["score"] = score
    dados["status_id"] = status_id
        

    if not campos:
            return jsonify({"msg": "Nenhum dado para atualizar"}), 400
            

    sql_update = text(
            "UPDATE leads SET " + ", ".join(campos) + " WHERE id_lead = :id"
        )

    sql_select = text(
            "SELECT * FROM leads WHERE id_lead = :id"
        )

    try:
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()
        result = db.session.execute(sql_update, dados)
        
        
        if result.rowcount == 1:
            depois = db.session.execute(sql_select, {"id": id}).mappings().first()
            db.session.commit()

            return {
                "msg": f"Lead com id {id} atualizado com sucesso",
                "antes": dict(antes),
                "depois": dict(depois)
            }
        else:
            db.session.rollback()
            return jsonify({"msg": "ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500
    
    #deletar/Destruir
#delete
@lead_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM leads WHERE id_lead = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Lead com o id:{id} removida"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)