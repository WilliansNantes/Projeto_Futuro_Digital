from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho


from conf.database import db


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


#Verificando login
#http/web - POST
@auth_bp.route('/login', methods=['POST'])
def login():
    
    #dados que vieram
    email = request.form.get("email")
    password = request.form.get("password")
    
    #SQL
    sql = text("SELECT * FROM usuario WHERE email = :email AND password = :password")
    dados = {"email": email, "password": password} #os dados do que veio lá da var sql
    try:
        result = db.session.execute(sql, dados)
        usuario = result.mappings().first()

        if usuario:
            return jsonify({
                "success": True,
                "usuario": {
                    "id": usuario["id_user"],
                    "name": usuario["nome_user"],
                    "função": usuario["funcao"]
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Email ou senha inválidos"
            }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500   
    
   