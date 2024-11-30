from datetime import datetime
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import unittest
import pytest
from api.models import db, Articulo, Categoria, Proveedor
from api.controllers import ArticuloResource, ArticulosResource, CategoriaResource, CategoriasResource, ProveedorResource, ProveedoresResource, TiposMovimientoResource, TipoMovimientoResource, HistorialDetalleResource, HistorialResource

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    api = Api(app)

    api.add_resource(ArticulosResource, '/api/articulos')
    api.add_resource(ArticuloResource, '/api/articulos/<int:articulo_id>')
    api.add_resource(CategoriasResource, '/api/categorias')
    api.add_resource(CategoriaResource, '/api/categorias/<int:categoria_id>')
    api.add_resource(ProveedoresResource, '/api/proveedores')
    api.add_resource(ProveedorResource, '/api/proveedores/<int:proveedor_id>')
    api.add_resource(HistorialResource, '/api/historial_inventario')
    api.add_resource(HistorialDetalleResource, '/api/historial_inventario/<int:historial_id>')
    api.add_resource(TiposMovimientoResource, '/api/tipos_movimiento')
    api.add_resource(TipoMovimientoResource, '/api/tipos_movimiento/<int:tipo_id>')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


# Pruebas para proveedores
# Crear un proveedor
def test_create_proveedor(client):
    response = client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 201
    assert response.get_json()['proveedor'] == 'Tech Supplier'

# Obtener todos los proveedores
def test_get_proveedores(client):
    response = client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    response = client.post('/api/proveedores', json={'proveedor': 'Global Electronics'})
    response = client.post('/api/proveedores', json={'proveedor': 'Best Supplies'})
    response = client.get('/api/proveedores')
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

#Eliminar proveedor
def test_delete_proveedor(client):
    response = client.post('/api/proveedores', json={'proveedor': 'Best Supplies'})
    proveedor_id = response.get_json()['id']
    print(f"Proveedor creado con ID: {proveedor_id}")

    delete_response = client.delete(f'/api/proveedores/{proveedor_id}')
    print(f"Status Code: {delete_response.status_code}")
    print(f"Delete Response: {delete_response.get_json()}")
    assert delete_response.status_code == 200
    assert client.get('/api/proveedores').get_json() == []  

# Pruebas para categorías
def test_create_categoria(client):
    response = client.post('/api/categorias', json={'categoria': 'Electrónica'})
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 201
    assert response.get_json()['categoria'] == 'Electrónica'

# Obtener todas las categorías
def test_get_categorias(client):
    response = client.post('/api/categorias', json={'categoria': 'Electrónica'})
    response = client.post('/api/categorias', json={'categoria': 'Hogar'})
    response = client.post('/api/categorias', json={'categoria': 'Ropa'})
    response = client.get('/api/categorias')
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# Eliminar una categorías
def test_get_categoria_no_existente(client):
    response = client.get('/api/categorias/999')
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Categoría no encontrada'

# Pruebas para artículos
# Crear un artículo
def test_create_articulo(client):
    client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    client.post('/api/categorias', json={'categoria': 'Electrónica'})
    
    response = client.post('/api/articulos', json={
        'nombre': 'Laptop ASUS',
        'descripcion': 'Laptop gaming',
        'categoria_id': 1,
        'proveedor_id': 1,
        'stock': 10,
        'precio': 1500.00
    })
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 201
    data = response.get_json()
    assert data['nombre'] == 'Laptop ASUS'

# Obtener todos los artículos
def test_get_articulos(client):
    client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    client.post('/api/categorias', json={'categoria': 'Electrónica'})
    
    response = client.post('/api/articulos', json={
        'nombre': 'Laptop ASUS',
        'descripcion': 'Laptop gaming',
        'categoria_id': 1,
        'proveedor_id': 1,
        'stock': 10,
        'precio': 1500.00
    })
    response = client.get('/api/articulos')
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# Obtener un artículo no existente
def test_get_articulo_no_existente(client):
    response = client.get('/api/articulos/999')
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Artículo no encontrado'

#Eliminar un artículo
def test_delete_articulo(client):
    # Primero crear un proveedor, categoría y artículo
    client.post('/api/proveedores', json={'proveedor': 'Best Supplier'})
    client.post('/api/categorias', json={'categoria': 'Accesorios'})
    response = client.post('/api/articulos', json={
        'nombre': 'Monitor Dell',
        'descripcion': 'Monitor 27 pulgadas',
        'categoria_id': 1,
        'proveedor_id': 1,
        'stock': 5,
        'precio': 300.00
    })
    articulo_id = response.get_json()['id']
    print(f"Artículo creado con ID: {articulo_id}")

    delete_response = client.delete(f'/api/articulos/{articulo_id}')
    print(f"Delete Response: {delete_response.get_json()}")
    assert delete_response.status_code == 200
    assert client.get('/api/articulos').get_json() == []  


# Pruebas para tipo de movimiento
# Crear un tipo de movimiento ("Ingreso" o "Egreso")
def test_create_tipo_movimiento(client):
    response = client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 201
    assert response.get_json()['tipo'] == 'Ingreso'

