from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db

itens_compra_bp = Blueprint('itens_compra',__name__,url_prefix='/itens_compra')


#CRUD
#Criar 
#insert - SQL
#http/web - POST
@itens_compra_bp.route("/", methods=["POST"])
def criar():
    #dados que vieram
    pedido = request.form.get("pedido")
    produto = request.form.get("produto")
    quantidade = request.form.get("quantidade")
    preco = request.form.get("preco")

    #SQL
    sql = text("INSERT INTO pedidos (pedido_id, produto_id, quantidade,preco_unitario) VALUES (:pedido, :produto, :quantidade, :preco) RETURNING id")
    dados = {"pedido": pedido, "produto": produto, "quantidade":quantidade, "preco" :preco} #os dados do que veio lá da var sql

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

#ver item/1 
@itens_compra_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM itens_compra where id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e

#verTodos os itens
@itens_compra_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM itens_compra ") #LIMIT 100 OFFSET 100 para paginação
    
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
@itens_compra_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    #dados que vieram
    pedido = request.form.get("pedido")
    produto = request.form.get("produto")
    quantidade = request.form.get("quantidade")
    preco = request.form.get("preco")

    sql = text("INSERT INTO pedidos (pedido_id, produto_id, quantidade,preco_unitario) VALUES (:pedido, :produto, :quantidade, :preco) RETURNING id")
    dados = {"pedido": pedido, "produto": produto, "quantidade":quantidade, "preco" :preco} #os dados do que veio lá da var sql
    
    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
        
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Item de compra com o id:{id} alterado"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    except Exception as e:
            return str(e)


#deletar/Destruir
#delete
@itens_compra_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM itens_compra WHERE id = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Item de compra com o id:{id} removido"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    except Exception as e:
         return str(e)