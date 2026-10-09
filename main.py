import os
import random
import ssl
from typing import Dict, List, Optional

import discord
import pyttsx3
import requests
from discord.ext import commands
from dotenv import load_dotenv

# Desactivar verificación SSL (solo para desarrollo)
ssl._create_default_https_context = ssl._create_unverified_context

# Cargar variables de entorno
load_dotenv()

# Constantes
PREFIJO_COMANDO = "!"
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN", "TU_TOKEN_AQUI")
API_URL = "https://uselessfacts.jsph.pl/random.json"

IDIOMAS_VALIDOS = {"es", "en"}
GENEROS_VOZ = {"male", "female"}
CATEGORIAS_VALIDAS = {"general", "science", "space", "history"}

NOMBRES_CATEGORIAS = {
    "general": {"es": "general", "en": "general"},
    "science": {"es": "ciencia", "en": "science"},
    "space": {"es": "espacio", "en": "space"},
    "history": {"es": "historia", "en": "history"},
}

# Base de datos de datos curiosos locales
DATOS_LOCALES = {
    "es": {
        "space": [
            "El Sol representa el 99.86% de la masa total del sistema solar.",
            "La Vía Láctea tiene entre 100 y 400 mil millones de estrellas.",
            "Un día en Venus es más largo que un año en Venus.",
            "El espacio es completamente silencioso porque no hay atmósfera.",
            "La estrella más grande conocida es UY Scuti, 1700 veces más grande que el Sol.",
        ],
        "history": [
            "La Gran Muralla China es la estructura más larga jamás construida por humanos.",
            "Los egipcios usaban miel como medicina hace 4000 años.",
            "La primera computadora pesaba 27 toneladas y ocupaba una habitación entera.",
            "Cleopatra vivió más cerca de la invención del iPhone que de la construcción de la Gran Pirámide.",
            "El código morse fue inventado en la década de 1830.",
        ],
        "science": [
            "El agua se expande cuando se congela, a diferencia de la mayoría de los líquidos.",
            "El cerebro humano usa el 20% de la energía total del cuerpo.",
            "La miel nunca se echa a perder; los arqueólogos encontraron miel de 3000 años en tumbas egipcias.",
            "El ADN es el mismo en cada célula de tu cuerpo.",
            "El cuerpo humano contiene suficiente hierro para hacer un clavo de 3 pulgadas.",
        ],
    },
    "en": {
        "space": [
            "The Sun accounts for 99.86% of the total mass of the solar system.",
            "The Milky Way has between 100 and 400 billion stars.",
            "A day on Venus is longer than a year on Venus.",
            "Space is completely silent because there is no atmosphere.",
            "The largest known star is UY Scuti, 1700 times larger than the Sun.",
        ],
        "history": [
            "The Great Wall of China is the longest structure ever built by humans.",
            "Egyptians used honey as medicine 4000 years ago.",
            "The first computer weighed 27 tons and occupied an entire room.",
            "Cleopatra lived closer to the invention of the iPhone than to the construction of the Great Pyramid.",
            "Morse code was invented in the 1830s.",
        ],
        "science": [
            "Water expands when it freezes, unlike most other liquids.",
            "The human brain uses 20% of the body's total energy.",
            "Honey never spoils; archaeologists found 3000-year-old honey in Egyptian tombs.",
            "DNA is the same in every cell of your body.",
            "The human body contains enough iron to make a 3-inch nail.",
        ],
    },
}


class ConfiguracionBot:
    """
    Clase para gestionar la configuración del bot.
    """

    def __init__(self):
        self.idioma = "es"
        self.genero_voz = "female"
        self.categoria = "general"

    def cambiar_idioma(self, idioma: str) -> bool:
        """
        Cambia el idioma si es válido.
        """
        if idioma in IDIOMAS_VALIDOS:
            self.idioma = idioma
            return True
        return False

    def cambiar_genero_voz(self, genero: str) -> bool:
        """
        Cambia el género de voz si es válido.
        """
        if genero in GENEROS_VOZ:
            self.genero_voz = genero
            return True
        return False

    def cambiar_categoria(self, categoria: str) -> bool:
        """
        Cambia la categoría si es válida.
        """
        if categoria in CATEGORIAS_VALIDAS:
            self.categoria = categoria
            return True
        return False

    def obtener_configuracion(self) -> str:
        """
        Retorna la configuración actual como texto.
        """
        return (
            f"Configuración actual:\n"
            f"🌐 Idioma: {self.idioma}\n"
            f"🎙️ Voz: {self.genero_voz}\n"
            f"📚 Categoría: {self.categoria}"
        )


