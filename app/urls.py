from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    path("medicines/", view=views.medicines_repository, name="medicines_repo"),
    path("medicines/nuevo/", view=views.medicines_form, name="medicines_form"),
    path("medicines/editar/<int:id>/", view=views.medicines_form, name="medicines_edit"),
    path("medicines/eliminar/", view=views.medicines_delete, name="medicines_delete"),
    path("products/", view=views.products_repository, name="products_repo"),
    path("products/nuevo/", view=views.products_form, name="products_form"),
    path("products/editar/<int:id>/", view=views.products_form, name="products_edit"),
    path("products/eliminar/", view=views.products_delete, name="products_delete"),
    path("products/increase_stock/", view=views.increase_stock, name="increase_stock"),
    path("products/decrease_stock/", view=views.decrease_stock, name="decrease_stock"),
    path("mascotas/", view=views.pets_repository, name="pets_repo"),
    path("mascotas/nuevo/", view=views.pets_form, name="pets_form"),
    path("mascotas/editar/<int:id>/", view=views.pets_form, name="pets_edit"),
    path("mascotas/eliminar/", view=views.pets_delete, name="pets_delete"),
    path("veterinario/", view=views.vet_repository, name="vet_repo"),
    path("veterinario/nuevo/", view=views.vet_form, name="vet_form"),
    path("veterinario/editar/<int:id>/", view=views.vet_form, name="vet_edit"),
    path("veterinario/eliminar/", view=views.vet_delete, name="vet_delete"),
]
