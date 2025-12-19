from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conf.database import init_db




from control.user           import user_bp
from routes.auth            import auth_bp 






app = Flask(__name__)


#Conexao Geral do meu app
init_db(app)




#Registro de controladores 
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)




if __name__ == "__main__":
    app.run(debug=True)



