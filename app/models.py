from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


def validate_client(data):
    """
    Valida los datos del cliente.

    Args:
        data: Diccionario con los datos del cliente.

    Returns:
        dict: Un diccionario con errores de validación si los hay.
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not phone.isnumeric():
        errors["phone"] = "El teléfono sólo puede contener números"
    
    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_pet(data):
    """
    Valida los datos de la mascota.

    Args:
        data: Diccionario con los datos de la mascota.

    Returns:
        dict: Un diccionario con errores de validación si los hay.
    """
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese la raza"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha"
    elif datetime.strptime(birthday, "%Y-%m-%d").date() > datetime.now().date():
        errors["birthday"] = "La fecha de cumpleaños no puede ser mayor al dia actual"

    return errors


class Client(models.Model):
    """
    Clase de cliente: almacena un valor y permite recuperarlo.

    Atributos:
        valor: está almacenado en la instancia de la clase.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()

def validate_medicines(data):
        """
        Valida los datos de la medicina.

        Args:
            data: Diccionario con los datos de la medicina.

        Returns:
            dict: Un diccionario con errores de validación si los hay.
        """
        errors = {}
        name = data.get("name", "")
        description = data.get("description", "")
        dose = data.get("dose", "")

        if name == "":
            errors["name"] = "Por favor, ingrese un nombre para la medicina"

        if description == "":
            errors["description"] = "Por favor, ingrese una descripcion"
        
        if dose == "":
            errors["dose"] = "Por favor, ingrese una dosis para la medicina"
        try:
            dose = int(dose)
            if (dose < 1) or (dose > 10):
                errors["dose"] = "La dosis debe ser entre 1 y 10"
        except ValueError:
            errors["dose"] = "La dosis debe ser un número entero"

        return errors



class Medicine(models.Model):
    """
    Clase de medicina: almacena un valor y permite recuperarlo.

    Atributos:
        valor: está almacenado en la instancia de la clase.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    dose = models.IntegerField()

    def __str__(self):
        return self.name
        
    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicines(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors
            
        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
            )
        
        return True, None
    
    def update_medicine(self, medicine_data):
        errors = validate_medicines(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()
    
def validate_products(data):
    """
    Valida los datos del producto.

    Args:
        data: Diccionario con los datos del producto.

    Returns:
        dict: Un diccionario con errores de validación si los hay.
    """
    errors = {}
    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")
    stock = data.get("stock", "")

    if name == "":
        errors["name"] = "Ingrese el nombre del producto"

    if type == "":
        errors["type"] = "Ingrese el tipo de producto"
    
    if price == "" :
        errors["price"] = "Ingrese el precio del producto"
    try:
        price = float(price)
        if price < 0:
            errors["price"] = "El precio no puede ser negativo"
    except ValueError:
        errors["price"] = "El precio debe ser un número valido"       

    try:
        stock = int(stock)
        if stock < 0:
            errors["stock"] = "El stock no puede ser negativo"
    except ValueError:
        errors["stock"] = "El stock debe ser un número entero"

    return errors

class Product(models.Model):
    """
    Clase de producto: almacena un valor y permite recuperarlo.

    Atributos:
        valor: está almacenado en la instancia de la clase.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
        
    @classmethod
    def save_product(cls, product_data):
        errors = validate_products(product_data)

        if len(errors.keys()) > 0:
            return False, errors
            
        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
            stock=product_data.get("stock", 0),
        )
        
        return True, None
    
    def update_product(self, product_data):
        errors = validate_products(product_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        if "stock" in product_data:
            try:
                self.stock = int(product_data["stock"])
            except ValueError:
                pass 
        self.save()

class Pet(models.Model):
    """
    Clase de mascota: almacena un valor y permite recuperarlo.

    Atributos:
        valor: está almacenado en la instancia de la clase.
    """
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=300)
    birthday = models.DateField()

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
        )

        return True, None

    def update_pet(self, pet_data):
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()

def validate_vet(data):
        """
        Valida los datos del veterinario.

        Args:
            data: Diccionario con los datos del veterinario.

        Returns:
            dict: Un diccionario con errores de validación si los hay.
        """
        errors = {}
        name = data.get("name", "")
        email = data.get("email", "")
        phone = data.get("phone", "")

        if name == "":
            errors["name"] = "Por favor, ingrese el nombre del veterinario/a"

        if email == "":
            errors["email"] = "Por favor ingrese un email del veterinario/a"
        elif email.count("@") == 0:
            errors["email"] = "Por favor ingrese un email válido del veterinario/a"
        
        if phone == "":
            errors["phone"] = "Por favor, ingrese el telefono del veterinario/a"

        return errors

class Vet(models.Model):
    """
    Clase de veterinarios/as: almacena un valor y permite recuperarlo.

    Atributos:
        valor: está almacenado en la instancia de la clase.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
            )

        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone

        self.save()