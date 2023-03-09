import logging
import mysql.connector
import Prueba_pandas
from typing import Dict

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

Planta_B=["TECNOLOGÍA","INFRAESTRUCTURA","COE","CAPITAL HUMANO","OFICIALÍA",
"OPERACIONES PB","AUDITORIO","CUARTO_DE_CONTROL","ALMACÉN","NOC-SOC","CASETAS_PBI"]
Piso1=["JURÍDICO","LLAMADAS 911","ESTADÍSTICA","UCA","APH","OPERACIONES","DEPENDENCIAS C3",
"DESPACHO","MÉDICAS","SALA_CRISIS","CALIDAD","VINCULACIÓN"]
Piso2=["DGAF","DGGE","DGAT","DGAO","FINANZAS","CAPACITACIÓN","SALAS_DE_JUNTAS","LOCATEL",
"SALA DE OBSERVACION"]
Piso3=["JEFATURA DE GOBIERNO","COORDINACIÓN GENERAL","REDES SOCIALES",
"MONITROREO INTELIGENTE","SEDESA","FISCALÍA","PENITENCIARÍA","LOCATEL","SALAS_DE_JUNTAS",]
Externo=["C2'S","ALCALDÍAS","BALBUENA","SEÑALES_COMPARTIDAS"]
Niveles=["PLANTA_BAJA","PISO1","PISO2","PISO3","EXTERNOS"]
Nombres=["ARACELI BENITEZ ROSALES","EDSON NAVARRO ALONSO","ZAHED LILA SANDOVAL",
"SERGIO LÓPEZ SÁNCHEZ","GUSTAVO HERNANDEZ LOPEZ","GERARDO MORALES GARCÍA"]
Actividad=["SOPORTE_WKS_ADMIN","SOPORTE_WKS_OPERATIVA","SOPORTE_IMPRESORAS","SOPORTE_OI",
"SOPORTE_GENERAL","ACTIVIDAD_ADMIN","CLONACIÓN_DONACIONES","WKS_ALCALDÍAS",
"IMÁGENES_DE_SO","MANTENIMIENTOS","WSUS"]
Tt=["MESA DE AYUDA","A SOLICITUD","BARRIDO"]

fase0,fase1, fase2, fase3, fase4, fase5,fase6,fase7,fase8 = range(9)
com_si, com_no, regresar_inicio,regresar_piso,regresar_nombre,regresar_actividad= range(6)
busqueda,bitacora= range(2)
# Pre-assign menu text
FIRST_MENU = "<b>Bienvenido</b>\n\n Seleccione el piso de la incidencia."
SECOND_MENU = "<b>Areas</b>\n\n."
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database ="WKS"
    #database="datos_adtvo_c5"
)

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("busqueda", callback_data=str(busqueda))],
    [InlineKeyboardButton("bitacora", callback_data=str(bitacora))],
    ])
MENU_FLOOR_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion", callback_data=str(regresar_inicio))],
    [InlineKeyboardButton(Niveles[0], callback_data=Niveles[0])],
    [InlineKeyboardButton(Niveles[1], callback_data=Niveles[1])],
    [InlineKeyboardButton(Niveles[2], callback_data=Niveles[2])],
    [InlineKeyboardButton(Niveles[3], callback_data=Niveles[3])],
    [InlineKeyboardButton(Niveles[4], callback_data=Niveles[4])],
    ])

