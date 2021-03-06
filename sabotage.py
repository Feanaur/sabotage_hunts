import discord
import random
import os
import csv
import requests

cards_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRc0bW1RxJc89pcW5Z070Vu4nTHBI9HgWE-VUVf-Ft38e16tj0NuWdLQE3w6Z4wnmCt_ZKSsBXyPxRE/pub?output=csv'
traps_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT6cFlWuzmbZ_dSlCilXnpN7Tz9TE5u39G3PyQ2khXQooAnguVg9PceALSXmurGiyppYGNAPJ3FNpSg/pub?output=csv"


def update_lists(url):
    cards_response = requests.get(url)
    population = []
    weights = []
    time = None
    data = cards_response.content.decode("utf-8").splitlines()
    for index, row in enumerate(csv.reader(data, delimiter=',')):
        if index == 0:
            time = row[3]
        population.append(f" `{row[0]}` *{row[1]}*")
        weights.append(float(row[2]))
    return population, weights, time


class SaboClient(discord.Client):
    card_population = []
    card_weights = []
    trap_population = []
    trap_weights = []
    cards_time = None
    monday_switch = False
    traps_time = None

    async def on_ready(self):
        print('Logged on as', self.user)
        print(f"Last updated cards: {self.cards_time}")
        print(f"Last updated traps: {self.traps_time}")

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.mentions and message.mentions[0] == client.user:
            if "turn on monday" in message.content:
                self.monday_switch = True
            if "turn off monday" in message.content:
                self.monday_switch = False
            if "draw" in message.content:
                if self.monday_switch:
                    amount_of_cards = message.content.split("draw ")[1]
                    try:
                        amount_of_cards = int(amount_of_cards)
                        cards = random.choices(self.card_population, weights=self.card_weights, k=amount_of_cards)
                        header = "**========================= CARDS DEALT =======================**\n"
                        await message.author.send(header + "\n".join(cards))
                    except Exception:
                        await message.channel.send("Something went wrong. ~~And that is HEX fault!~~")
                else:
                    await message.channel.send("https://tenor.com/view/monkey-with-money-happy-withmoney-swag-dollars-more-money-gif-14116367")

            if " update cards" in message.content:
                self.card_population, self.card_weights, self.cards_time = update_lists(cards_url)
                self.trap_population, self.trap_weights, self.traps_time = update_lists(traps_url)
                await message.channel.send(f"```List of cards has been updated!\nCards last updated: {self.cards_time}\nTraps last updated: {self.cards_time}```")
            if " roll trap for " in message.content and len(message.mentions) > 1:
                cards = random.choices(self.trap_population, weights=self.trap_weights, k=1)
                header = "**---------------------- YOUR TRAP CARD ------------------------**\n"
                for mention in message.mentions[1:]:
                    await mention.send(header + "\n".join(cards))
            if "roll out of " in message.content:
                max_roll = message.content.split("roll out of ")[1]
                try:
                    max_roll = int(max_roll)
                    roll = random.choice(range(1, max_roll))
                    await message.channel.send(f"You rolled {roll}.")
                except Exception:
                    await message.channel.send("Something went wrong. ~~And that is HEX fault!~~")

        if "this is fine" in message.content:
            await message.channel.send("https://tenor.com/view/this-is-fine-fire-coffee-dog-gif-10959043")
        if "Why u hate me" in message.content:
            random_hate_me_gif = random.choice([
                "https://media.discordapp.net/attachments/761784276714389535/789457045480538163/image0.gif",
                "https://tenor.com/view/borgar-02-nom-cheeseburger-day-hungry-gif-15074926",
                "https://media.discordapp.net/attachments/585278697720905729/803645754517749760/image0.gif",
                "https://media.discordapp.net/attachments/772351531491262504/782305412828626944/image2.gif",
                "https://media.discordapp.net/attachments/771737019784626196/797878593861845052/image0.gif",
                "https://media.discordapp.net/attachments/772351531491262504/782305412317577236/image1.gif",
                "https://media.discordapp.net/attachments/772351531491262504/784404304022077460/image0.gif",
                "https://media.discordapp.net/attachments/772351531491262504/787136736261570590/image0.gif",
                "https://media.discordapp.net/attachments/771737019784626196/788101150905860096/image0.gif",
                "https://media.discordapp.net/attachments/788584127938428929/794268113490673684/image0.gif",
            ])
            await message.channel.send(random_hate_me_gif)


client = SaboClient()
client.card_population, client.card_weights, client.cards_time = update_lists(cards_url)
client.trap_population, client.trap_weights, client.traps_time = update_lists(traps_url)
client.run(os.getenv("DISCORD_TOKEN"))
