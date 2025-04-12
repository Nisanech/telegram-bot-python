import os
import logging

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Verificar si el token está disponible
if not TOKEN:
    logger.error("❌ No se encontró el token del bot.")
    exit(1)

# Estados para la conversación
CHOOSING, TYPING_REPLY, STOPPING = range(3)

# Estados para el submenu
ADDING_NAME, ADDING_PRICE, ADDING_QUANTITY = range(3)
SEARCHING_NAME, SEARCHING_CODE = range(2)
UPDATING_CODE, UPDATING_QUANTITY = range(2)

# Inicializar el inventario
inventory = [
    {
        "name": "Pizza Margarita",
        "price": 12000,
        "quantity": 10,
        "code": 1
    },
    {
        "name": "Pasta con Trufa",
        "price": 15000,
        "quantity": 10,
        "code": 2
    },
    {
        "name": "Salmón a la Parrilla",
        "price": 18000,
        "quantity": 10,
        "code": 3
    },
    {
        "name": "Beef Wellington",
        "price": 25000,
        "quantity": 10,
        "code": 4
    },
    {
        "name": "Ensalada César",
        "price": 8000,
        "quantity": 10,
        "code": 5
    }
]

# Teclados de respuesta
main_menu_keyboard = [
    ['📦 Agregar producto', '🔍 Buscar por nombre'],
    ['🔢 Buscar por código', '📋 Actualizar cantidad'],
    ['💰 Valor total', '📊 Mostrar inventario'],
    ['🚪 Salir'],
]
main_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "¡Bienvenido al Sistema de Gestión de Inventario! 🏪\n\n"
        "Selecciona una opción:",
        reply_markup=main_markup
    )
    return CHOOSING

# Función para el comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Iniciar el sistema\n"
        "/help - Mostrar esta ayuda\n"
        "/menu - Mostrar menú principal\n"
        "/inventario - Mostrar inventario completo\n"
        "/salir - Finalizar la conversación",
        reply_markup=main_markup
    )

# Función para el comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Selecciona una opción:",
        reply_markup=main_markup
    )
    return CHOOSING

# Función para salir del chat
async def exit_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "¡Gracias por usar el Sistema de Gestión de Inventario! 👋\n"
        "Hasta pronto.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Función para agregar un producto - Mensaje de inicio
async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['current_operation'] = 'add_product'
    await update.message.reply_text(
        "📦 *AGREGAR PRODUCTO*\n\n"
        "Ingrese el nombre del nuevo producto:\n"
        "(o use /cancel para volver sin agregar)",
        parse_mode='Markdown',
        reply_markup=main_markup
    )
    return TYPING_REPLY

# Función para agregar un producto
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    step = context.user_data.get('add_step', 'name')

    # Agregar el nombre
    if step == 'name':
        name = user_text

        # Verificar si el producto ya existe
        for product in inventory:
            if product["name"].lower() == name.lower():
                await update.message.reply_text(
                    f"❌ Ya existe un producto con el nombre '{name}'\n"
                    "Ingrese un nombre diferente o use /cancel para cancelar",
                    reply_markup=main_markup
                )
                return TYPING_REPLY

        # Guardar el nombre en el contexto del usuario
        context.user_data["product_name"] = name
        context.user_data['add_step'] = 'price'

        await update.message.reply_text(
            f"Nombre: ✅ {name}\n\n"
            "Ahora ingrese el precio unitario:",
            reply_markup=main_markup
        )
        return TYPING_REPLY

    # Agregar el precio
    elif step == 'price':
        try:
            price = float(user_text)
            if price <= 0:
                await update.message.reply_text(
                    "❌ El precio debe ser mayor que 0. Intente nuevamente:",
                    reply_markup=main_markup
                )
                return TYPING_REPLY

            # Guardar el precio en el contexto del usuario
            context.user_data["product_price"] = price
            context.user_data['add_step'] = 'quantity'

            await update.message.reply_text(
                f"Precio: ✅ ${price}\n\n"
                "Ahora ingrese la cantidad disponible:",
                reply_markup=main_markup
            )
            return TYPING_REPLY

        except ValueError:
            await update.message.reply_text(
                "❌ Por favor ingrese un número válido para el precio:",
                reply_markup=main_markup
            )
            return TYPING_REPLY

    # Agregar la cantidad
    elif step == 'quantity':
        try:
            quantity = int(user_text)
            if quantity < 0:
                await update.message.reply_text(
                    "❌ La cantidad no puede ser negativa. Intente nuevamente:",
                    reply_markup=main_markup
                )
                return TYPING_REPLY

            # Crear y agregar el nuevo producto
            name = context.user_data["product_name"]
            price = context.user_data["product_price"]

            # Generar un nuevo código
            new_code = max([product["code"] for product in inventory]) + 1 if inventory else 1

            # Crear el nuevo producto
            new_product = {
                "name": name,
                "price": price,
                "quantity": quantity,
                "code": new_code
            }

            # Agregar al inventario
            inventory.append(new_product)

            # Limpiar datos temporales
            del context.user_data['add_step']
            del context.user_data['product_name']
            del context.user_data['product_price']
            del context.user_data['current_operation']

            await update.message.reply_text(
                f"✅ Producto '{name}' agregado exitosamente con código {new_code}\n\n"
                "¿Qué deseas hacer ahora?",
                reply_markup=main_markup
            )
            return CHOOSING

        except ValueError:
            await update.message.reply_text(
                "❌ Por favor ingrese un número entero válido para la cantidad:",
                reply_markup=main_markup
            )
            return TYPING_REPLY

