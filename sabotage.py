import discord
import random


import csv
import requests


class SaboClient(discord.Client):
    async def __init__(self):
        self.population = []
        self.weights = []
        await self.update_lists()

    async def update_lists(self):
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRc0bW1RxJc89pcW5Z070Vu4nTHBI9HgWE-VUVf-Ft38e16tj0NuWdLQE3w6Z4wnmCt_ZKSsBXyPxRE/pub?output=csv'
        response = requests.get(url)
        data = response.content.decode("utf-8").splitlines()
        for row in csv.reader(data, delimiter=','):
            self.population.append(f"*{row[0]}* `{row[1]}`")

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if "draw" in message.content:
            amount_of_cards = message.content.split("draw ")[1]
            try:
                amount_of_cards = int(amount_of_cards)
            except Exception:
                message.channel.send("Amount of cards, you dumbo!")

            cards = random.choices(self.population, weights=self.weights, k=amount_of_cards)
            await message.author.send("\n".join(cards))
        if "update" in message.content:
            self.update_lists()
            message.channel.send("`List of cards has been updated!`")


client = SaboClient()
client.run('NzUyNzc4NDMzODU1MDk0Nzk1.X1cljA.IeBOG_KkcbM9Qb66q0CTqPghJVE')
