import discord
from discord.ext import commands
from wit import Wit
import discord_speech_recognition as dsr

# Wit.ai access token
WIT_ACCESS_TOKEN = "5PBN3FX4WR7IQRDOVX3LZYXXEC6QJL6I"

# Initialize the bot
bot = commands.Bot(command_prefix="!")
recognizer = dsr.Recognizer()

# Initialize Wit.ai client
wit_client = Wit(WIT_ACCESS_TOKEN)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and not before.channel:
        vc = await after.channel.connect()
        vc.start_listening(dsr.Client(recognizer=recognizer))

@bot.event
async def on_speech(vc, user, audio_data):
    print(f"Audio received from {user}")
    # Send audio data to Wit.ai for recognition
    response = wit_client.speech(audio_data, {'Content-Type': 'audio/wav'})
    
    if response.get('text'):
        text = response['text']
        print(f"Recognized speech: {text}")
        if "hello bot" in text.lower():
            await vc.guild.text_channels[0].send(f"Hello, {user}!")

@bot.command()
async def leave(ctx):
    for vc in bot.voice_clients:
        if vc.guild == ctx.guild:
            await vc.disconnect()
            break

bot.run("OTE2ODA4NTMzMTA4OTk0MTE5.GklUF2.1iStTLDOIPrsSec-4P-FGL6FfQvVMJTEYl7hjw")
