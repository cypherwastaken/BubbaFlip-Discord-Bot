# The userbalance is defaulted to 10,000 and does not include the adjust balance logic

@bot.tree.command(name="slots", description="Spin the slot machine")
@app_commands.describe(amount="Amount to bet")
async def slots(interaction: discord.Interaction, amount: int):
    bal = 10000 # Input your logic to get a users balance here, original was removed
    if amount > bal or amount <= 0:
        await interaction.response.send_message("Invalid bet amount.", ephemeral=True)
        return

    import random
    symbols = [":cherries:", ":lemon:", ":seven:", ":bell:", ":gem:"]
    result = [random.choice(symbols) for _ in range(3)]
    win = False
    multiplier = 0

    if result.count(result[0]) == 3:
        multiplier = 10
        win = True
    elif result.count(result[0]) == 2 or result.count(result[1]) == 2:
        multiplier = 2
        win = True
    if win:
        winnings = amount * multiplier
        # put your adjust balance logic here
        msg = f"{' '.join(result)} - You won {winnings} R$!"
    else:
        # put your adjust balance logic here
        msg = f"{' '.join(result)} - You lost {amount} R$."

    await interaction.response.send_message(f"{msg}")
