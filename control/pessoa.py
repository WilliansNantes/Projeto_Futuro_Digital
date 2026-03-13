from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
import re

from conf.database import db


pessoa_bp = Blueprint('pessoa',__name__,url_prefix='/pessoa')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@pessoa_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    contato = request.form.get("contato")
    cidade = request.form.get("cidade")    
    
    campos = []
    dados = {}
    score = 0
    media_cons_mes = None

    #Validação do nome
    if nome:
        if not nome or nome.strip() == "":
            return jsonify({"erro": "Nome não pode ser vazio"}), 400
        campos.append("nome")
        dados["nome"] = nome
        
    # Validação do email 
    if email:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return jsonify({"erro": "E-mail inválido"}), 400
        campos.append("email")
        dados["email"] = email

    # Validação do contato 
    if contato:
        contato = contato.replace(" ", "")
        if not contato.isdigit():
            return jsonify({
                "erro": "Numero de contato inválido;Colocar apenas numeros"
            }), 400
        campos.append("contato")
        dados["contato"] = contato
    
    # Validação da cidade
    if cidade:
        campos.append("cidade")
        dados["cidade"] = cidade
        
    
    
    #SQL
    cols = ", ".join(campos)
    placeholders = ", :".join( campos)

    sql = text(f"INSERT INTO pessoas ({cols}) VALUES (:{placeholders}) RETURNING id_pessoa")
    


    #executar consulta
    result = db.session.execute(sql, dados)


    #pega o id
    id_pessoa = result.fetchone()[0]
    dados['id_pessoa'] = id_pessoa
    
    #SCORE base 
    if email and contato:
        score += 100
    else:
        score += 50
        
    campos.append("score")
    dados["score"] = score
            
            
    #Inserindo o status
    if score <= 50:
        status_id = 1 #Lead
    elif score > 50 and score <= 100:
        status_id = 2 #Cliente 
    else:
        status_id = 3 #Cliente Promissor
        
    campos.append("status_id")
    dados["status_id"] = status_id



    db.session.commit()

    return dados
    
    #Selects
#ver usuário/1
@pessoa_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM pessoas where id_pessoa = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os usuarios
@pessoa_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM pessoas ") 
    
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
@pessoa_bp.route("/<id>", methods=["PUT"])
def atualizar(id):

    # dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    contato = request.form.get("contato")
    cidade = request.form.get("cidade")    
    
    
    #verificando pessoa existe
    sql_check = text("SELECT * FROM pessoas WHERE id_pessoa = :id")
    pessoa_atual = db.session.execute(sql_check, {"id": id}).mappings().first()
    
    if not pessoa_atual:
        return jsonify({"erro": "Pessoa não encontrada"}), 404
    
    #calculando score
    score = 0
    media_cons_mes = None
    
    campos_principais = [
        nome, email, contato, cidade,
    ]

    #Verificando quais campos foram enviados
    campos = []
    dados = {"id": id}

    # Validação do nome (somente se alterado)
    if nome:
        sql_check_nome = text("""
            SELECT COUNT(*) 
            FROM pessoas 
            WHERE nome ILIKE :nome
            AND id_pessoa != :id
        """)
        result = db.session.execute(sql_check_nome, {
            "nome": nome,
            "id": id
        })

        if result.fetchone()[0] > 0:
            return jsonify({"erro": "Nome da Pessoa já cadastrado"}), 400

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
    
   
        if email and contato:
         score += 100
        
        else :
         score += 50
            
    campos.append("score")
    dados["score"] = score
            
    #Inserindo o status
    if score <= 50:
        status_id = 1 #Lead
    elif score > 50 and score <= 100:
        status_id = 2 #Cliente 
    else:
        status_id = 3 #Cliente Promissor
        
    campos.append("status_id")
    dados["status_id"] = status_id
        

    if not campos:
            return jsonify({"msg": "Nenhum dado para atualizar"}), 400
            

    sql_update = text(
            "UPDATE pessoas SET " + ", ".join(campos) + " WHERE id_pessoa = :id"
        )

    sql_select = text(
            "SELECT * FROM pessoas WHERE id_pessoa = :id"
        )

    try:
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()
        result = db.session.execute(sql_update, dados)
        
        
        if result.rowcount == 1:
            depois = db.session.execute(sql_select, {"id": id}).mappings().first()
            db.session.commit()

            return {
                "msg": f"Pessoa com id {id} atualizado com sucesso",
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
@pessoa_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM pessoas WHERE id_pessoa = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Pessoa com o id:{id} removida"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)