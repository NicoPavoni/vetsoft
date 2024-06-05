from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Mascotas", "href": reverse("pets_repo"), "icon":"bi bi-heart-pulse"},
]


def navbar(request):
    """
    Genera un diccionario con una lista de enlaces de navegación, marcando el enlace activo según la ruta de la solicitud actual.

    Args:
        request: Objeto de solicitud HTTP que contiene la ruta de la solicitud actual.

    Returns:
        dict: Un diccionario con una lista de enlaces de navegación donde cada enlace tiene un atributo 'active' que indica si está activo.

    La función interna `add_active` copia cada enlace y establece el atributo 'active' en True si el href del enlace coincide con la ruta de la solicitud actual.
    Para la ruta raíz ("/"), verifica una coincidencia exacta. Para otras rutas, verifica si la ruta de la solicitud comienza con el href del enlace.
    """
    
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
