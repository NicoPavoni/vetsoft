from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Client, Medicine, Pet, Product, Vet


def home(request):
    """
    Renderiza la página de inicio.
    """
    return render(request, "home.html")

def clients_repository(request):
    """
    Muestra todos los clientes en el repositorio.
    """
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})

def clients_form(request, id=None):
    """
    Maneja el formulario de creación y actualización de clientes.

    Args:
        request: Objeto de solicitud HTTP.
        id: ID opcional del cliente para editar (None para crear un nuevo cliente).

    Returns:
        HttpResponse: Redirige al repositorio de clientes si se guarda con éxito.
        Render: Renderiza el formulario con errores si hay problemas o con los datos del cliente a editar.
    """
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            saved, errors = client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))
        
        if len(errors) > 0:
            messages.warning(request, f"{errors}")

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST},
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})

def clients_delete(request):
    """
    Elimina un cliente de la base de datos según el ID proporcionado en la solicitud POST.

    Args:
        request: Objeto de solicitud HTTP que contiene el ID del cliente en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de clientes después de eliminar el cliente.
    """
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()
    return redirect(reverse("clients_repo"))

def medicines_repository(request):
    """
    Muestra todos los medicamentos en el repositorio.
    """
    medicines = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicines})

def medicines_form(request, id=None):
    """
    Maneja el formulario de creación y actualización de medicamentos.

    Args:
        request: Objeto de solicitud HTTP.
        id: ID opcional del medicamento para editar (None para crear un nuevo medicamento).

    Returns:
        HttpResponse: Redirige al repositorio de medicamentos si se guarda con éxito.
        Render: Renderiza el formulario con errores si hay problemas o con los datos del medicamento a editar.
    """
    if request.method == "POST":
        medicine_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine.update_medicine(request.POST)

        if saved:
            return redirect(reverse("medicines_repo"))

        return render(
            request, "medicines/form.html", {"errors": errors, "medicine": request.POST},
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicines/form.html", {"medicine": medicine})

def medicines_delete(request):
    """
    Elimina un medicamento de la base de datos según el ID proporcionado en la solicitud POST.

    Args:
        request: Objeto de solicitud HTTP que contiene el ID del medicamento en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de medicamentos después de eliminar el medicamento.
    """
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()
    return redirect(reverse("medicines_repo"))

def products_repository(request):
    """
    Muestra todos los productos en el repositorio.
    """
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})

def products_form(request, id=None):
    """
    Maneja el formulario de creación y actualización de productos.

    Args:
        request: Objeto de solicitud HTTP.
        id: ID opcional del producto para editar (None para crear un nuevo producto).

    Returns:
        HttpResponse: Redirige al repositorio de productos si se guarda con éxito.
        Render: Renderiza el formulario con errores si hay problemas o con los datos del producto a editar.
    """
    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if product_id == "":
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            saved, errors = product.update_product(request.POST)

        if saved:
            return redirect(reverse("products_repo"))

        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST},
        )

    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)

    return render(request, "products/form.html", {"product": product})

def products_delete(request):
    """
    Elimina un producto de la base de datos según el ID proporcionado en la solicitud POST.

    Args:
        request: Objeto de solicitud HTTP que contiene el ID del producto en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de productos después de eliminar el producto.
    """
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()
    return redirect(reverse("products_repo"))

def increase_stock(request):
    """
    Aumenta el stock de un producto según el ID proporcionado en la solicitud POST.

    Args:
        request: Objeto de solicitud HTTP que contiene el ID del producto en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de productos después de aumentar el stock.
    """
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        product.stock += 1
        product.save()
        return redirect("products_repo")

def decrease_stock(request):
    """
    Disminuye el stock de un producto según el ID proporcionado en la solicitud POST.

    Args:
        request: Objeto de solicitud HTTP que contiene el ID del producto en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de productos después de disminuir el stock.
    """
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        if product.stock > 0:
            product.stock -= 1
            product.save()
        
        if product.stock == 0:
            messages.warning(request, f"{product.name}: Fuera de stock.")

        return redirect("products_repo")

def pets_repository(request):
    """
    Muestra todas las mascotas en el repositorio.
    """
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pets_form(request, id=None):
    """
    Maneja el formulario de creación y actualización de mascotas.

    Args:
        request: Objeto de solicitud HTTP.
        id: ID opcional de la mascota para editar (None para crear una nueva mascota).

    Returns:
        HttpResponse: Redirige al repositorio de mascotas si se guarda con éxito.
        Render: Renderiza el formulario con errores si hay problemas o con los datos de la mascota a editar.
    """
    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)

        if saved:
            return redirect(reverse("pets_repo"))
        
        if len(errors) > 0:
            messages.warning(request, f"{errors}")

        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST},
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet})

def pets_delete(request):
    """
    Elimina una mascota de la base de datos según el ID proporcionado en la solicitud POST.

    Args:
        request: Objeto de solicitud HTTP que contiene el ID de la mascota en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de mascotas después de eliminar la mascota.
    """
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()
    return redirect(reverse("pets_repo"))

def vet_repository(request):
    """
    Muestra todos los veterinarios en el repositorio.
    """
    vets = Vet.objects.all()
    return render(request, "vets/repository.html", {"vets": vets})

def vet_form(request, id=None):
    """
    Maneja el formulario de creación y actualización de veterinarios.

    Args:
        request: Objeto de solicitud HTTP.
        id: ID opcional del veterinario para editar (None para crear un nuevo veterinario).

    Returns:
        HttpResponse: Redirige al repositorio de veterinarios si se guarda con éxito.
        Render: Renderiza el formulario con errores si hay problemas o con los datos del veterinario a editar.
    """
    
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vet_repo"))

        return render(
            request, "vets/form.html", {"errors": errors, "vet": request.POST},
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)

    return render(request, "vets/form.html", {"vet": vet})

def vet_delete(request):
    """
    Elimina un veterinario de la base de datos según el ID proporcionado en la solicitud POST.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene el ID del veterinario en los datos POST.

    Returns:
        HttpResponseRedirect: Redirige a la página del repositorio de veterinarios después de eliminar el veterinario.
    """
    
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()
    return redirect(reverse("vet_repo"))