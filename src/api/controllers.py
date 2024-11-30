import datetime
from flask import Response, json
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from api.models import db, Articulo, Categoria, Proveedor,TipoMovimiento,HistorialInventario  

articulo_args = reqparse.RequestParser()
articulo_args.add_argument("nombre", type=str, required=True, help="El nombre del artículo es obligatorio")
articulo_args.add_argument("descripcion", type=str)
articulo_args.add_argument("categoria_id", type=int, required=True, help="La categoría es obligatoria")
articulo_args.add_argument("proveedor_id", type=int, required=True, help="El proveedor es obligatorio")
articulo_args.add_argument("stock", type=int, required=True, help="El stock es obligatorio")
articulo_args.add_argument("precio", type=float, required=True, help="El precio es obligatorio")

articulo_fields = {
    "id": fields.Integer,
    "nombre": fields.String,
    "descripcion": fields.String,
    "categoria_id": fields.Integer,
    "proveedor_id": fields.Integer,
    "stock": fields.Integer,
    "precio": fields.Float
}

class ArticulosResource(Resource):
    @marshal_with(articulo_fields)
    def post(self):
        args = articulo_args.parse_args()
        nuevo_articulo = Articulo(  
            nombre=args["nombre"],
            descripcion=args["descripcion"],
            categoria_id=args["categoria_id"],
            proveedor_id=args["proveedor_id"],
            stock=args["stock"],
            precio=args["precio"]
        )
        db.session.add(nuevo_articulo)
        db.session.commit()
        return nuevo_articulo, 201
    
    @marshal_with(articulo_fields)
    def get(self):
        articulos = Articulo.query.all()  
        return articulos

class ArticuloResource(Resource):
    @marshal_with(articulo_fields)
    def get(self, articulo_id):
        articulo = Articulo.query.filter_by(id=articulo_id).first()  
        if not articulo:
            abort(404, message="Artículo no encontrado")
        return articulo, 200
    
    @marshal_with(articulo_fields)
    def patch(self, articulo_id):
        args = articulo_args.parse_args()
        articulo = Articulo.query.filter_by(id=articulo_id).first()  
        if not articulo:
            abort(404, message="Artículo no encontrado")
        articulo.nombre = args["nombre"]
        articulo.descripcion = args["descripcion"]
        articulo.categoria_id = args["categoria_id"]
        articulo.proveedor_id = args["proveedor_id"]
        articulo.stock = args["stock"]
        articulo.precio = args["precio"]
        db.session.commit()
        return articulo, 200
    
    @marshal_with(articulo_fields)
    def delete(self, articulo_id):
        articulo = Articulo.query.filter_by(id=articulo_id).first()  
        if not articulo:
            abort(404, message="Artículo no encontrado")
        db.session.delete(articulo)
        db.session.commit()
        return {"message": "Artículo eliminado"}, 200


categoria_args = reqparse.RequestParser()
categoria_args.add_argument("categoria", type=str, required=True, help="El nombre de la categoría es obligatorio")


categoria_fields = {
    "id": fields.Integer,
    "categoria": fields.String
}


class CategoriasResource(Resource):
    @marshal_with(categoria_fields)
    def post(self):
        args = categoria_args.parse_args()
        nueva_categoria = Categoria(categoria=args["categoria"])  
        db.session.add(nueva_categoria)
        db.session.commit()
        return nueva_categoria, 201
    
    @marshal_with(categoria_fields)
    def get(self):
        categorias = Categoria.query.all() 
        return categorias

class CategoriaResource(Resource):
    @marshal_with(categoria_fields)
    def get(self, categoria_id):
        categoria = Categoria.query.filter_by(id=categoria_id).first()  
        if not categoria:
            abort(404, message="Categoría no encontrada")
        return categoria, 200
    
    @marshal_with(categoria_fields)
    def patch(self, categoria_id):
        args = categoria_args.parse_args()
        categoria = Categoria.query.filter_by(id=categoria_id).first()  
        if not categoria:
            abort(404, message="Categoría no encontrada")
        categoria.categoria = args["categoria"]
        db.session.commit()
        return categoria, 200
    
    @marshal_with(categoria_fields)
    def delete(self, categoria_id):
        categoria = Categoria.query.filter_by(id=categoria_id).first()  
        if not categoria:
            abort(404, message="Categoría no encontrada")
        db.session.delete(categoria)
        db.session.commit()
        return {"message": "Categoría eliminada"}, 200


proveedor_args = reqparse.RequestParser()
proveedor_args.add_argument("proveedor", type=str, required=True, help="El nombre del proveedor es obligatorio")


proveedor_fields = {
    "id": fields.Integer,
    "proveedor": fields.String
}


class ProveedoresResource(Resource):
    @marshal_with(proveedor_fields)
    def post(self):
        args = proveedor_args.parse_args()
        nuevo_proveedor = Proveedor(proveedor=args["proveedor"])  
        db.session.add(nuevo_proveedor)
        db.session.commit()
        return nuevo_proveedor, 201
    
    @marshal_with(proveedor_fields)
    def get(self):
        proveedores = Proveedor.query.all()  
        return proveedores

