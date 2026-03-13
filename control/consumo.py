from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
from funcao._perse_decimal     import _parse_decimal
import re

from conf.database import db


consumo_bp = Blueprint('consumo',__name__,url_prefix='/consumo')



#SAVE/UPSert
#http/web - POST
@consumo_bp.route("/insert", methods=["POST"])
def criar():
    
    #dados que vieram
    ano = request.form.get("ano")
    mes = request.form.get("mes")
    valor_kwh_consumo = request.form.get("valor_consumo")
    pessoa_id = request.form.get("pessoa_id")    
    
    campos = []
    dados = {}
    
    # Validação do ano 
    if ano:
        try:
                ano = int(ano)
        except ValueError:
                return jsonify({"erro": "Ano deve ser um número inteiro"}), 400
    
    campos.append("ano")
    dados["ano"] = ano
    
    # Validação do mes 
    if mes:
        try:
                mes = int(mes)
        except ValueError:
                return jsonify({"erro": "Mes deve ser um número inteiro"}), 400
    
    campos.append("mes")
    dados["mes"] = mes
    
    # Validação  de pessoa 
    try:
        pessoa_id = int(pessoa_id)
    except (ValueError, TypeError):
        return jsonify({"erro": "Pessoa ID deve ser um número inteiro"}), 400

    sql_check_pessoa = text("""
        SELECT COUNT(*)
        FROM pessoas
        WHERE id_pessoa = :pessoa_id
    """)

    pessoa_existe = db.session.execute(
        sql_check_pessoa,
        {"pessoa_id": pessoa_id}
    ).scalar()

    if pessoa_existe == 0:
        return jsonify({"erro": "id_pessoa não existe"}), 400

    campos.append("pessoa_id")
    dados["pessoa_id"] = pessoa_id

        
    # Validação do valor de consumo
    if valor_kwh_consumo:
        try:
            valor_kwh_consumo = _parse_decimal(valor_kwh_consumo)
        except ValueError:
            return jsonify({"erro": "Valor de consumo deve ser um número decimal"}), 400
        
    campos.append("valor_consumo")
    dados["valor_consumo"] = valor_kwh_consumo
    
    # UPSERT (UPDATE OU INSERT)
    sql_check = text("""
        SELECT COUNT(*)
        FROM consumo
        WHERE pessoa_id = :pessoa_id
        AND ano = :ano
        AND mes = :mes
    """)

    existe = db.session.execute(sql_check, dados).scalar()


    # UPDATE
    if existe > 0:

        sql_update = text("""
            UPDATE consumo
            SET valor_consumo = :valor_consumo
            WHERE pessoa_id = :pessoa_id
            AND ano = :ano
            AND mes = :mes
        """)

        db.session.execute(sql_update, dados)

        mensagem = "Consumo atualizado com sucesso"


    # INSERT
    else:

        cols = ", ".join(campos)
        placeholders = ", :".join(campos)

        sql_insert = text(f"""
            INSERT INTO consumo ({cols})
            VALUES (:{placeholders})
        """)

        db.session.execute(sql_insert, dados)

        mensagem = "Consumo inserido com sucesso"


    db.session.commit()

    return jsonify({"mensagem": mensagem, "consumo": valor_kwh_consumo}), 201

    #Selects
#ver usuário/1
@consumo_bp.route('/<id>')
def get_one(id):
    sql = text("SELECT * FROM consumo where id_consumo = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e
    
#verTodos os usuarios
@consumo_bp.route('/all')
def get_all():
    sql_query = text("SELECT * FROM consumo ") 
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambiara pq cada linha é um objeto


        print(json)


        return json
    
    except Exception as e:
        return str(e)
    
@consumo_bp.route("/<id>", methods=['DELETE'])
def delete(id):
    sql = text("DELETE FROM consumo WHERE id_consumo = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql,dados)
        linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
        if linhas_afetadas == 1: 
            db.session.commit()
            return f"Consumo com o id:{id} removido com sucesso!!"
        else:
            db.session.rollback()
            return f"ATENÇÃO, ALGO NÃO ESTÁ CORRETO!!"
   
    except Exception as e:
         return str(e)
     
     #Calculando a média de consumo e valor pago
    valores = []
    sql_media = text("""
        SELECT valor_consumo
        FROM consumo
        WHERE pessoa_id = :id_pessoa
        ORDER BY ano DESC, mes DESC
        LIMIT 3
    """)
    result = db.session.execute(sql_media, {"id_pessoa": id_pessoa})
    valores = [row[0] for row in result.fetchall()]
    
    
    quantidade_valores = len(valores)
    if quantidade_valores == 3:
        media_kwh_mes = sum(valores) / 3
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
    elif quantidade_valores == 2:
        media_kwh_mes = sum(valores) / 2
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
    elif quantidade_valores == 1:    
        media_kwh_mes = valores[0]
        media_pago_mes = media_kwh_mes * 1.41  # tarifa fixa
        
    else: 
        media_kwh_mes = None
        media_pago_mes = None
        
        campos.append("media_kwh_mes")
        dados["media_kwh_mes"] = media_cons_mes
    
    # BÔNUS DE SCORE 
    if media_pago_mes is not None:
        if 500 <= media_pago_mes < 720:
            score += 50
        elif media_pago_mes >= 720:
            score += 100
            
            campos.append("score")
            dados["score"] = score