# The following was removed:
# - balance fetching logic (balance defaulted to 10,000)
# - balance adjusting logic

@bot.tree.command(name="rps", description="Play Rock Paper Scissors")
@app_commands.describe(choice="rock, paper, or scissors", amount="Amount to bet")
async def rps(interaction: discord.Interaction, choice: str, amount: int):
    choice = choice.lower()
    options = ["rock", "paper", "scissors"]
    if choice not in options:
        await interaction.response.send_message("Invalid choice. Choose rock, paper, or scissors.", ephemeral=True)
        return

    bal = 10000 # put your balance fetching logic here, original removed
    if amount > bal or amount <= 0:
        await interaction.response.send_message("Invalid bet amount.", ephemeral=True)
        return

    import random
    bot_choice = random.choice(options)

    if choice == bot_choice:
        msg = f"🤝 It's a tie! Both chose {bot_choice}."
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        # put your balance adjusting logic here
        msg = f"🎉 You win! You chose {choice}, I chose {bot_choice}."
    else:
        # put your balance adjusting logic here
        msg = f"💥 You lose! You chose {choice}, I chose {bot_choice}."

    await interaction.response.send_message(f"{msg}")
