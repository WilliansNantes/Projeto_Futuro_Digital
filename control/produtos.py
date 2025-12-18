from flask import Flask, Blueprint, request,jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db

produto_bp = Blueprint('produto',__name__,url_prefix='/produto')


#CRUD
#Criar 
#insert - SQL
#http/web - POST
@produto_bp.route("/", methods=["POST"])
def criar_produto_com_id():
    #dados que vieram
    nome = request.form.get("nome")
    preco = request.form.get("preco")
    estoque = request.form.get("estoque")
    marca = request.form.get("marca")


    #SQL
    sql = text("INSERT INTO produtos (nome_produto, preco, estoque, marca_id) VALUES (:nome, :preco, :estoque, :marca) RETURNING id")
    dados = {"nome": nome, "preco": preco, "estoque":estoque, "marca":marca} #os dados do que veio lá da var sql
     
    try:
        # executar consulta
        result = db.session.execute(sql, dados)
        db.session.commit()


        # pega o id
        id_gerado = result.fetchone()[0]
        dados['id'] = id_gerado
        
        return dados
    except Exception as e:
        return f"Erro: {e}"


#Selects
#ver produto/1 
@produto_bp.route('/<id>')
def get_produto(id):
    sql = text("SELECT * FROM produtos WHERE id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        # Mapear todas as colunas para a linha
        linhas = result.mappings().all()
        
        if len(linhas) > 0:
            return dict(linhas[0])
        else:
            return "Produto não encontrado"
            
    except Exception as e:
        return str(e)
 
#verTodos os produtos
@produto_bp.route('/all')
def get_all_produtos():
    sql_query = text("SELECT * FROM produtos")
    
    try:
        result = db.session.execute(sql_query)
        
        relatorio = result.mappings().all()
        json_output = [dict(row) for row in relatorio] # Converte linhas em lista de dicionários


        return json_output
    except Exception as e:
        return []

#atualizar 
#update
@produto_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    #dados que vieram
    nome = request.form.get("nome")
    preco = request.form.get("preco")
    estoque = request.form.get("estoque")
    marca = request.form.get("marca")
    sql = text("UPDATE produtos set nome_produto = :nome, preco = :preco, estoque = :estoque, marca_id = :marca  WHERE id = :id")
    dados = {"nome": nome, "preco": preco, "estoque" :estoque, "marca" :marca, "id" : id} #os dados do que veio lá da var sql
    
    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
        
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Produto com o id:{id} alterado"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    except Exception as e:
        return str(e)

#deletar/Destruir
#delete
@produto_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM produtos WHERE id = :id")
    dados = {"id": id}
    
    
    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Produto com o id:{id} removido"
        else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    except Exception as e:
        return str(e)