MENU_PB_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de piso ", callback_data=str(regresar_piso))],
    [InlineKeyboardButton(Planta_B[0], callback_data=Planta_B[0])],
    [InlineKeyboardButton(Planta_B[1], callback_data=Planta_B[1])],
    [InlineKeyboardButton(Planta_B[2], callback_data=Planta_B[2])],
    [InlineKeyboardButton(Planta_B[3], callback_data=Planta_B[3])],
    [InlineKeyboardButton(Planta_B[4], callback_data=Planta_B[4])],
    [InlineKeyboardButton(Planta_B[5], callback_data=Planta_B[5])],
    [InlineKeyboardButton(Planta_B[6], callback_data=Planta_B[6])],
    [InlineKeyboardButton(Planta_B[7], callback_data=Planta_B[7])],
    [InlineKeyboardButton(Planta_B[8], callback_data=Planta_B[8])],
    [InlineKeyboardButton(Planta_B[9], callback_data=Planta_B[9])],
    [InlineKeyboardButton(Planta_B[10], callback_data=Planta_B[10])]
])
MENU_P1_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de piso", callback_data=str(regresar_piso))],
    [InlineKeyboardButton(Piso1[0], callback_data=Piso1[0])],
    [InlineKeyboardButton(Piso1[1], callback_data=Piso1[1])],
    [InlineKeyboardButton(Piso1[2], callback_data=Piso1[2])],
    [InlineKeyboardButton(Piso1[3], callback_data=Piso1[3])],
    [InlineKeyboardButton(Piso1[4], callback_data=Piso1[4])],
    [InlineKeyboardButton(Piso1[5], callback_data=Piso1[5])],
    [InlineKeyboardButton(Piso1[6], callback_data=Piso1[6])],
    [InlineKeyboardButton(Piso1[7], callback_data=Piso1[7])],
    [InlineKeyboardButton(Piso1[8], callback_data=Piso1[8])],
    [InlineKeyboardButton(Piso1[9], callback_data=Piso1[9])],
    [InlineKeyboardButton(Piso1[10], callback_data=Piso1[10])],
    [InlineKeyboardButton(Piso1[11], callback_data=Piso1[11])]
])
MENU_P2_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de piso", callback_data=str(regresar_piso))],
    [InlineKeyboardButton(Piso2[0], callback_data=Piso2[0])],
    [InlineKeyboardButton(Piso2[1], callback_data=Piso2[1])],
    [InlineKeyboardButton(Piso2[2], callback_data=Piso2[2])],
    [InlineKeyboardButton(Piso2[3], callback_data=Piso2[3])],
    [InlineKeyboardButton(Piso2[4], callback_data=Piso2[4])],
    [InlineKeyboardButton(Piso2[5], callback_data=Piso2[5])],
    [InlineKeyboardButton(Piso2[6], callback_data=Piso2[6])],
    [InlineKeyboardButton(Piso2[7], callback_data=Piso2[7])],
    [InlineKeyboardButton(Piso2[8], callback_data=Piso2[8])]
])
MENU_P3_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccionde piso", callback_data=str(regresar_piso))],
    [InlineKeyboardButton(Piso3[0], callback_data=Piso3[0])],
    [InlineKeyboardButton(Piso3[1], callback_data=Piso3[1])],
    [InlineKeyboardButton(Piso3[2], callback_data=Piso3[2])],
    [InlineKeyboardButton(Piso3[3], callback_data=Piso3[3])],
    [InlineKeyboardButton(Piso3[4], callback_data=Piso3[4])],
    [InlineKeyboardButton(Piso3[5], callback_data=Piso3[5])],
    [InlineKeyboardButton(Piso3[6], callback_data=Piso3[6])],
    [InlineKeyboardButton(Piso3[7], callback_data=Piso3[7])],
    [InlineKeyboardButton(Piso3[8], callback_data=Piso3[8])]
])
MENU_EX_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de piso", callback_data=str(regresar_piso))],
    [InlineKeyboardButton(Externo[0], callback_data=Externo[0])],
    [InlineKeyboardButton(Externo[1], callback_data=Externo[1])],
    [InlineKeyboardButton(Externo[2], callback_data=Externo[2])],
    [InlineKeyboardButton(Externo[3], callback_data=Externo[3])],

])
MENU_NAME_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de area", callback_data=str(regresar_piso))],
    [InlineKeyboardButton(Nombres[0], callback_data=Nombres[0])],
    [InlineKeyboardButton(Nombres[1], callback_data=Nombres[1])],
    [InlineKeyboardButton(Nombres[2], callback_data=Nombres[2])],
    [InlineKeyboardButton(Nombres[3], callback_data=Nombres[3])],
    [InlineKeyboardButton(Nombres[4], callback_data=Nombres[4])],
    [InlineKeyboardButton(Nombres[5], callback_data=Nombres[5])]
])