class MotorVoz:
    """
    Clase para gestionar la síntesis de voz.
    """

    def __init__(self):
        self.engine = pyttsx3.init()

    def configurar_voz(self, genero: str):
        """
        Configura la voz según el género seleccionado.
        """
        voices = self.engine.getProperty("voices")
        if genero == "female":
            for voice in voices:
                if "female" in voice.name.lower() or "mujer" in voice.name.lower():
                    self.engine.setProperty("voice", voice.id)
                    return
        if voices:
            self.engine.setProperty("voice", voices[0].id)

    def hablar(self, texto: str):
        """
        Vocaliza el texto proporcionado.
        """
        try:
            self.configurar_voz(configuracion.genero_voz)
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error al hablar: {e}")


class GeneradorDatos:
    """
    Clase para generar datos curiosos.
    """

    @staticmethod
    def obtener_dato_local(idioma: str, categoria: str) -> Optional[str]:
        """
        Obtiene un dato de la base de datos local.
        """
        if idioma in DATOS_LOCALES and categoria in DATOS_LOCALES[idioma]:
            return random.choice(DATOS_LOCALES[idioma][categoria])
        return None

    @staticmethod
    def obtener_dato_api(idioma: str) -> Optional[str]:
        """
        Obtiene un dato de la API externa.
        """
        try:
            response = requests.get(f"{API_URL}?language={idioma}")
            if response.status_code == 200:
                data = response.json()
                return data.get("text")
            return None
        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            return None

    @staticmethod
    def generar_dato(idioma: str, categoria: str) -> str:
        """
        Genera un dato curioso usando API o base de datos local.
        """
        if categoria == "general":
            dato_api = GeneradorDatos.obtener_dato_api(idioma)
            if dato_api:
                return dato_api
            return "No se pudo obtener el dato de la API"

        dato_local = GeneradorDatos.obtener_dato_local(idioma, categoria)
        if dato_local:
            return dato_local

        return "Categoría no disponible"


# Inicialización
configuracion = ConfiguracionBot()
motor_voz = MotorVoz()

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIJO_COMANDO, intents=intents)


@bot.event
async def on_ready():
    """
    Evento que se ejecuta cuando el bot se conecta.
    """
    print(f"Bot conectado como {bot.user.name}")


@bot.command()
async def start(ctx: commands.Context):
    """
    Envía un mensaje de bienvenida.
    """
    mensaje_bienvenida = (
        f"¡Hola {ctx.author.name}! Bienvenido al servidor. "
        f"¡Usa !fact para obtener un dato interesante!"
    )
    await ctx.send(mensaje_bienvenida)
    motor_voz.hablar(mensaje_bienvenida)


@bot.command()
async def fact(ctx: commands.Context):
    """
    Envía un hecho interesante.
    """
    dato = GeneradorDatos.generar_dato(configuracion.idioma, configuracion.categoria)
    await ctx.send(f"🧠 Dato interesante: {dato}")
    motor_voz.hablar(dato)


@bot.command()
async def lang(ctx: commands.Context, idioma: Optional[str] = None):
    """
    Cambia el idioma de los datos.
    """
    if idioma and configuracion.cambiar_idioma(idioma.lower()):
        nombre_idioma = "español" if configuracion.idioma == "es" else "inglés"
        mensaje = f"Idioma cambiado a {nombre_idioma}"
        await ctx.send(f"🌐 {mensaje}")
        motor_voz.hablar(mensaje)
    else:
        await ctx.send("Uso: !lang es o !lang en")


@bot.command()
async def voice(ctx: commands.Context, genero: Optional[str] = None):
    """
    Cambia el género de la voz.
    """
    if genero and configuracion.cambiar_genero_voz(genero.lower()):
        nombre_voz = "masculina" if configuracion.genero_voz == "male" else "femenina"
        mensaje = f"Voz cambiada a {nombre_voz}"
        await ctx.send(f"🎙️ {mensaje}")
        motor_voz.hablar(mensaje)
    else:
        await ctx.send("Uso: !voice male o !voice female")


@bot.command()
async def category(ctx: commands.Context, categoria: Optional[str] = None):
    """
    Cambia la categoría de datos.
    """
    if categoria and configuracion.cambiar_categoria(categoria.lower()):
        nombre_categoria = NOMBRES_CATEGORIAS[configuracion.categoria][configuracion.idioma]
        mensaje = f"Categoría cambiada a {nombre_categoria}"
        await ctx.send(f"📚 {mensaje}")
        motor_voz.hablar(mensaje)
    else:
        await ctx.send(f"Uso: !category {'/'.join(sorted(CATEGORIAS_VALIDAS))}")


@bot.command()
async def config(ctx: commands.Context):
    """
    Muestra la configuración actual.
    """
    await ctx.send(configuracion.obtener_configuracion())
    motor_voz.hablar(
        f"Idioma {configuracion.idioma}, "
        f"voz {configuracion.genero_voz}, "
        f"categoría {configuracion.categoria}"
    )


if __name__ == "__main__":
    bot.run(TOKEN_DISCORD)