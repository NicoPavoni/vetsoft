from django.shortcuts import reverse
from django.test import TestCase


class ClientTest(TestCase):
    """
    Clase de test de integracion para recibir mediante un post la advertencia de que el telefono deben ser solo numeros.

    """

    def test_client_phone_number_only(self):
            response = self.client.post(
                reverse("clients_form"),
                data={
                    "name": "Juan Perez",
                    "phone": "aaaaa",
                    "email": "mail@vetsoft.com",
                    "address": "1 y 57",
                },
            )

            self.assertContains(response, " El teléfono sólo puede contener números")