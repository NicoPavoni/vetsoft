from django.shortcuts import reverse
from django.test import TestCase


class ProductTest(TestCase):

    """
    Clase de test de unidad que valida que el precio de un producto sea mayor a 0.
    
    """
    def test_precio_menor(self):
            response = self.client.post(
                reverse("products_form"),
                data={
                    "name": "Producto 1",
                    "type": "Tipo 1",
                    "price": "-15",
                    "stock": "5",
                },
            )

            self.assertContains(response, "El precio no puede ser negativo")

    def test_precio_cero(self):
            response = self.client.post(
                reverse("products_form"),
                data={
                    "name": "Producto 2",
                    "type": "Tipo 2",
                    "price": "1A5",
                    "stock": "10",
                },
            )

            self.assertContains(response, "El precio debe ser un número valido")