MENU_ACTIV_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de usuario", callback_data=str(regresar_nombre))],
    [InlineKeyboardButton(Actividad[0], callback_data=Actividad[0])],
    [InlineKeyboardButton(Actividad[1], callback_data=Actividad[1])],
    [InlineKeyboardButton(Actividad[2], callback_data=Actividad[2])],
    [InlineKeyboardButton(Actividad[3], callback_data=Actividad[3])],
    [InlineKeyboardButton(Actividad[4], callback_data=Actividad[4])],
    [InlineKeyboardButton(Actividad[5], callback_data=Actividad[5])],
    [InlineKeyboardButton(Actividad[6], callback_data=Actividad[6])],
    [InlineKeyboardButton(Actividad[7], callback_data=Actividad[7])],
    [InlineKeyboardButton(Actividad[8], callback_data=Actividad[8])],
    [InlineKeyboardButton(Actividad[9], callback_data=Actividad[9])],
    [InlineKeyboardButton(Actividad[10], callback_data=Actividad[10])]
])


MENU_TT_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("regresar a seleccion de actividad", callback_data=str(regresar_actividad))],
    [InlineKeyboardButton(Tt[0], callback_data=Tt[0])],
    [InlineKeyboardButton(Tt[1], callback_data=Tt[1])],
    [InlineKeyboardButton(Tt[2], callback_data=Tt[2])],
    ])


