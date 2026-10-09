# Bot de Discord con Datos Interesantes y Síntesis de Voz

Bot de Discord mejorado que responde a comandos y proporciona datos interesantes con síntesis de voz, con soporte multiidioma, selección de voz y categorías temáticas.

## Características

- **Comando !start**: Envía un mensaje de bienvenida al usuario
- **Comando !fact**: Obtiene un dato interesante (con API y base de datos local)
- **Comando !lang [es/en]**: Cambia el idioma de los datos (español/inglés)
- **Comando !voice [male/female]**: Cambia el género de la voz (masculino/femenino)
- **Comando !category [general/science/space/history]**: Cambia la categoría de datos
- **Comando !config**: Muestra la configuración actual del bot
- **Síntesis de voz**: El bot vocaliza los mensajes usando pyttsx3

## Instalación

1. Instala las dependencias:
```bash
pip3 install -r requirements.txt
```

2. Crea un archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

3. Edita el archivo `.env` y agrega tu token de Discord:
```
DISCORD_TOKEN=tu_token_aqui
```

## Obtener el Token de Discord

1. Ve a [Discord Developer Portal](https://discord.com/developers)
2. Crea una nueva aplicación o selecciona una existente
3. Ve a la sección "Bot"
4. Crea un bot si no existe uno
5. Copia el token y agrégalo al archivo `.env`

## Ejecutar el Bot

```bash
python3 main.py
```

## Comandos

- `!start` - Muestra un mensaje de bienvenida
- `!fact` - Muestra un dato interesante y lo vocaliza
- `!lang es` - Cambia el idioma a español
- `!lang en` - Cambia el idioma a inglés
- `!voice male` - Cambia la voz a masculina
- `!voice female` - Cambia la voz a femenina
- `!category general` - Datos generales
- `!category science` - Datos de ciencia
- `!category space` - Datos del espacio
- `!category history` - Datos de historia
- `!config` - Muestra la configuración actual

## Notas

- Asegúrate de que el bot tenga los permisos necesarios en tu servidor de Discord
- La síntesis de voz se reproduce en el sistema donde se ejecuta el bot
- La API de hechos puede estar en inglés
