from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from api.models import db, Articulo, Categoria, Proveedor,TipoMovimiento,HistorialInventario 
from api.controllers import ArticuloResource, ArticulosResource, CategoriaResource, CategoriasResource, ProveedorResource, ProveedoresResource, TiposMovimientoResource, TipoMovimientoResource, HistorialDetalleResource, HistorialResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()


# --- Rutas ---
api.add_resource(ArticulosResource, '/api/articulos')
api.add_resource(ArticuloResource, '/api/articulos/<int:articulo_id>')
api.add_resource(CategoriasResource, '/api/categorias')
api.add_resource(CategoriaResource, '/api/categorias/<int:categoria_id>')
api.add_resource(ProveedoresResource, '/api/proveedores')
api.add_resource(ProveedorResource, '/api/proveedores/<int:proveedor_id>')
api.add_resource(HistorialResource, '/api/historial_inventario')
api.add_resource(HistorialDetalleResource, '/api/historial_inventario/<int:historial_id>')
api.add_resource(TiposMovimientoResource, '/api/tipos_movimiento')
api.add_resource(TipoMovimientoResource, '/api/tipos_movimiento/<int:tipo_movimiento_id>')

@app.route('/')
def hello():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)
