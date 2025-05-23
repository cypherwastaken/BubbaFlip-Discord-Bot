# balance was defaulted to 10,000 and the following was removed:
# - fetching balance logic
# - adjusting balance logic

@bot.tree.command(name="roulette", description="Play roulette (red, black, green)")
@app_commands.describe(color="red, black, or green", amount="Amount to bet")
async def roulette(interaction: discord.Interaction, color: str, amount: int):
    color = color.lower()
    if color not in ["red", "black", "green"]:
        await interaction.response.send_message("Invalid color. Choose red, black, or green.", ephemeral=True)
        return

    bal = 10000 # put your balance fetching logic here, original removed
    if amount > bal or amount <= 0:
        await interaction.response.send_message("Invalid bet amount.", ephemeral=True)
        return

    import random
    roll = random.randint(0, 36)
    result = "green" if roll == 0 else "red" if roll % 2 == 0 else "black"

    if result == color:
        if color == "green":
            winnings = amount * 14
        else:
            winnings = amount * 2
        # put your adjust balance logic here
        msg = f"🎉 It landed on {result}! You won {winnings} R$."
    else:
        # put your adjust balance logic here
        msg = f"💥 It landed on {result}. You lost {amount} R$."

    await interaction.response.send_message(f"{msg}")