# Obtener todos los tipos de movimientos
def test_get_tipos_movimiento(client):
    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    client.post('/api/tipos_movimiento', json={'tipo': 'Egreso'})
    
    response = client.get('/api/tipos_movimiento')
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# Consultar un tipo de movimiento no existente
def test_get_tipo_movimiento_no_existente(client):
    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    response = client.get('/api/tipos_movimiento/999')
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Tipo de movimiento no encontrado'

#Eliminar un tipo de movimiento
def test_delete_tipo_movimiento(client):
    response = client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    tipo_id = response.get_json()['id']
    print(f"Tipo de movimiento creado con ID: {tipo_id}")

    delete_response = client.delete(f'/api/tipos_movimiento/{tipo_id}')
    print(f"Delete Response: {delete_response.get_json()}")
    assert delete_response.status_code == 200
    assert client.get('/api/tipos_movimiento').get_json() == []  


# Pruebas para historial de inventario

#Crear un historial de inventario con tipo de movimiento de ingreso
def test_ingreso_stock(client):
    client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    client.post('/api/categorias', json={'categoria': 'Electrónica'})
    response = client.post('/api/articulos', json={
        'nombre': 'Laptop ASUS',
        'descripcion': 'Laptop gaming',
        'categoria_id': 1,
        'proveedor_id': 1,
        'stock': 10,
        'precio': 1500.00
    })
    articulo_id = response.get_json()['id']
    print(f"Artículo creado con ID: {articulo_id}")

    articulo_before = client.get(f'/api/articulos/{articulo_id}').get_json()
    print(f"Articulo antes del ingreso: {articulo_before}")

    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})

    response = client.post('/api/historial_inventario', json={
        'articulo_id': articulo_id,
        'tipo_movimiento_id': 1, 
        'cantidad': 5,
        'fecha_movimiento': datetime.now().isoformat()
    })
    print(f"Ingreso realizado: {response.get_json()}")

    articulo = client.get(f'/api/articulos/{articulo_id}').get_json()
    print(f"Stock después del ingreso: {articulo['stock']}")
    assert articulo['stock'] == 15 

#Crear un historial de inventario con tipo de movimiento de egreso
def test_egreso_stock(client):
    client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    client.post('/api/categorias', json={'categoria': 'Electrónica'})
    response = client.post('/api/articulos', json={
        'nombre': 'Laptop ASUS',
        'descripcion': 'Laptop gaming',
        'categoria_id': 1,
        'proveedor_id': 1,
        'stock': 10,
        'precio': 1500.00
    })
    articulo_id = response.get_json()['id']
    print(f"Artículo creado con ID: {articulo_id}")

    articulo_after = client.get(f'/api/articulos/{articulo_id}').get_json()
    print(f"Articulo antes del egreso: {articulo_after}")

    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    client.post('/api/tipos_movimiento', json={'tipo': 'Egreso'})

    response = client.post('/api/historial_inventario', json={
        'articulo_id': articulo_id,
        'tipo_movimiento_id': 2,  
        'cantidad': 3,
        'fecha_movimiento': datetime.now().isoformat()
    })
    print(f"Egreso realizado: {response.get_json()}")

    articulo = client.get(f'/api/articulos/{articulo_id}').get_json()
    print(f"Stock después del egreso: {articulo['stock']}")
    assert articulo['stock'] == 7  


#Obtener todos los historiales de inventario
def test_get_historial_inventario(client):
    client.post('/api/proveedores', json={'proveedor': 'Tech Supplier'})
    client.post('/api/categorias', json={'categoria': 'Electrónica'})
    client.post('/api/articulos', json={'nombre': 'Laptop ASUS', 'descripcion': 'Laptop gaming', 'categoria_id': 1, 'proveedor_id': 1, 'stock': 10, 'precio': 1500.00})
    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    client.post('/api/historial_inventario', json={'id_producto': 1, 'tipo_movimiento_id': 1, 'cantidad': 5})
    
    response = client.get('/api/historial_inventario')
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

#Consultar un historial de inventario no existente
def test_get_historial_inventario_no_existente(client):
    client.post('/api/articulos', json={'nombre': 'Laptop Acer', 'descripcion': 'Laptop ideal para trabajo', 'categoria_id': 1, 'proveedor_id': 1, 'stock': 65, 'precio': 5600.00})
    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    client.post('/api/historial_inventario', json={'id_producto': 1, 'tipo_movimiento_id': 1, 'cantidad': 5})
    response = client.get('/api/historial_inventario/999')
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Historial no encontrado'

#Eliminar un historial de inventario
def test_delete_historial_inventario(client):
    client.post('/api/articulos', json={'nombre': 'Laptop ASUS', 'descripcion': 'Laptop gaming', 'categoria_id': 1, 'proveedor_id': 1, 'stock': 10, 'precio': 1500.00})
    client.post('/api/tipos_movimiento', json={'tipo': 'Ingreso'})
    response = client.post('/api/historial_inventario', json={'articulo_id': 1, 'tipo_movimiento_id': 1, 'cantidad': 5, 'fecha': '2024-11-27'})
    historial_id = response.get_json()['id']
    print(f"Historial creado con ID: {historial_id}")

    delete_response = client.delete(f'/api/historial_inventario/{historial_id}')
    print(f"Delete Response: {delete_response.get_json()}")
    assert delete_response.status_code == 200
    assert client.get('/api/historial_inventario').get_json() == [] 
