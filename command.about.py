# Create the following files:
# data\pendingconnections.json
# data\connections.json
@bot.tree.command(name="connect", description="Connect your BubbaBlox account")
@app_commands.describe(username="Your BubbaFlip username")
async def connect(interaction: discord.Interaction, username: str):
    import aiohttp
    import random

    phrases = ["taco winter rocket boost", "glow panda banana tree", "rainbow turbo guitar flip", "mango echo jungle storm"]
    chosen_phrase = random.choice(phrases)

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        search_url = f"https://bb.zawg.ca/search/users/results?keyword={username}&maxRows=1&startIndex=0"
        async with session.get(search_url) as resp:
            data = await resp.json()
            if not data["UserSearchResults"]:
                await interaction.response.send_message("User not found.", ephemeral=True)
                return
            user_id = data["UserSearchResults"][0]["UserId"]

        profile_url = f"https://bb.zawg.ca/apisite/users/v1/users/{user_id}"
        async with session.get(profile_url) as resp:
            user_data = await resp.json()

    embed = discord.Embed(
        title="Connect to BubbaFlip",
        description=f"Set your description to this phrase:\n```{chosen_phrase}```\nReact when complete.",
        color=discord.Color.green()
    )
    message = await interaction.user.send(embed=embed)
    await message.add_reaction("⭐")

    with open("data/pendingconnections.json", "r") as f:
        pending = json.load(f)
    pending[str(interaction.user.id)] = {"userid": user_id, "phrase": chosen_phrase}
    with open("data/pendingconnections.json", "w") as f:
        json.dump(pending, f)

    await interaction.response.send_message("Check your DMs to complete connection.", ephemeral=True)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message.author != bot.user:
        return
    if str(reaction.emoji) != "⭐":
        return

    try:
        with open("data/pendingconnections.json", "r") as f:
            pending = json.load(f)
    except FileNotFoundError:
        return

    pending_entry = pending.get(str(user.id))
    if not pending_entry:
        return

    import aiohttp
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        url = f"https://bb.zawg.ca/apisite/users/v1/users/{pending_entry['userid']}"
        async with session.get(url) as resp:
            data = await resp.json()

    if data.get("description") == pending_entry["phrase"]:
        try:
            with open("data/connections.json", "r") as f:
                connections = json.load(f)
        except FileNotFoundError:
            connections = {}

        connections[str(user.id)] = pending_entry["userid"]
        with open("data/connections.json", "w") as f:
            json.dump(connections, f)

        await reaction.message.channel.send("✅ Successfully connected your BubbaFlip account!")
    else:
        await reaction.message.channel.send(f"❌ Failed to connect to `{data.get('name')}`")

    pending.pop(str(user.id))
    with open("data/pendingconnections.json", "w") as f:
        json.dump(pending, f)