class ProveedorResource(Resource):
    @marshal_with(proveedor_fields)
    def get(self, proveedor_id):
        proveedor = Proveedor.query.filter_by(id=proveedor_id).first() 
        if not proveedor:
            abort(404, message="Proveedor no encontrado")
        return proveedor, 200
    
    @marshal_with(proveedor_fields)
    def patch(self, proveedor_id):
        args = proveedor_args.parse_args()
        proveedor = Proveedor.query.filter_by(id=proveedor_id).first()  
        if not proveedor:
            abort(404, message="Proveedor no encontrado")
        proveedor.proveedor = args["proveedor"]
        db.session.commit()
        return proveedor, 200
    
    @marshal_with(proveedor_fields)
    def delete(self, proveedor_id):
        proveedor = Proveedor.query.filter_by(id=proveedor_id).first()  
        if not proveedor:
            abort(404, message="Proveedor no encontrado")
        db.session.delete(proveedor)
        db.session.commit()
        return {"message": "Proveedor eliminado"}, 200



tipo_movimiento_args = reqparse.RequestParser()
tipo_movimiento_args.add_argument("tipo", type=str, required=True, help="El tipo de movimiento es obligatorio")


tipo_movimiento_fields = {
    "id": fields.Integer,
    "tipo": fields.String
}


class TiposMovimientoResource(Resource):
    @marshal_with(tipo_movimiento_fields)
    def post(self):
        args = tipo_movimiento_args.parse_args()
        nuevo_tipo = TipoMovimiento(tipo=args["tipo"])
        db.session.add(nuevo_tipo)
        db.session.commit()
        return nuevo_tipo, 201
    
    @marshal_with(tipo_movimiento_fields)
    def get(self):
        tipos = TipoMovimiento.query.all()
        return tipos

class TipoMovimientoResource(Resource):
    @marshal_with(tipo_movimiento_fields)
    def get(self, tipo_id):
        tipo = TipoMovimiento.query.filter_by(id=tipo_id).first()
        if not tipo:
            abort(404, message="Tipo de movimiento no encontrado")
        return tipo, 200
    
    @marshal_with(tipo_movimiento_fields)
    def patch(self, tipo_id):
        args = tipo_movimiento_args.parse_args()
        tipo = TipoMovimiento.query.filter_by(id=tipo_id).first()
        if not tipo:
            abort(404, message="Tipo de movimiento no encontrado")
        tipo.tipo = args["tipo"]
        db.session.commit()
        return tipo, 200
    
    @marshal_with(tipo_movimiento_fields)
    def delete(self, tipo_id):
        tipo = TipoMovimiento.query.filter_by(id=tipo_id).first()
        if not tipo:
            abort(404, message="Tipo de movimiento no encontrado")
        db.session.delete(tipo)
        db.session.commit()
        return {"message": "Tipo de movimiento eliminado"}, 200
    


historial_inventario_args = reqparse.RequestParser()
historial_inventario_args.add_argument("articulo_id", type=int, required=True, help="El ID del artículo es obligatorio")
historial_inventario_args.add_argument("tipo_movimiento_id", type=int, required=True, help="El tipo de movimiento es obligatorio")
historial_inventario_args.add_argument("cantidad", type=int, required=True, help="La cantidad es obligatoria")


historial_inventario_fields = {
    "id": fields.Integer,
    "articulo_id": fields.Integer,
    "tipo_movimiento_id": fields.Integer,
    "cantidad": fields.Integer,
    "fecha_movimiento": fields.DateTime  
}


class HistorialResource(Resource):
    @marshal_with(historial_inventario_fields)  
    def post(self):
        args = historial_inventario_args.parse_args()


        articulo = Articulo.query.filter_by(id=args["articulo_id"]).first()
        tipo_movimiento = TipoMovimiento.query.filter_by(id=args["tipo_movimiento_id"]).first()


        if not articulo:
            abort(404, message="Artículo no encontrado")
        if not tipo_movimiento:
            abort(404, message="Tipo de movimiento no encontrado")

        nuevo_historial = HistorialInventario(
            articulo_id=args["articulo_id"],
            tipo_movimiento_id=args["tipo_movimiento_id"],
            cantidad=args["cantidad"],
            fecha_movimiento=datetime.datetime.now()  
        )


        if tipo_movimiento.tipo == "Ingreso":
            articulo.stock += args["cantidad"]  
        elif tipo_movimiento.tipo == "Egreso":
            if articulo.stock >= args["cantidad"]:
                articulo.stock -= args["cantidad"]  
            else:
                abort(400, message="No hay suficiente stock para realizar el egreso")


        db.session.add(nuevo_historial)
        db.session.commit()

        return nuevo_historial, 201

    @marshal_with(historial_inventario_fields)  
    def get(self):
        historial = HistorialInventario.query.all()  
        return historial

class HistorialDetalleResource(Resource):
    @marshal_with(historial_inventario_fields) 
    def get(self, historial_id):
        historial = HistorialInventario.query.filter_by(id=historial_id).first()
        if not historial:
            abort(404, message="Historial no encontrado")
        return historial, 200
    
    @marshal_with(historial_inventario_fields) 
    def delete(self, historial_id):
        historial = HistorialInventario.query.filter_by(id=historial_id).first()
        if not historial:
            abort(404, message="Registro de historial no encontrado")
        db.session.delete(historial)
        db.session.commit()
        return {"message": "Registro de historial eliminado"}, 200


