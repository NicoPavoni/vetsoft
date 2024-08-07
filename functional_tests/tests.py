import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 0) == 1
slow_mo = os.environ.get("SLOW_MO", 500)


class PlaywrightTestCase(StaticLiveServerTestCase):
    """
    Clase base para tests utilizando Playwright con un servidor estático en vivo.

    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=True, slow_mo=int(slow_mo),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    """
    Clase de tests para el Home con Playwright
    """
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    """
    Clase de tests para el modelo de clientes con Playwright
    """
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="54221232555",
            email="goleador@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente",
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    """
    Clase de tests para la creacion y edicion de los clientes con Playwright
    """
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        divs = self.page.locator(".invalid-feedback").all()
        
        textos = [div.text_content() for div in divs]
        assert "Por favor ingrese un nombre" in str(textos)
        assert "Por favor ingrese un teléfono" in str(textos)
        assert "Por favor ingrese un email" in str(textos)

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        divs = self.page.locator(".invalid-feedback").all()
        
        textos = [div.text_content() for div in divs]
        assert "El correo electrónico debe terminar en @vetsoft.com" in str(textos)

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("54221232555")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )
    
    def test_clientPhone_should_give_error(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Perez")
        self.page.get_by_label("Teléfono").fill("aaaaa")
        self.page.get_by_label("Email").fill("testMail@vetsoft.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        divs = self.page.locator(".invalid-feedback").all()
        
        textos = [div.text_content() for div in divs]
        assert "El teléfono sólo puede contener números" in str(textos)

    def test_cant_create_a_client_with_numbers_in_name(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Perez68")
        self.page.get_by_label("Teléfono").fill("aaaaa")
        self.page.get_by_label("Email").fill("testMail@vetsoft.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        divs = self.page.locator(".invalid-feedback").all()
        
        textos = [div.text_content() for div in divs]
        assert "El nombre solo debe contener letras y espacios" in str(textos)

    def test_cant_create_a_client_with_letters_in_phone(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Perez")
        self.page.get_by_label("Teléfono").fill("aaaaa")
        self.page.get_by_label("Email").fill("testMail@vetsoft.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        divs = self.page.locator(".invalid-feedback").all()
        
        textos = [div.text_content() for div in divs]
        assert "El teléfono sólo puede contener números" in str(textos)


class AddPet(PlaywrightTestCase):
    """
    Clase de tests para agregar una mascota con Playwright
    """
    def test_add_new_pet(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Cachito")
        self.page.get_by_label("Raza").fill("Una Raza")
        self.page.get_by_label("Cumpleaños").fill("2024-05-05")

        self.page.get_by_role("button", name="Guardar").click()

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        expect(self.page.get_by_text("Cachito")).to_be_visible()
        expect(self.page.get_by_text("Una Raza")).to_be_visible()

    def test_add_new_empy_pet(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("")
        self.page.get_by_label("Raza").fill("")
        self.page.get_by_label("Cumpleaños").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        divs = self.page.locator(".invalid-feedback").all()
        
        textos = [div.text_content() for div in divs]
        assert "Por favor ingrese un nombre" in str(textos)
        assert "Por favor ingrese la raza" in str(textos)
        assert "Por favor ingrese una fecha" in str(textos)

class AddProduct(PlaywrightTestCase):
    """
    Clase de tests para agregar un producto con Playwright
    """
    def test_add_new_product(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Producto1")
        self.page.get_by_label("Tipo").fill("Tipo1")
        self.page.get_by_label("Precio").fill("10")
        self.page.get_by_label("Stock").fill("15")
        

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Producto1")).to_be_visible()
        expect(self.page.get_by_text("Tipo1")).to_be_visible()
        expect(self.page.get_by_text("10")).to_be_visible()
        expect(self.page.get_by_text("15")).to_be_visible()

class AddMedicine(PlaywrightTestCase):
    """
    Clase de tests para agregar una medicina con Playwright
    """
    def test_add_new_medicine(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Bayaspirina")
        self.page.get_by_label("Descripción").fill("Para dolores de cabeza")
        self.page.get_by_label("Dosis").fill("1")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Bayaspirina")).to_be_visible()
        expect(self.page.get_by_text("Para dolores de cabeza")).to_be_visible()
        expect(self.page.get_by_text("1")).to_be_visible()

    def test_medicine_dose_range(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Medicina 1")
        self.page.get_by_label("Descripción").fill("Descripción de medicina 1")
        self.page.get_by_label("Dosis").fill("0")

        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("La dosis debe ser entre 1 y 10")).to_be_visible()

        self.page.get_by_label("Dosis").fill("12")

        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("La dosis debe ser entre 1 y 10")).to_be_visible()

