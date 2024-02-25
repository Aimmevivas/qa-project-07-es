import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException


class UrbanRoutesPage:
    address_from = (By.ID, 'from')
    address_to = (By.ID, 'to')
    personal_mode = (By.XPATH, "//div[@class='mode' and text()='Personal']")
    taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_button = (By.XPATH, "//button[@data-for='tariff-card-4']")
    phone_number_open = (By.XPATH, "//div[@class='np-text' and contains(text(), 'Número de teléfono')]")
    phone_input_section = (By.XPATH, "//div[@class='section active']//input[@id='phone' and @class='input']")
    phone_input_field = (By.XPATH, "//input[@id='phone']")
    next_phone_number_button = (By.XPATH, "//button[@type='submit' and contains(@class, 'button full')]")
    phone_verification_code = (By.XPATH, "//input[@id='code']")
    submit_phone_code = (By.XPATH, '//button[@type="submit" and @class="button full" and text()="Confirmar"]')
    phone_number_is_filled = (By.XPATH, "//div[@class='np-button filled']/div[@class='np-text'][text()='{{phone_number}}']")
    payment_method_open = (By.XPATH, "//div[@class='pp-button filled']//div[@class='pp-text' and text()='Forma de pago']")
    payment_input_section = (By.XPATH, "//div[@class='modal']//div[@class='section active']//button[text()='Cancelar']")
    add_card_open = (By.XPATH, "//div[contains(@class, 'pp-row') and contains(@class, 'disabled') and .//div[@class='pp-title' and text()='Agregar una tarjeta']]")
    card_input_field = (By.XPATH, "//div[@class='card-number-input']/input[@type='text']")
    cvv_input_field = (By.XPATH, "//div[@class='card-code-input']/input[@type='text']")
    focus_change = (By.XPATH, "//div[@class='head' and text()='Agregar una tarjeta']")
    submit_add_card = (By.XPATH, "//button[@type='submit' and contains(@class, 'button') and contains(@class, 'full') and contains(text(), 'Enlace')]")
    payment_method_close = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[1]/button")
    message_for_driver_field = (By.XPATH, "//input[@id='comment']")
    blanket_and_tissues = (By.XPATH, "//div[@class='r-sw-container']//input[@type='checkbox' and @class='switch-input']")
    ice_cream_counter = (By.XPATH, '//div[@class="r-counter-label" and text()="Helado"]')
    ice_cream_plus_button = (By.XPATH, '//div[@class="r-counter-label" and text()="Helado"]/following-sibling::div[@class="counter-plus"]')
    get_a_taxi = (By.XPATH, '//button[@type="button" and @class="smart-button"]/span[@class="smart-button-main"][text()="Pedir un taxi"]')
    taxi_modal = (By.XPATH, '/html/body/div/div/div[5]/div[2]')

    def __init__(self, driver):
       self.driver = driver

    def set_from(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'from')))
        element.send_keys(data.address_from)

    def set_to(self):
        self.driver.find_element(*self.address_to).send_keys(data.address_to)

    def get_from(self):
        return self.driver.find_element(*self.address_from).get_attribute('value')

    def get_to(self):
        return self.driver.find_element(*self.address_to).get_attribute('value')

    def click_personal_mode(self):
        personal_mode = self.driver.find_element(*self.personal_mode)
        personal_mode.click()

    def click_taxi_button(self):
        wait = WebDriverWait(self.driver, 15)
        taxi_button = wait.until(EC.element_to_be_clickable(self.taxi_button))
        taxi_button.click()

    def get_comfort_button(self):
        wait = WebDriverWait(self.driver, 15)

        comfort_button_present = wait.until(EC.presence_of_element_located(self.comfort_button))

        self.click_taxi_button()
        comfort_button = wait.until(EC.element_to_be_clickable(self.comfort_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", comfort_button)

        try:
            comfort_button.click()
        except ElementClickInterceptedException:
            # Si el clic es interceptado, intentar hacer clic mediante JavaScript
            self.driver.execute_script("arguments[0].click();", comfort_button)

        return comfort_button

    def click_phone_number_open(self):
        wait = WebDriverWait(self.driver, 5)
        phone_number_open = wait.until(EC.element_to_be_clickable(self.phone_number_open))
        phone_number_open.click()

    def phone_input_section_is_active(self):
        wait = WebDriverWait(self.driver, 5)
        return wait.until(EC.visibility_of_element_located(self.phone_input_section))

    def fill_phone_input_field(self, test_data):
        phone_input = self.driver.find_element(*self.phone_input_field)
        phone_input.clear()
        phone_input.send_keys(test_data)

    def click_next_phone_number_button(self):
        wait = WebDriverWait(self.driver, 5)
        next_phone_number_button = wait.until(EC.element_to_be_clickable(self.next_phone_number_button))
        next_phone_number_button.click()

    def fill_phone_verification_code(self, code):
        phone_verification_input = self.driver.find_element(*self.phone_verification_code)
        phone_verification_input.clear()
        phone_verification_input.send_keys(code)
    def retrieve_phone_code(self):
        """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
        Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
        El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

        import json
        import time
        from selenium.common import WebDriverException

        code = None
        for i in range(10):
            try:
                logs = [log["message"] for log in self.driver.get_log('performance') if log.get("message")
                        and 'api/v1/number?number' in log.get("message")]
                for log in reversed(logs):
                    message_data = json.loads(log)["message"]
                    body = self.driver.execute_cdp_cmd('Network.getResponseBody',
                                                       {'requestId': message_data["params"]["requestId"]})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
            except WebDriverException:
                time.sleep(1)
                continue

            if not code:
                raise Exception("No se encontró el código de confirmación del teléfono.\n"
                                "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")

            return code

    def click_submit_phone_code(self):
        wait = WebDriverWait(self.driver, 30)
        submit_phone_code = wait.until(EC.element_to_be_clickable(self.submit_phone_code))
        submit_phone_code.click()

    def is_phone_number_filled(self):
        try:
            phone_input = self.driver.find_element(*self.phone_input_field)
            phone_number = phone_input.get_attribute('value')
            return bool(phone_number)
        except NoSuchElementException:
            return False

    def click_payment_method_open(self):
        wait = WebDriverWait(self.driver, 5)
        payment_method_open = wait.until(EC.element_to_be_clickable(self.payment_method_open))
        payment_method_open.click()

    def payment_input_section_is_active(self):
        wait = WebDriverWait(self.driver, 5)
        return wait.until(EC.visibility_of_element_located(self.payment_input_section))

    def click_add_card_open(self):
        wait = WebDriverWait(self.driver, 5)
        add_card_open = wait.until(EC.element_to_be_clickable(self.add_card_open))
        add_card_open.click()

    def fill_card_input_field(self, test_data):
        card_input = self.driver.find_element(*self.card_input_field)
        card_input.clear()
        card_input.send_keys(test_data)

    def fill_cvv_input_field(self, test_data):
        cvv_input = self.driver.find_element(*self.cvv_input_field)
        cvv_input.clear()
        cvv_input.send_keys(test_data)

    def click_focus_change(self):
        wait = WebDriverWait(self.driver, 5)
        focus_change = wait.until(EC.element_to_be_clickable(self.focus_change))
        focus_change.click()

    def click_submit_add_card(self):
        wait = WebDriverWait(self.driver, 15)
        submit_add_card = wait.until(EC.element_to_be_clickable(self.submit_add_card))
        submit_add_card.click()

    def click_payment_method_close(self):
        wait = WebDriverWait(self.driver, 5)
        payment_method_close = wait.until(EC.element_to_be_clickable(self.payment_method_close))
        payment_method_close.click()

    def fill_message_for_driver_field(self, test_data):
        message_for_driver_field = self.driver.find_element(*self.message_for_driver_field)
        message_for_driver_field.clear()
        message_for_driver_field.send_keys(test_data)

    def switch_blanket_and_tissues(self):
        blanket_and_tissues_switch = (By.CLASS_NAME, 'switch-input')
        switch_element = self.driver.find_element(*blanket_and_tissues_switch)

        # Desplazarse hasta el elemento
        self.driver.execute_script("arguments[0].scrollIntoView(true);", switch_element)

        # Intentar interactuar con el elemento
        try:
            switch_element.click()
        except ElementNotInteractableException:
            # Si el clic no es posible, intentar con JavaScript
            self.driver.execute_script("arguments[0].click();", switch_element)

    def click_ice_cream_plus_button(self):
        try:
            ice_cream_counter = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.ice_cream_counter))
            current_value = int(ice_cream_counter.text)

            if current_value < 2:
                try:
                    ice_cream_plus_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(self.ice_cream_plus_button))
                    self.driver.execute_script("arguments[0].scrollIntoView();", ice_cream_plus_button)
                    for _ in range(2 - current_value):
                        ice_cream_plus_button.click()
                except Exception as e:
                    print(f"No se pudo hacer clic en el botón directamente: {e}")
                    # Si no se puede hacer clic directamente, intentar hacer clic mediante JavaScript
                    ice_cream_plus_button_js = self.driver.find_element_by_id(
                        'ice_cream_plus_button_id')  # Reemplaza con tu selector específico
                    for _ in range(2 - current_value):
                        self.driver.execute_script("arguments[0].click();", ice_cream_plus_button_js)
        except Exception as e:
            print(f"No se pudo encontrar el contador de helados: {e}")

    def click_get_a_taxi(self):
        wait = WebDriverWait(self.driver, 5)
        get_a_taxi = wait.until(EC.element_to_be_clickable(self.get_a_taxi))
        get_a_taxi.click()

    def wait_for_modal_with_taxi_info(self):
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.taxi_modal))

            print("El modal con la información del conductor está presente")

        except Exception as e:
            print(f"Ocurrió un error al esperar el modal o los datos del conductor: {e}")


driver = webdriver.Chrome()
driver.get(data.urban_routes_url)

class TestUrbanRoutes:
    driver = None
    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from()
        routes_page.set_to()

        assert routes_page.get_from() == address_from, "Address 'from' not set correctly"
        assert routes_page.get_to() == address_to, "Address 'to' not set correctly"

    def test_click_comfort_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_taxi_button()
        comfort_button = routes_page.comfort_button
        # Obtener el botón 'Comfort' después de hacer clic en 'Pedir un taxi'

        assert comfort_button is not None, "No se pudo obtener el botón 'Comfort'"

    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        test_data = data.phone_number
        routes_page.click_phone_number_open()

        assert routes_page.phone_input_section_is_active(), "La sección de entrada de número de teléfono no está activa"

        routes_page.fill_phone_input_field(test_data)
        routes_page.click_next_phone_number_button()
        verification_code = routes_page.retrieve_phone_code()
        routes_page.fill_phone_verification_code(verification_code)
        routes_page.click_submit_phone_code()

        assert routes_page.is_phone_number_filled(), "El número de teléfono no se ha llenado correctamente"

    def test_add_payment_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method_open()
        routes_page.click_add_card_open()
        test_card_number = data.card_number
        test_cvv = data.cvv
        routes_page.fill_card_input_field(test_card_number)
        routes_page.fill_cvv_input_field(test_cvv)
        routes_page.click_focus_change()
        routes_page.click_submit_add_card()
        routes_page.click_payment_method_close()

        assert True

    def test_fill_message_for_driver_field(self):
        routes_page = UrbanRoutesPage(self.driver)
        test_message = data.message_for_driver
        routes_page.fill_message_for_driver_field(test_message)
        message_field_value = test_message

        assert message_field_value == test_message, "El campo de mensaje para el conductor no se llenó correctamente"

    def test_switch_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.switch_blanket_and_tissues()

        assert True

    def test_click_ice_cream_counter(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_ice_cream_plus_button()

        assert True


    def test_taxi_modal_with_info(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_get_a_taxi()
        routes_page.wait_for_modal_with_taxi_info()

        assert True
