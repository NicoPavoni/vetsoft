from django.test import TestCase

from app.models import Medicine


class MedicineDoseTest(TestCase):
    """
    Clase de test de dosis de medicina para las mascotas.

    Atributos:
        valores para realizar el test que estan almacenados en la instancia de la clase.
    """

    #Se agrega una nueva medicina con dosis 0 para verificar que se cumpla la condición de minimo 1
    def test_create_medicine_below(self):
        medicine = Medicine.objects.create(name="Medicine test 1", description="Medicine A", dose=0)
        self.assertEqual(medicine.name, "Medicine test 1")
        self.assertEqual(medicine.description, "Medicine A")
        self.assertFalse(medicine.dose)

    #Se agrega una nueva medicina con dosis 12 para verificar que se cumpla la condición de maximo 10
    def test_create_medicine_above(self):
        medicine = Medicine.objects.create(name="Medicine test 2", description="Medicine B", dose=12)
        self.assertEqual(medicine.name, "Medicine test 2")
        self.assertEqual(medicine.description, "Medicine B")
        self.assertGreater(medicine.dose, 10)