# Función para buscar un producto por nombre - Mensaje de inicio
async def search_by_name_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['current_operation'] = 'search_name'
    await update.message.reply_text(
        "🔍 *BUSCAR POR NOMBRE*\n\n"
        "Ingrese el nombre del producto a buscar:",
        parse_mode='Markdown',
        reply_markup=main_markup
    )
    return TYPING_REPLY

# Buscar producto por nombre
async def search_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.lower()
    found = False
    results = "🔍 *RESULTADOS DE BÚSQUEDA*\n\n"

    for product in inventory:
        if name in product["name"].lower():
            results += f"*Código:* {product['code']}\n"
            results += f"*Nombre:* {product['name']}\n"
            results += f"*Precio:* ${product['price']}\n"
            results += f"*Cantidad:* {product['quantity']}\n\n"
            found = True

    if not found:
        results = f"❌ No se encontraron productos con el nombre '{name}'"

    # Limpiar datos temporales
    del context.user_data['current_operation']

    await update.message.reply_text(
        results + "\n¿Qué deseas hacer ahora?",
        parse_mode='Markdown',
        reply_markup=main_markup
    )
    return CHOOSING

# Función para buscar un producto por código - Mensaje de inicio
async def search_by_code_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['current_operation'] = 'search_code'
    await update.message.reply_text(
        "🔢 *BUSCAR POR CÓDIGO*\n\n"
        "Ingrese el código del producto a buscar:",
        parse_mode='Markdown',
        reply_markup=main_markup
    )
    return TYPING_REPLY

# Buscar producto por código
async def search_by_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        code = int(update.message.text)
        found = False

        for product in inventory:
            if product["code"] == code:
                results = f"🔍 *PRODUCTO ENCONTRADO*\n\n"
                results += f"*Código:* {product['code']}\n"
                results += f"*Nombre:* {product['name']}\n"
                results += f"*Precio:* ${product['price']}\n"
                results += f"*Cantidad:* {product['quantity']}"
                found = True
                break

        if not found:
            results = f"❌ No se encontró ningún producto con el código {code}"

        # Limpiar datos temporales
        del context.user_data['current_operation']

        await update.message.reply_text(
            results + "\n\n¿Qué deseas hacer ahora?",
            parse_mode='Markdown',
            reply_markup=main_markup
        )
        return CHOOSING

    except ValueError:
        await update.message.reply_text(
            "❌ Por favor ingrese un número entero válido:",
            reply_markup=main_markup
        )
        return TYPING_REPLY

# Función para actualizar la cantidad de un producto - Mensaje de inicio
async def update_quantity_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['current_operation'] = 'update_quantity'
    await update.message.reply_text(
        "📋 *ACTUALIZAR CANTIDAD*\n\n"
        "Ingrese el código del producto a actualizar:",
        parse_mode='Markdown',
        reply_markup=main_markup
    )
    return TYPING_REPLY

# Función para actualizar la cantidad
async def update_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    step = context.user_data.get('update_step', 'code')

    # Buscar producto
    if step == 'code':
        try:
            code = int(user_text)
            product_index = -1

            for i, product in enumerate(inventory):
                if product["code"] == code:
                    product_index = i
                    break

            if product_index == -1:
                await update.message.reply_text(
                    f"❌ No se encontró ningún producto con el código {code}",
                    reply_markup=main_markup
                )

                # Limpiar datos temporales
                del context.user_data['current_operation']
                return CHOOSING

            context.user_data["product_index"] = product_index
            context.user_data['update_step'] = 'quantity'

            await update.message.reply_text(
                f"Producto: ✅ '{inventory[product_index]['name']}'\n\n"
                "Ingrese la nueva cantidad:",
                reply_markup=main_markup
            )
            return TYPING_REPLY

        except ValueError:
            await update.message.reply_text(
                "❌ Por favor ingrese un número entero válido para el código:",
                reply_markup=main_markup
            )
            return TYPING_REPLY

    # Actualizar cantidad
    elif step == 'quantity':
        try:
            new_quantity = int(user_text)
            if new_quantity < 0:
                await update.message.reply_text(
                    "❌ La cantidad no puede ser negativa. Intente nuevamente:",
                    reply_markup=main_markup
                )
                return TYPING_REPLY

            product_index = context.user_data["product_index"]
            inventory[product_index]["quantity"] = new_quantity

            # Limpiar datos temporales
            del context.user_data['update_step']
            del context.user_data['product_index']
            del context.user_data['current_operation']

            await update.message.reply_text(
                f"✅ Cantidad actualizada para '{inventory[product_index]['name']}' a {new_quantity}\n\n"
                "¿Qué deseas hacer ahora?",
                reply_markup=main_markup
            )
            return CHOOSING

        except ValueError:
            await update.message.reply_text(
                "❌ Por favor ingrese un número entero válido para la cantidad:",
                reply_markup=main_markup
            )
            return TYPING_REPLY