MENU_COM_MARKUP = InlineKeyboardMarkup([
    #[InlineKeyboardButton("regresar a seleccion de motivo", callback_data=str(regresar))],
    [InlineKeyboardButton("sin comentarios", callback_data=str(com_no))],
    [InlineKeyboardButton("informacion adicional", callback_data=str(com_si))],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    
    await update.message.reply_text("que actividad desea realizar", reply_markup=FIRST_MENU_MARKUP)
    return fase0


async def Spiso(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    
    query = update.callback_query
    await query.answer()
    data1 =query.data
    #print(data1)
    
    texto="escoger el piso donde se dio la atencion"
    #query.answer()
    await query.edit_message_text(
        text=texto, reply_markup=MENU_FLOOR_MARKUP
    )
    
    return fase1


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    data1 =query.data
    
    context.user_data["piso"] = query.data
    markup=MENU_PB_MARKUP
    if data1 == Niveles[0]:#pb
        markup = MENU_PB_MARKUP
    elif data1 == Niveles[1]:#p1
        markup = MENU_P1_MARKUP
    elif data1 == Niveles[2]:#p2
        markup = MENU_P2_MARKUP
    elif data1 == Niveles[3]:#p3
        markup = MENU_P3_MARKUP
    elif data1 == Niveles[4]:#externos
        markup = MENU_EX_MARKUP
    elif data1==str(regresar_inicio):
        #print ("si entro")
        await query.edit_message_text(text="que actividad desea realizar", reply_markup=FIRST_MENU_MARKUP)
        return fase0
    await query.edit_message_text(text="escoja el area donde se dio la atencion", reply_markup=markup)
    return fase2


async def nombre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    data1 =query.data
    
    if data1==str(regresar_piso):
        #print("sie entro en areas")
        await query.edit_message_text(text="seleccionar el piso donde se dio la atencion", reply_markup=MENU_FLOOR_MARKUP)
        return fase1
    context.user_data["area"] = query.data
    await query.edit_message_text(text="escoja el nombre de quien dio la atencion", reply_markup=MENU_NAME_MARKUP)
    return fase3
    

async def actividad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data1 =query.data
    
    if data1==str(regresar_piso):
        #print("nombes")
        await query.edit_message_text(text="escoja el nombre de quien dio la atencion", reply_markup=MENU_FLOOR_MARKUP)
        return fase1
    context.user_data["nombre"] = query.data
    await query.edit_message_text(
        text="escoja la actividad realizada", reply_markup=MENU_ACTIV_MARKUP
    )
    return fase4


async def tt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data1 =query.data
    
    if data1==str(regresar_nombre):
        #print("nombes")
        await query.edit_message_text(text="escoja la actividad realizada", reply_markup=MENU_NAME_MARKUP)
        return fase3
    context.user_data["actividad"] = query.data
    await query.edit_message_text(
        text="esta actividad se realizo bajo.", reply_markup=MENU_TT_MARKUP
    )
    return fase5


async def comentarios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    data1 =query.data
    
    if data1==str(regresar_actividad):
        print("coments")
        await query.edit_message_text(text="seleccionar la actividad realizada", reply_markup=MENU_ACTIV_MARKUP)
        return fase4
    context.user_data["tt"] = query.data
    await query.edit_message_text(
        text="agregar comentario?", reply_markup=MENU_COM_MARKUP
    )
    return fase6

    
async def escribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="agrega tu comentario/ numero de ticket"
    )
    return fase7


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"entendido, hasta pronto!\n{facts_to_str(context.user_data)}")
    context.user_data["comentario"]=""
    Prueba_pandas.Agergar_Linea(facts_to_array(context.user_data))
    context.user_data.clear()
    return ConversationHandler.END


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])
def facts_to_array(user_data: Dict[str, str]):
   
    return list(user_data.values())


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["comentario"]=update.message.text
    await update.message.reply_text(
        f"comentario recibido hasta pronto!\n{facts_to_str(context.user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    Prueba_pandas.Agergar_Linea(facts_to_array(context.user_data))
    context.user_data.clear()
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    await update.message.reply_text(
        f"operacion cancelada!",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    context.user_data.clear()
    return ConversationHandler.END


async def escribe_BUS(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="ingesa la wks a buscar"
    )
    return fase8
# Función para buscar un dato en la base de datos

async def search_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Obtener el dato ingresado por el usuario
    
    user = update.message.from_user
    user_input = update.message.text
    logger.info("User %s ha escrito %s.", user.first_name, user_input)
    # Crear cursor para realizar consultas a la base de datos
    cursor = db.cursor()

    # Consultar si el dato ingresado existe en la base de datos
    query = "SELECT * FROM prueba1 WHERE hostname like '%"+user_input+"%' limit 1"
    logger.info("query ejecutado %s ", query)
    cursor.execute(query)
    result = cursor.fetchone()

    if result is not None:
        # Si se encontró el dato, enviar los datos correspondientes al usuario
        response = f"Los datos para {user_input} son:\n"
        for i in range(len(result)):
            response += f"{cursor.description[i][0]}: {result[i]}\n"
        
    else:
        # Si el dato no se encontró, informar al usuario
        response="no se encotro un resgistro con el host proporcionado"
    await update.message.reply_text(
        response,
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5907090086:AAFHF4xE0e2KCqjY2xRwqwcFpcS9JliZpzI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            fase0:[CallbackQueryHandler( Spiso, pattern="^" + str(bitacora) + "$"),
                CallbackQueryHandler(escribe_BUS, pattern="^" + str(busqueda) + "$"),
                CommandHandler("cancelar", cancelar),
                
                ],
            fase1:[CallbackQueryHandler( area),CommandHandler("cancelar", cancelar)], 
            fase2:[CallbackQueryHandler( nombre),CommandHandler("cancelar", cancelar)], 
            fase3:[CallbackQueryHandler( actividad),CommandHandler("cancelar", cancelar)], 
            fase4:[CallbackQueryHandler( tt),CommandHandler("cancelar", cancelar)],
            fase5:[CallbackQueryHandler( comentarios),CommandHandler("cancelar", cancelar)], 
            fase6:[
                CallbackQueryHandler(escribe, pattern="^" + str(com_si) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(com_no) + "$"),
                CommandHandler("cancelar", cancelar),
                ],
            fase7:[MessageHandler(filters.TEXT, done),CommandHandler("cancelar", cancelar)],
            fase8:[MessageHandler(filters.TEXT, search_data)], 
            
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

