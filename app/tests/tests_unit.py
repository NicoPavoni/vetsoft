import re

from django.test import TestCase

from app.models import Client


class ClientModelTest(TestCase):
    """
    Clase de tests de unidad para el modelo de cliente en la creacion y update.
    """
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({
            "name":"Juan Sebastian Veron",
            "phone": "54221555233",
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")

    def test_cant_create_a_client_with_numbers_in_name (self):
        response = Client.save_client(
            {
                "name": "Juan Sebastian Veron777",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        self.assertTrue(re.match("^[a-zA-ZÁÉÍÓÚáéíóúüÜ\s]+$", response[1]['name']), "El nombre solo debe contener letras y espacios")

    def test_cant_create_a_client_with_letters_in_phone (self):
        response = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "542215552qdsfghj",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        self.assertFalse(re.match("^[0-9]+$", response[1]['phone']), "El teléfono sólo puede contener números")
