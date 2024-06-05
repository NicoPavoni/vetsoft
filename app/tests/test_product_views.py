from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from app.models import Product


class ProductViewsTest(TestCase):
    """
    Clase de test de integracion que valida que el stock de un producto incremente y decremente.
    
    """
    def test_decrease_stock_view(self):
        # Creo un producto inicial con stock 1
        product = Product.objects.create(name="Test Product", type="Type A", price=10.0, stock=1)
        url = reverse('decrease_stock')
        
        # Enviar una solicitud POST para disminuir el stock
        response = self.client.post(url, {'product_id': product.id})
        
        # Verifico que el stock se haya disminuido 
        product.refresh_from_db()
        self.assertEqual(product.stock, 0)
        
        # Verifico que se haya generado el mensaje de producto sin stock
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Test Product:  Fuera de stock.")

    def test_increase_stock_view(self):
        # Creo un producto inicial con stock 0
        product = Product.objects.create(name="Test Product", type="Type A", price=10.0, stock=0)
        url = reverse('increase_stock')
        
        # Enviar una solicitud POST para aumentar el stock
        response = self.client.post(url, {'product_id': product.id})
        
        # Verifico que el stock se haya aumentado correctamente
        product.refresh_from_db()
        self.assertEqual(product.stock, 1)
        
        # Verifico que no haya mensajes de advertencia
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
