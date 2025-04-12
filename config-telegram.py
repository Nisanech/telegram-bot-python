import os
import logging
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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

# Variable para controlar el estado del bot
bot_running = True

# Función para el comando /start
async def start_command( update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    user = update.effective_user

    await update.message.reply_text(
        f'¡{user.first_name}! El bot está funcionando correctamente.✅\n\n'
        f'Opciones disponibles:\n'
        f'/start - Reiniciar el bot\n'
        f'/help - Ver ayuda\n'
        f'/salir - Finalizar la conversación'
    )

    logger.info( f"Usuario {user.id} ({user.first_name}) inició una conversación" )


# Función para el comando /help
async def help_command( update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    await update.message.reply_text(
        'Este es un bot de prueba para validar la conexión.\n'
        'Comandos disponibles:\n'
        '/start - Reiniciar el bot\n'
        '/help - Muestra este mensaje de ayuda\n'
        '/salir - Finalizar la conversación'
    )

# Función para el comando /salir
async def exit_command( update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    global bot_running

    user = update.effective_user
    await update.message.reply_text( f'¡{user.first_name}! Finalizando la conversación.' )
    logger.info( f"Usuario {user.id} ({user.first_name}) finalizó la conversación con /salir" )

    await context.application.stop()
    bot_running = False
    logger.info( "Bot detenido por comando /salir" )


# Función para manejar mensajes de texto
async def show_message( update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    message_received = update.message.text
    logger.info( f"Mensaje recibido: '{message_received}' de {update.effective_user.first_name}" )

    await update.message.reply_text(
        f"Recibí tu mensaje: {message_received}\n\n"
        f"Recuerda que puedes usar:\n"
        f"/start - Reiniciar\n"
        f"/help - Ayuda\n"
        f"/salir - Finalizar"
    )

def main() -> None:
    # Crear la aplicación
    application = Application.builder().token( TOKEN ).build()

    # Registrar manejadores
    application.add_handler( CommandHandler( "start", start_command ) )
    application.add_handler( CommandHandler( "help", help_command ) )
    application.add_handler( CommandHandler( "salir", exit_command ) )
    application.add_handler( MessageHandler( filters.TEXT & ~filters.COMMAND, show_message ) )

    # Iniciar el bot
    logger.info( "Iniciando bot..." )
    application.run_polling( allowed_updates = Update.ALL_TYPES )

    # Sí se activó el comando /salir, terminar el programa
    if not bot_running:
        print( "Finalizando programa por solicitud del usuario" )
        sys.exit( 0 )


if __name__ == "__main__":
    print( "Iniciando validación del bot de Telegram..." )
    print( f"El token comienza con: {TOKEN[ :5 ]}..." if TOKEN else "⚠️No se encontró el token" )

    main()