from flask import Flask,Blueprint, request,jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho

from conf.database import db

marca_bp = Blueprint('marca',__name__,url_prefix= '/marca')


#CRUD
#Criar 
#insert - SQL
#http/web - POST
@marca_bp.route("/", methods=["POST"])
def criar():
    #dados que vieram
    nome = request.form.get("nome")
    pais = request.form.get("pais")


    #SQL
    sql = text("INSERT INTO marcas (nome_marca, pais_origem) VALUES (:nome, :pais) RETURNING id")
    dados = {"nome": nome, "pais": pais} #os dados do que veio lá da var sql


    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()


    #pega o id
    id = result.fetchone()[0]
    dados['id'] = id


    return dados

#Selects
#ver marca/1 
@marca_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM marcas where id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e

#verTodas as marcas
@marca_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM marcas ") #LIMIT 100 OFFSET 100 para paginação
    
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
@marca_bp.route("/<id>", methods=["PUT"])
def atualizar(id):
    #dados que vieram
    nome = request.form.get("nome")
    pais = request.form.get("pais")
    sql = text("UPDATE marcas set nome_marca = :nome, pais_origem = :pais WHERE id = :id")
    dados = {"nome": nome, "pais": pais, "id" : id} #os dados do que veio lá da var sql
    result = db.session.execute(sql,dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
        
    if linhas_afetadas == 1: 
            db.session.commit()
            return f"Marca com o id:{id} alterado"
    else:
            db.session.rollback()
            return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"


#deletar/Destruir
#delete
@marca_bp.route("/marca/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM marcas WHERE id = :id")
    dados = {"id": id}
    result = db.session.execute(sql,dados)


    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Marca com o id:{id} removida"
    else:
        db.session.rollback()
        return f"PRESTE ATENÇÃO, ALGO NÃO ESTÁ CORRETO!! SÓ DEUS NA CAUSA!!"
    

