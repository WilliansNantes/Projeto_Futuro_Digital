from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db


cliente_bp = Blueprint('cliente',__name__,url_prefix='/cliente')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@cliente_bp.route("/", methods=["POST"])
def criar():
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    cidade = request.form.get("cidade")


    #SQL
    sql = text("INSERT INTO clientes (nome_cliente, email, cidade) VALUES (:nome, :email, :cidade) RETURNING id")
    dados = {"nome": nome, "email": email, "cidade": cidade} #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id = result.fetchone()[0]
    dados['id'] = id


    return dados

#Selects
#ver cliente/1
@cliente_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM clientes where id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os clientes
@cliente_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM clientes ") #LIMIT 100 OFFSET 100 para paginação
    
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
@cliente_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    cidade = request.form.get("cidade")
    sql = text("UPDATE clientes set nome_cliente = :nome, email = :email, cidade = :cidade WHERE id = :id")
    dados = {"nome": nome, "email": email, "cidade": cidade, "id" : id} #os dados do que veio lá da var sql
    
    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
        
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Cliente com o id:{id} alterado"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    except Exception as e:
            return str(e)


#deletar/Destruir
#delete
@cliente_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM clientes WHERE id = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Cliente com o id:{id} removida"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
   
    except Exception as e:
         return str(e)

