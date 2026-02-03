from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
import re

from conf.database import db


user_bp = Blueprint('usuario',__name__,url_prefix='/usuario')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@user_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    password = request.form.get("password")
    funcao = request.form.get("funcao")
    
    campos = []
    dados = {}
    
     # Validação
    if not all([nome, email, password, funcao]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    #Validação nome unico
    if nome:
        sql_check_nome = text("""
            SELECT COUNT(*) 
            FROM usuario 
            WHERE nome_user ILIKE :nome
        """)
        result = db.session.execute(sql_check_nome, {
            "nome": nome,
        })

        if result.fetchone()[0] > 0:
            return jsonify({"erro": "Nome de Usuário já cadastrado"}), 400
        
    campos.append("nome_user")
    dados["nome_user"] = nome
    
    #Validação email 
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    if not re.match(email_regex, email):
        return jsonify({"erro": "Email inválido"}), 400
    
    campos.append("email")
    dados["email"] = email
    
    #Password mínimo 6 caracteres
    if len(password) < 6:
        return jsonify({"erro": "Senha deve ter no mínimo 6 caracteres"}), 400  
    
    campos.append("password")
    dados["password"] = password
    
    #Função
    if funcao:
        campos.append("funcao")
        dados["funcao"] = funcao

    #SQL
    cols = ", ".join(campos)
    placeholders = ", ".join(':' + c for c in campos)
    sql = text(f"INSERT INTO usuario ({cols}) VALUES ({placeholders}) RETURNING id_user")


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_user = result.fetchone()[0]
    dados['id_user'] = id_user


    return dados

#Selects
#ver usuário/1
@user_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM usuario where id_user = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os usuarios
@user_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM usuario ") #LIMIT 100 OFFSET 100 para paginação
    
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
@user_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    
    #dados que vieram   
    nome = request.form.get("nome")
    email = request.form.get("email")
    password = request.form.get("password")
    funcao = request.form.get("funcao")
    
    #Verificando quais campos foram enviados
    campos = []
    dados = {"id": id}
    
    if nome:
            campos.append("nome_user = :nome")
            dados["nome"] = nome

    if email:
        campos.append("email = :email")
        dados["email"] = email

    if password:
        campos.append("password = :password")
        dados["password"] = password

    if funcao:
        campos.append("funcao = :funcao")
        dados["funcao"] = funcao

    if not campos:
        return "Nenhum dado para atualizar"
    
    #SQL
    sql_update = text("UPDATE fornecedor_empresa SET " + ", ".join(campos) + " WHERE id_company = :id")

    sql_select = text("SELECT * FROM fornecedor_empresa WHERE id_company = :id")
   

    try:
        #DADOS ANTES
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()

        if not antes:
            return f"Fornecedor não encontrado"

        #EXECUTA UPDATE
        result = db.session.execute(sql_update, dados)
        #conta quantas linhas foram afetadas
        linhas_afetadas = result.rowcount  

        if linhas_afetadas == 1:
            db.session.commit()

            #DADOS DEPOIS
            depois = db.session.execute(sql_select, {"id": id}).mappings().first()

            return {
                "msg": f"Fornecedor com id {id} atualizado com sucesso",
                "antes": dict(antes),
                "depois": dict(depois)
            }
        else:
            db.session.rollback()
            return {"msg": "ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"}

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}


#deletar/Destruir
#delete
@user_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM usuario WHERE id_user = :id")
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

