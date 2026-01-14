from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conf.database import init_db




from control.usuario           import user_bp
from routes.auth               import auth_bp 
from control.leads             import lead_bp
from control.produtos          import product_bp
from control.fornecedor        import fornecedor_bp



app = Flask(__name__)


#Conexao Geral do meu app
init_db(app)




#Registro de controladores 
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(lead_bp)
app.register_blueprint(product_bp)
app.register_blueprint(fornecedor_bp)

if __name__ == "__main__":
    app.run(debug=True)



