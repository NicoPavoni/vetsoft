from django.test import TestCase

from app.models import Client


class ClientNumberOnlyTest(TestCase):
    """
    Test de unidad para verificar que el numero de telefono del cliente sean, efectivamente, solo numeros y no contenga letras.
    """

    def test_create_client(self):
        client = Client.objects.create(name="Client A", phone="aaaaa", email="testMail@vetsoft.com", address="1 y 57")
        self.assertEqual(client.name, "Client A")
        self.assertFalse(client.phone.isdigit())
        self.assertEqual(client.email, "testMail@vetsoft.com")
        self.assertEqual(client.address, "1 y 57")