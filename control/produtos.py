from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db


product_bp = Blueprint('produtos',__name__,url_prefix='/produto')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@product_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    nome = request.form.get("nome_produto")
    valor = request.form.get("valor_por_unidade")
    qtd_comprado = request.form.get("qtd_comprado")
    qtd_vendido = request.form.get("qtd_vendido")
    qtd_in_stock = request.form.get("qtd_in_stock")
    fornecedor_id = request.form.get("fornecedor_id")
    
    
     # Validação
    if not all([nome, valor, qtd_comprado, qtd_vendido, qtd_in_stock, fornecedor_id]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400


    #SQL
    sql = text("INSERT INTO produtos (nome_produto, valor_por_unidade, qtd_comprado, qtd_vendido, qtd_in_stock, fornecedor_id) VALUES (:nome_produto, :valor_por_unidade, :qtd_comprado, :qtd_vendido, :qtd_in_stock, :fornecedor_id) RETURNING id_produto")
    dados = {"nome_produto": nome, "valor_por_unidade": valor, "qtd_comprado": qtd_comprado, "qtd_vendido": qtd_vendido, "qtd_in_stock": qtd_in_stock, "fornecedor_id": fornecedor_id} #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_produto = result.fetchone()[0]
    dados['id_produto'] = id_produto


    return dados

#Selects
#ver produto/1
@product_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM produtos where id_produto = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os produtos
@product_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM produtos ") #LIMIT 100 OFFSET 100 para paginação
    
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
@product_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    
    #dados que vieram   
    nome = request.form.get("nome_produto")
    valor = request.form.get("valor_por_unidade")
    qtd_comprado = request.form.get("qtd_comprado")
    qtd_vendido = request.form.get("qtd_vendido")
    qtd_in_stock = request.form.get("qtd_in_stock")
    fornecedor_id = request.form.get("fornecedor_id")
    
    #Verificando quais campos foram enviados
    campos = []
    dados = {"id": id}
    
    if nome:
            campos.append("nome_produto = :nome")
            dados["nome"] = nome

    if valor:
        campos.append("valor_por_unidade = :valor")
        dados["valor"] = valor

    if qtd_comprado:
        campos.append("qtd_comprado = :qtd_comprado")
        dados["qtd_comprado"] = qtd_comprado

    if qtd_vendido:
        campos.append("qtd_vendido = :qtd_vendido")
        dados["qtd_vendido"] = qtd_vendido

    if qtd_in_stock:
        campos.append("qtd_in_stock = :qtd_in_stock")
        dados["qtd_in_stock"] = qtd_in_stock

    if fornecedor_id:
        campos.append("fornecedor_id = :fornecedor_id")
        dados["fornecedor_id"] = fornecedor_id

    if not campos:
        return "Nenhum dado para atualizar"
    
    #SQL
    sql_update = text("UPDATE produtos SET " + ", ".join(campos) + " WHERE id_produto = :id")

    sql_select = text("SELECT * FROM produtos WHERE id_produto = :id")
   
    try:
        
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()

        if not antes:
            return "Usuário não encontrado"

        
        result = db.session.execute(sql_update, dados)
        linhas_afetadas = result.rowcount

        if linhas_afetadas != 1:
            db.session.rollback()
            return "ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"

        
        db.session.commit()

        
        depois = db.session.execute(sql_select, {"id": id}).mappings().first()
        
        if not depois:
            return jsonify({"erro": "Falha ao recuperar dados atualizados"}), 500

        # verificar quais campos foram alterados
        alterados = {}

        for campo in depois.keys():
            if antes[campo] != depois[campo]:
                alterados[campo] = {
                    "antes": antes[campo],
                    "depois": depois[campo]
                }

        return jsonify({
    "mensagem": f"Produto com o id:{id} alterado",
    "dados_alterados": alterados,
    "Produto_atualizado": dict(depois)
}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)})

#deletar/Destruir
#delete
@product_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM produtos WHERE id_produto = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Produto com o id:{id} removido"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)