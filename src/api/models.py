import datetime
from .extensions import db
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Articulo(db.Model):
    __tablename__ = 'articulos' 
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    

    categoria = db.relationship('Categoria', back_populates='articulos')
    proveedor = db.relationship('Proveedor', back_populates='articulos')
    historial = db.relationship('HistorialInventario', back_populates='articulo', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Articulo (nombre={self.nombre}, precio={self.precio})>"

class Categoria(db.Model):
    __tablename__ = 'categorias'  
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    categoria = db.Column(db.String(80), unique=True, nullable=False)
    

    articulos = db.relationship('Articulo', back_populates='categoria')

    def __repr__(self):
        return f"<Categoria (nombre={self.categoria})>"

class Proveedor(db.Model):
    __tablename__ = 'proveedores'  
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    proveedor = db.Column(db.String(80), unique=True, nullable=False)
    

    articulos = db.relationship('Articulo', back_populates='proveedor')

    def __repr__(self):
        return f"<Proveedor (nombre={self.proveedor})>"

class TipoMovimiento(db.Model):
    __tablename__ = 'tipos_movimiento'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    tipo = db.Column(db.String(20), unique=True, nullable=False)  # 'Ingreso', 'Egreso'


    historial = db.relationship('HistorialInventario', back_populates='tipo_movimiento')

    def __repr__(self):
        return f"<TipoMovimiento (nombre={self.tipo})>"

class HistorialInventario(db.Model):
    __tablename__ = 'historial_inventario'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    articulo_id = db.Column(db.Integer, db.ForeignKey('articulos.id'), nullable=False)  
    tipo_movimiento_id = db.Column(db.Integer, db.ForeignKey('tipos_movimiento.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_movimiento = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False) 


    articulo = db.relationship('Articulo', back_populates='historial')
    tipo_movimiento = db.relationship('TipoMovimiento', back_populates='historial')

    def __repr__(self):

        return f"<HistorialInventario (articulo_id={self.articulo_id}, tipo_movimiento={self.tipo_movimiento.tipo}, cantidad={self.cantidad})>"