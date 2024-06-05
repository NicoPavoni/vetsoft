from django.test import TestCase

from app.models import Product


class ProductPrecioTest(TestCase):
    """
    Clase de test de unidad que valida que el precio de un producto sea mayor que 0.
    
    """
    def test_create_product(self):
        product = Product.objects.create(name="Producto_Test", type="Tipo 1", price=15, stock=50)
        self.assertEqual(product.name, "Producto_Test")
        self.assertEqual(product.type, "Tipo 1")
        self.assertEqual(product.price, 15)
        self.assertEqual(product.stock, 50)

    def test_validate_precioMayor (self):
        precio_producto = 30
        product = Product.objects.create(name="Producto_Test", type="Tipo 1", price=precio_producto, stock=50)
        self.assertEqual(product.name, "Producto_Test")
        self.assertEqual(product.type, "Tipo 1")
        self.assertEqual(product.price, precio_producto)
        self.assertEqual(product.stock, 50)
        self.assertTrue(product.price > 0, "El precio del producto debe ser mayor a 0")

    def test_validate_precioMenor(self):
        precio_producto = -30
        product = Product.objects.create(name="Producto_Test", type="Tipo 1", price= precio_producto, stock=50)
        self.assertEqual(product.name, "Producto_Test")
        self.assertEqual(product.type, "Tipo 1")
        self.assertEqual(product.price, precio_producto)
        self.assertEqual(product.stock, 50)
        self.assertTrue(product.price < 0, "El precio del producto no debe ser negativo")