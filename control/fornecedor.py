from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
import re

from conf.database import db


fornecedor_bp = Blueprint('fornecedor',__name__,url_prefix='/fornecedor')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@fornecedor_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    contato = request.form.get("contato").replace(" ", "")
    cidade = request.form.get("cidade")
    status = request.form.get("status")
    
    
     # Validação
    if not all([  nome,email,contato,status,cidade]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    #verificar nome tem igual
    sql_check_nome = text("SELECT COUNT(*) FROM fornecedor_empresa WHERE name_company ilike :nome")
    result = db.session.execute(sql_check_nome, {"nome": nome})
    resultado = result.fetchone()
    if resultado[0] > 0:
        return jsonify({"erro": "Nome da empresa já cadastrado"}), 400
    
    
    # Validação do email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    if not re.match(email_regex, email):
        return jsonify({"erro": "Email inválido"}), 400

    # Validação do contato (somente números)
    if not contato.isdigit():
        return jsonify({
            "erro": "Numero de contato inválido;Colocar apenas numero"
        }), 400

    # Validação do status (somente número)
    if not status.isdigit():
        return jsonify({
            "erro": "Digite o digito do Status"
        }), 400
    
    # Verifica se status é válido
    sql_check_status = text("SELECT COUNT(*) FROM status WHERE id_status = :status_id")
    result = db.session.execute(sql_check_status, {"status_id": status})  
      
    if result.fetchone()[0] == 0:
        return jsonify({"erro": "Status inválido"}), 400


    #SQL
    sql = text("""
        INSERT INTO fornecedor_empresa (
             name_company, email_company, contato, cidade, status_id
        ) 
        VALUES (
            :nome, :email, :contato, :cidade, :status
        ) 
        RETURNING id_company
        """)
    
    dados = {
        "nome": nome, 
        "email": email, 
        "contato": contato, 
        "cidade": cidade, 
        "status": status
        } #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_company = result.fetchone()[0]
    dados['id_company'] = id_company


    return dados

#Selects
#ver usuário/1
@fornecedor_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM fornecedor_empresa where id_company = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os usuarios
@fornecedor_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM fornecedor_empresa ") #LIMIT 100 OFFSET 100 para paginação
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambi pq cada linha é um objeto


        print(json)


        return json
    
    except Exception as e:
        return str(e)

#atualizar 
#update
@fornecedor_bp.route("/<id>", methods=["PUT"])
def atualizar(id):

    # dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    contato = request.form.get("contato")
    cidade = request.form.get("cidade")
    status = request.form.get("status")

    campos = []
    dados = {"id": id}

    # Validação do nome (somente se alterado)
    if nome:
        sql_check_nome = text("""
            SELECT COUNT(*) 
            FROM fornecedor_empresa 
            WHERE name_company ILIKE :nome
            AND id_company != :id
        """)
        result = db.session.execute(sql_check_nome, {
            "nome": nome,
            "id": id
        })

        if result.fetchone()[0] > 0:
            return jsonify({"erro": "Nome da empresa já cadastrado"}), 400

        campos.append("name_company = :nome")
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

    # Validação do status (somente se alterado)
    if status:
        if not status.isdigit():
            return jsonify({"erro": "Digite o digito do Status"}), 400

        sql_check_status = text("""
            SELECT COUNT(*) 
            FROM status 
            WHERE id_status = :status_id
        """)
        result = db.session.execute(sql_check_status, {"status_id": status})

        if result.fetchone()[0] == 0:
            return jsonify({"erro": "Status inválido"}), 400

        campos.append("status_id = :status")
        dados["status"] = status

    if not campos:
        return jsonify({"msg": "Nenhum dado para atualizar"}), 400

    sql_update = text(
        "UPDATE fornecedor_empresa SET " + ", ".join(campos) + " WHERE id_company = :id"
    )

    sql_select = text(
        "SELECT * FROM fornecedor_empresa WHERE id_company = :id"
    )

    try:
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()
        result = db.session.execute(sql_update, dados)
        
        
        if result.rowcount == 1:
            depois = db.session.execute(sql_select, {"id": id}).mappings().first()
            db.session.commit()

            return {
                "msg": f"Fornecedor com id {id} atualizado com sucesso",
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
@fornecedor_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM fornecedor_empresa WHERE id_company = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Usuário com o id:{id} removida"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)
