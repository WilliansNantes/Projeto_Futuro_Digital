from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db

pedido_bp = Blueprint('pedido',__name__,url_prefix='/pedido')


#CRUD
#Criar 
#insert - SQL
#http/web - POST
@pedido_bp.route("/", methods=["POST"])
def criar():
    #dados que vieram
    cliente = request.form.get("cliente")
    data = request.form.get("data")
    status = request.form.get("status")

    #SQL
    sql = text("INSERT INTO pedidos (cliente_id, data_pedido, status) VALUES (:cliente, :data, :status) RETURNING id")
    dados = {"cliente": cliente, "data": data, "status":status} #os dados do que veio lá da var sql

    try:
        #executar consulta
        result = db.session.execute(sql, dados)
        db.session.commit()


        #pega o id
        id = result.fetchone()[0]
        dados['id'] = id

        return dados
    except Exception as e:
         return f"Erro: {e}"

#Selects

#ver pedido/1 
@pedido_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM pedidos where id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e

#verTodos os pedidos
@pedido_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM pedidos ") #LIMIT 100 OFFSET 100 para paginação
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambi pq cada linha é um objeto


        print(json)


        return json
    except Exception as e:
        
        #salvar log da aplicação 
        #Mandar email programador
        return e



#atualizar 
#update
@pedido_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    #dados que vieram
    cliente = request.form.get("cliente")
    data = request.form.get("data")
    status = request.form.get("status")

    sql = text("UPDATE pedidos set cliente_id = :cliente, data_pedido = :data, status = :status  WHERE id = :id")
    dados = {"cliente": cliente, "data": data, "status" :status, "id" : id} #os dados do que veio lá da var sql
    result = db.session.execute(sql,dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
        
    if linhas_afetadas == 1: 
            db.session.commit()
            return f"Pedido com o id:{id} alterado"
    else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"


#deletar/Destruir
#delete
@pedido_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM pedidos WHERE id = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Pedido com o id:{id} removido"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    except Exception as e:
         return str(e)
