# Gestión de Inventario de Tienda

Este proyecto consiste en el desarrollo de un programa que gestiona el inventario de un restaurante. El programa 
permitirá agregar productos al inventario, realizar búsquedas por nombre, realizar búsquedas por código, actualizar 
cantidades de productos, calcular el valor total del inventario y mostrar inventario. Además, se implementa un menú 
interactivo donde el usuario puede elegir las diferentes acciones a realizar.

## Archivos del Proyecto

- `store-inventory.py`: Contiene el código del programa principal, que gestiona el inventario de la tienda a través de 
la consola.
- `store-inventory-telegram.py`: Contiene el código del programa principal, que gestiona el inventario de la tienda 
a través de un bot de Telegram.
- `config-telegram.py`: Contiene un código de ejemplo para configurar y ejecutar el bot de Telegram.

## Requisitos

- Python 3.13
- Token del bot de Telegram creado a través de [@BotFather](https://t.me/BotFather)
- Librería [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/index.html)
- Librería [python-dotenv](https://pypi.org/project/python-dotenv/)

## Instalación y Ejecución del Proyecto

1. **Clonar el repositorio**

    ```bash
      git clone https://github.com/Nisanech/telegram-bot-python
    ```
       
    ```bash
      cd telegram-bot-python
    ```
   
2. **Crear un entorno virtual en Windows**

    ```bash
      python -m venv venv
    ```

    ```bash
      .\venv\Scripts\activate
    ```

3. **Instalar las dependencias**

    ```bash
      pip install -r requirements.txt
    ```

4. **Configurar el token del bot de Telegram**

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```
TELEGRAM_BOT_TOKEN=token_del_bot_de_telegram
```

## Ejecutar el Proyecto

1. Ejecutar la aplicación en la consola:

    ```bash
      python store-inventory.py
    ```

2. Ejecutar la aplicación en Telegram:

    ```bash
      python store-inventory-telegram.py
    ```

3. Ejecutar la aplicación de configuración en Telegram:

    ```bash
      python config-telegram.py
    ```
   
## Estructura del Proyecto

```
telegram-bot-python/
├── config-telegram.py
├── store-inventory.py
├── store-inventory-telegram.py
├── requirements.txt
├── .env.example
└── README.md
```

## Documentación

La documentación del proyecto se encuentra en el siguiente enlace: 
[Documentación](https://polydactyl-mule-c5a.notion.site/Proyecto-Gesti-n-de-Inventario-de-Tienda-Bot-Telegram-1d0e4951fb4c80a89b3cf1cddbd284c8)

## Desarrollado por

[Nicolas Santiago Naranjo](https://github.com/Nisanech) para el curso de 
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) de 
[Dev Senior Code](https://devseniorcode.com/)
