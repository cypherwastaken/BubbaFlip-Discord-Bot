# Make sure to have command.connect.py installed to use this command

@bot.tree.command(name="whois", description="Check a user's connected BubbaFlip profile")
@app_commands.describe(user="User to lookup")
async def whois(interaction: discord.Interaction, user: discord.User):
    try:
        with open("data/connections.json", "r") as f:
            connections = json.load(f)
    except FileNotFoundError:
        connections = {}

    uid = str(user.id)
    if uid not in connections:
        await interaction.response.send_message("That user is not connected to a BubbaFlip account.", ephemeral=True)
        return

    bubba_id = connections[uid]
    profile_link = f"https://bb.zawg.ca/users/{bubba_id}/profile"
    await interaction.response.send_message(f"{user.display_name}'s BubbaFlip profile:\n{profile_link}")