# Calcular valor total del inventario
async def calculate_total_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    total_value = 0
    value_text = "💰 *VALOR TOTAL DEL INVENTARIO*\n\n"

    for product in inventory:
        product_value = product["price"] * product["quantity"]
        total_value += product_value
        value_text += f"{product['name']}: ${product_value:,.0f}\n"

    value_text += f"\n*VALOR TOTAL:* ${total_value:,.0f}"

    await update.message.reply_text(
        value_text + "\n\n¿Qué deseas hacer ahora?",
        parse_mode='Markdown',
        reply_markup=main_markup
    )
    return CHOOSING

# Función para mostrar el inventario completo
async def display_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not inventory:
        await update.message.reply_text("El inventario está vacío", reply_markup=main_markup)
        return CHOOSING

    inventory_text = "📊 *INVENTARIO COMPLETO*\n\n"
    inventory_text += "`CÓDIGO  NOMBRE                      PRECIO      CANTIDAD`\n"
    inventory_text += "`" + "-" * 60 + "`\n"

    for product in inventory:
        inventory_text += f"`{product['code']:<7}{product['name'][:25]:<25}${product['price']:<10}{product['quantity']:<10}`\n"

    await update.message.reply_text(inventory_text, parse_mode='Markdown', reply_markup=main_markup)
    return CHOOSING

# Función para manejar la entrada del usuario
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    user_text = update.message.text
    current_op = context.user_data.get('current_operation', None)

    # Verificar si es una opción del menú principal
    if user_text in ['📦 Agregar producto', '🔍 Buscar por nombre', '🔢 Buscar por código',
                     '📋 Actualizar cantidad', '💰 Valor total', '📊 Mostrar inventario', '🚪 Salir']:

        # Sí es un botón del menú, redirigir a la función correspondiente
        if user_text == '📦 Agregar producto':
            return await add_product_start(update, context)
        elif user_text == '🔍 Buscar por nombre':
            return await search_by_name_start(update, context)
        elif user_text == '🔢 Buscar por código':
            return await search_by_code_start(update, context)
        elif user_text == '📋 Actualizar cantidad':
            return await update_quantity_start(update, context)
        elif user_text == '💰 Valor total':
            return await calculate_total_value(update, context)
        elif user_text == '📊 Mostrar inventario':
            return await display_inventory(update, context)
        elif user_text == '🚪 Salir':
            return await exit_chat(update, context)

    # Si no es una opción del menú, procesar según la operación actual
    if current_op == 'add_product':
        return await add_product(update, context)
    elif current_op == 'search_name':
        return await search_by_name(update, context)
    elif current_op == 'search_code':
        return await search_by_code(update, context)
    elif current_op == 'update_quantity':
        return await update_quantity(update, context)
    else:
        await update.message.reply_text(
            "No entiendo esa entrada. Por favor selecciona una opción del menú.",
            reply_markup=main_markup
        )
        return CHOOSING

# Función para cancelar la operación actual
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Limpiar datos temporales
    keys_to_remove = []
    for key in context.user_data:
        if key in ['add_step', 'product_name', 'product_price', 'update_step',
                  'product_index', 'current_operation']:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del context.user_data[key]

    await update.message.reply_text(
        "🚫 Operación cancelada.\n\n¿Qué deseas hacer ahora?",
        reply_markup=main_markup
    )
    return CHOOSING

def main():
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()

    # Agregar manejadores
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex('^📦 Agregar producto$'), add_product_start),
                MessageHandler(filters.Regex('^🔍 Buscar por nombre$'), search_by_name_start),
                MessageHandler(filters.Regex('^🔢 Buscar por código$'), search_by_code_start),
                MessageHandler(filters.Regex('^📋 Actualizar cantidad$'), update_quantity_start),
                MessageHandler(filters.Regex('^💰 Valor total$'), calculate_total_value),
                MessageHandler(filters.Regex('^📊 Mostrar inventario$'), display_inventory),
                MessageHandler(filters.Regex('^🚪 Salir$'), exit_chat),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input),
            ],
            TYPING_REPLY: [
                CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('salir', exit_chat)
        ]
    )

    application.add_handler(conv_handler)

    # Comandos de ayuda
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('inventario', display_inventory))
    application.add_handler(CommandHandler('salir', exit_chat))

    # Iniciar el bot
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

if __name__ == "__main__":
    main()