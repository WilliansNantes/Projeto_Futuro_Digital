from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db


status_bp = Blueprint('status',__name__,url_prefix='/status')



#CRUD
#Criar 
#insert - SQL
#http/web - POST
@status_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    situacao = request.form.get("situação")
    score_min = request.form.get("score_min")
    score_max = request.form.get("score_max")
    
     # Validação
    if not all([situacao, score_min,score_max]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400


    #SQL
    sql = text("""
        INSERT INTO status (
             situação, score_min, score_max 
        ) 
        VALUES (
            :situacao, :score_min, :score_max 
        ) 
        RETURNING id_status
        """)
    
    dados = {
        "situacao": situacao, 
        "score_min": score_min, 
        "score_max": score_max, 
        } #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id_status = result.fetchone()[0]
    dados['id_status'] = id_status


    return dados

#Selects
#ver usuário/1
@status_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM status where id_status = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os usuarios
@status_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM status ") #LIMIT 100 OFFSET 100 para paginação
    
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
@status_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    
    #dados que vieram   
    situacao = request.form.get("situação")
    score_min = request.form.get("score_min")
    score_max = request.form.get("score_max")
    
    #Verificando quais campos foram enviados
    campos = []
    dados = {"id": id}
    
    if situacao:
            campos.append("situação = :situacao")
            dados["situacao"] = situacao

    if score_min:
        campos.append("score_min = :score_min")
        dados["score_min"] = score_min

    if score_max:
        campos.append("score_max = :score_max")
        dados["score_max"] = score_max

    if not campos:
        return "Nenhum dado para atualizar"
    
    #SQL
    sql_update = text("UPDATE status SET " + ", ".join(campos) + " WHERE id_status = :id")

    sql_select = text("SELECT * FROM status WHERE id_status = :id")
   

    try:
        #DADOS ANTES
        antes = db.session.execute(sql_select, {"id": id}).mappings().first()

        if not antes:
            return f"Status não encontrado", 400

        #EXECUTA UPDATE
        result = db.session.execute(sql_update, dados)
        #conta quantas linhas foram afetadas
        linhas_afetadas = result.rowcount  

        if linhas_afetadas == 1:
            db.session.commit()

            #DADOS DEPOIS
            depois = db.session.execute(sql_select, {"id": id}).mappings().first()

            return {
                "msg": f"Status com id {id} atualizado com sucesso",
                "antes": dict(antes),
                "depois": dict(depois)
            }
        else:
            db.session.rollback()
            return {"msg": "ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"}, 400

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}


#deletar/Destruir
#delete
@status_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM status WHERE id_status = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Status com o id:{id} removida"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)
