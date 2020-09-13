import discord
import random

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
    traps_time = None

    async def on_ready(self):
        print('Logged on as', self.user)
        print(f"Last updated cards: {self.cards_time}")
        print(f"Last updated traps: {self.traps_time}")

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.mentions and message.mentions[0] == client.user:
            if "draw" in message.content:
                amount_of_cards = message.content.split("draw ")[1]
                try:
                    amount_of_cards = int(amount_of_cards)
                    cards = random.choices(self.card_population, weights=self.card_weights, k=amount_of_cards)
                    header = "**========================= CARDS DEALT =======================**\n"
                    await message.author.send(header + "\n".join(cards))
                except Exception:
                    await message.channel.send("Something went wrong. ~~And that is HEX fault!~~")

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


client = SaboClient()
client.card_population, client.card_weights, client.cards_time = update_lists(cards_url)
client.trap_population, client.trap_weights, client.traps_time = update_lists(traps_url)
client.run('NzUyNzc4NDMzODU1MDk0Nzk1.X1cljA.IeBOG_KkcbM9Qb66q0CTqPghJVE')
