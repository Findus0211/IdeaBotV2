import discord
from discord import app_commands
import random

# --- CONFIGURATION ---
# PASTE YOUR TOKEN BETWEEN THE QUOTES BELOW
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# --- IDEA DATABASE ---
# You can add more categories here by following the format: "name": ["idea", "idea"],
IDEAS_DB = {
    "general": [
        "A 'Day in the Life' vlog.",
        "Reviewing a product you use every day.",
        "A tutorial on a skill you recently learned.",
        "Reacting to your old videos.",
        "Interviewing someone with an interesting job.",
        "A 'Tier List' of your favorite movies/games/foods.",
        "Behind the scenes of your setup.",
        "Answering subscriber Q&A.",
        "Testing a viral life hack to see if it works."
    ],
    "f1": [
        "Predicting the next race podium.",
        "Analyzing a controversial crash from the last GP.",
        "Tier ranking all current F1 liveries.",
        "Explaining a complex F1 rule (like Safety Car restarts).",
        "A history of a specific track.",
        "Driver transfer rumors and predictions.",
        "Who is the greatest driver of all time?"
    ],
    "gaming": [
        "A 'Let's Play' of a horror game.",
        "Speedrunning a short game.",
        "Gaming highlights compilation.",
        "Reviewing an indie game nobody talks about.",
        "Challenging a friend to a 1v1.",
        "Trying to beat a game without taking damage."
    ],
    "math": [
        "Explaining the Golden Ratio in simple terms.",
        "Solving a viral math problem from the internet.",
        "The history of Pi and why it matters.",
        "Visualizing 4th dimension shapes.",
        "Math paradoxes that will break your brain.",
        "How probability works in real life (lottery, etc)."
    ],
    "science": [
        "Kitchen chemistry experiments you can do at home.",
        "Explaining the physics of a black hole.",
        "Microscope video: Looking at everyday objects up close.",
        "The science behind how specific gadgets work.",
        "Debunking common scientific myths.",
        "Time-lapse of a plant growing."
    ],
    "coding": [
        "Coding a Discord bot from scratch.",
        "Python vs Java: Which is better for beginners?",
        "Automating a boring task with code.",
        "Reviewing your very first code project.",
        "Speed coding challenge: Build a website in 10 minutes."
    ],
    "cooking": [
        "Cooking a 3-ingredient meal.",
        "Trying to follow a recipe from 100 years ago.",
        "Fast food vs Homemade: Which tastes better?",
        "Cooking with a budget of only $5.",
        "Gordon Ramsay reaction video."
    ],
    "history": [
        "The true story behind a famous historical event.",
        "Biography of a forgotten historical figure.",
        "Timeline of World War 1 explained.",
        "Ancient technologies we still don't understand.",
        "Reacting to historical inaccuracies in movies."
    ]
}

# --- BOT SETUP ---
class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synced!")

client = Client()

# --- COMMANDS ---

@client.tree.command(name="idea", description="Get a video idea. Categories: Math, Science, F1, Gaming, Cooking...")
@app_commands.describe(category="Type a category (e.g. Math) or leave empty for random")
async def idea(interaction: discord.Interaction, category: str = None):
    
    # 1. If no category is typed, pick from "general"
    if category is None:
        selected_idea = random.choice(IDEAS_DB["general"])
        # We also pick a random emoji for flair
        emoji = random.choice(["💡", "🎥", "🎬", "✨"])
        response_text = f"{emoji} **General Idea:** {selected_idea}"

    # 2. If a category IS typed
    else:
        # Convert user input to lowercase so "Math" and "math" both work
        cat_clean = category.lower().strip()

        # Check if the category exists in our database
        if cat_clean in IDEAS_DB:
            selected_idea = random.choice(IDEAS_DB[cat_clean])
            
            # Add specific emojis based on category
            emoji_map = {
                "f1": "🏎️", "gaming": "🎮", "math": "🧮", 
                "science": "🧪", "coding": "💻", "cooking": "🍳", "history": "📜"
            }
            # Get the emoji, default to star if not found
            emoji = emoji_map.get(cat_clean, "🌟") 
            
            response_text = f"{emoji} **{category.capitalize()} Idea:** {selected_idea}"
        
        # 3. If category is not found
        else:
            # Create a nice list of available categories to show the user
            available_cats = ", ".join([key.capitalize() for key in IDEAS_DB.keys()])
            response_text = (f"❌ I don't have ideas for **'{category}'** yet.\n"
                             f"📂 **Try one of these:** {available_cats}")

    await interaction.response.send_message(response_text)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

client.run(BOT_TOKEN)
