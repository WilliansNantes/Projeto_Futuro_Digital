import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para o ambiente do sistema
load_dotenv()

db = SQLAlchemy()


def init_db(app):
    #Procura a variável de ambiente DATABASE_URL, se não encontrar, usa o valor padrão(opcional)
    database_url = os.getenv('DATABASE_URL')
    
    
    if not database_url:
        raise ValueError("A variável de ambiente 'DATABASE_URL' não foi encontrada. Por favor, defina-a no arquivo .env.")
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    #É boa prática desativar o recurso de rastreamento de modificações do SQLAlchemy, pois ele pode consumir recursos desnecessários
    app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
