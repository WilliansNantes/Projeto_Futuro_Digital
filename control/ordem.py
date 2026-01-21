from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
from datetime import datetime

from conf.database import db


ordem_bp = Blueprint('ordem',__name__,url_prefix='/ordem')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@ordem_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    lead_id = request.form.get("lead")
    data_ordem = request.form.get("data_ordem")
    produto_id = request.form.get("produto_id")
    quantidade = request.form.get("quantidade").replace(',','.')
    valor_vendido = request.form.get("valor_vendido").replace(',','.')
    status = request.form.get("status")
    
    
     # Validações
     # Verifica se todos os campos obrigatórios foram fornecidos
    if not all([lead_id,data_ordem, produto_id, quantidade, valor_vendido, status]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    # Valida e converte a data
    try:
        data_ordem = datetime.strptime(data_ordem, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Data da ordem inválida. Use o formato YYYY-MM-DD"}), 400
    
    #verifica se produto,quantidade,valor_vendido,status são numeros
    if not lead_id.isdigit() or not produto_id.isdigit() or not quantidade.isdigit() or not valor_vendido.replace('.','',1).isdigit() or not status.isdigit():
        return jsonify({"erro": "Lead ID, Produto ID, Quantidade, Valor Vendido e Status devem ser números"}), 400
    
    #Verifica se lead existe
    sql_check_lead = text("SELECT COUNT(*) FROM leads WHERE id_lead = :lead")
    result = db.session.execute(sql_check_lead, {"lead": lead_id})
    
    if result.fetchone()[0] == 0:
        return jsonify({"erro": "Lead não existe"}), 400

    # Verifica se produto existe
    sql_check_produto = text("SELECT COUNT(*) FROM produtos WHERE id_produto = :produto_id")
    result = db.session.execute(sql_check_produto, {"produto_id": produto_id})

    if result.fetchone()[0] == 0:
        return jsonify({"erro": "Produto não encontrado"}), 400
    
    # Verifica se status é válido
    sql_check_status = text("SELECT COUNT(*) FROM status WHERE id_status = :status_id")
    result = db.session.execute(sql_check_status, {"status_id": status})  
      
    if result.fetchone()[0] == 0:
        return jsonify({"erro": "Status inválido"}), 400
    
    #Verifica se quantidade é positiva
    quantidade = int(quantidade)
    if quantidade <= 0:
        return jsonify({"erro": "Quantidade deve ser um número positivo"}), 400

#verifica se valor_vendido é positivo
    valor_vendido = float(valor_vendido)
    if valor_vendido <= 0:
        return jsonify({"erro": "Valor vendido deve ser um número positivo"}), 400

    #SQL
    sql = text("""
        INSERT INTO ordem (
             lead_id,data_ordem, produto_id, quantidade, valor_vendido, status
        ) 
        VALUES (
             :lead_id, :data_ordem, :produto_id, :quantidade, :valor_vendido, :status
        ) 
        RETURNING id_ordem
        """)
    
    dados = {
        "lead_id": lead_id,
        "data_ordem": data_ordem,
        "produto_id": produto_id,
        "quantidade": quantidade,
        "valor_vendido": valor_vendido,
        "status": status
        } #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_ordem = result.fetchone()[0]
    dados['id_ordem'] = id_ordem


    return dados

#Selects
#ver produto/1
@ordem_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM ordem where id_ordem = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os produtos
@ordem_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM ordem ") #LIMIT 100 OFFSET 100 para paginação
    
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
@ordem_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    
    #dados que vieram   
    lead_id = request.form.get("lead")
    data_ordem = request.form.get("data_ordem")
    produto_id = request.form.get("produto_id")
    quantidade = request.form.get("quantidade").replace(',','.')
    valor_vendido = request.form.get("valor_vendido").replace(',','.')
    status = request.form.get("status")
    
    #Verificando quais campos foram enviados
    campos = []
    dados = {"id": id}
    
    if lead_id:
            campos.append("lead_id = :lead_id")
            dados["lead_id"] = lead_id

    if data_ordem:
        campos.append("data_ordem = :data_ordem")
        dados["data_ordem"] = data_ordem

    if produto_id:
        campos.append("produto_id = :produto_id")
        dados["produto_id"] = produto_id

    if quantidade:
        campos.append("quantidade = :quantidade")
        dados["quantidade"] = quantidade

    if valor_vendido:
        campos.append("valor_vendido = :valor_vendido")
        dados["valor_vendido"] = valor_vendido

    if status:
        campos.append("status = :status")
        dados["status"] = status

    if not campos:
        return "Nenhum dado para atualizar"
    
    #SQL
    sql_update = text("UPDATE ordem SET " + ", ".join(campos) + " WHERE id_ordem = :id")

    sql_select = text("SELECT * FROM ordem WHERE id_ordem = :id")
   
    try:
        
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()

        if not antes:
            return "Ordem não encontrado"

        
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
    "mensagem": f"Ordem com o id:{id} alterado",
    "dados_alterados": alterados,
    "Ordem_atualizada": dict(depois)
}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)})

#deletar/Destruir
#delete
@ordem_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM ordem WHERE id_ordem = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Ordem com o id:{id} removida"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)