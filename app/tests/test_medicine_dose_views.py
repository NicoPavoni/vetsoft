from django.shortcuts import reverse
from django.test import TestCase


class MedicineTest(TestCase):
    """
    Clase de test de integracion para recibir mediante un post la dosis de medicina para las mascotas.

    """

    def test_dose_below_one(self):
            response = self.client.post(
                reverse("medicines_form"),
                data={
                    "name": "Medicina 1",
                    "description": "Descripcion de medicina 1",
                    "dose": "0",
                },
            )

            self.assertContains(response, "La dosis debe ser entre 1 y 10")

    def test_dose_above_ten(self):
            response = self.client.post(
                reverse("medicines_form"),
                data={
                    "name": "Medicina 2",
                    "description": "Descripcion de medicina 2",
                    "dose": "12",
                },
            )

            self.assertContains(response, "La dosis debe ser entre 1 y 10")