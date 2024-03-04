Aimme Vivas, Sprint 7

Pruebas Automatizada para UrbanRoutes

Este proyecto incluye pruebas automatizadas utilizando Selenium para la aplicación UrbanRoutes.
Estas pruebas testean diversas funcionalidades, desde establecer rutas hasta interactuar con formularios de pago.

 Requisitos
Asegurarse tener instalados los siguientes requisitos:

- Python (última versión)
- Selenium
- WebDriver para Chrome o navegador a utilizar, en nuestro caso utilizaremos Chrome
- comsndo a utilizar pytest folder/de/proyecto

 Pasos a seguir:

1. Instala pip install selenium
2. Clona el repositorio del proyecto (https://github.com/Aimmevivas/qa-project-07-es)

Archivos Principales
- data.py:
Contiene datos de prueba utilizados en las pruebas, como direcciones, números de teléfono, número de tarjeta de crédito y código de seguridad de la misma

Funcionalidades a testear

1. Establecer Ruta: Verifica que la aplicación pueda establecer correctamente la dirección de origen y destino.
2. Pedir un Taxi: Confirma que el botón "Pedir un taxi" y la opción "Comfort" funcionen como lo esperado
3. Ingresar Número de Teléfono: Asegura que el proceso de ingresar y confirmar un número de teléfono sea exitoso.
4. Agregar Tarjeta de Pago: Verifica que el proceso de agregar una tarjeta de pago se realice correctamente.
5. Llenar Campo de Mensaje para el Conductor: Confirma que el campo de mensaje para el conductor se llene correctamente.
7. Interacciones Adicionales: Cubre interacciones adicionales como cambiar opciones y seleccionar productos.

Conclusión
Este conjunto de pruebas automatizadas para UrbanRoutes nos permite tener una sólida base para validar la funcionalidad de la aplicación.
Al cubrir diversas interacciones, desde la configuración de rutas hasta la interacción con formularios de pago
