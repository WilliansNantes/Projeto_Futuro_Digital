from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conf.database import init_db




from control.marcas         import marca_bp
from control.produtos       import produto_bp
from control.pedidos        import pedido_bp
from control.clientes       import cliente_bp
from control.itens_compra   import itens_compra_bp






app = Flask(__name__)


#Conexao Geral do meu app
init_db(app)




#Registro de controladores 
app.register_blueprint(marca_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(itens_compra_bp)




if __name__ == "__main__":
    app.run(debug=True)



