import discord
import random


import csv
import requests


class SaboClient(discord.Client):
    population = []
    weights = []

    def update_lists(self):
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRc0bW1RxJc89pcW5Z070Vu4nTHBI9HgWE-VUVf-Ft38e16tj0NuWdLQE3w6Z4wnmCt_ZKSsBXyPxRE/pub?output=csv'
        response = requests.get(url)
        self.population = []
        self.weights = []
        data = response.content.decode("utf-8").splitlines()
        for row in csv.reader(data, delimiter=','):
            self.population.append(f"*{row[0]}* `{row[1]}`")
            self.weights.append(float(row[2]))

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == client.user:
            return
        if "draw" in message.content:
            amount_of_cards = message.content.split("draw ")[1]
            try:
                amount_of_cards = int(amount_of_cards)
                cards = random.choices(self.population, weights=self.weights, k=amount_of_cards)
                await message.author.send("\n".join(cards))
            except Exception as e:
                print(e)
                await message.channel.send("Amount of cards, you dumbo!")

        if " update cards" in message.content:
            self.update_lists()
            await message.channel.send("`List of cards has been updated!`")


client = SaboClient()
client.update_lists()
client.run('NzUyNzc4NDMzODU1MDk0Nzk1.X1cljA.IeBOG_KkcbM9Qb66q0CTqPghJVE')
