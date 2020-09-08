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
            self.population.append(f" `{row[0]}` *{row[1]}*")
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
                header = "**========================= CARDS DEALT =======================**"
                await message.author.send(header + "\n".join(cards))
            except Exception:
                await message.channel.send("Something went wrong. ~~And that is HEX fault!~~")

        if " update cards" in message.content:
            self.update_lists()
            await message.channel.send("`List of cards has been updated!`")
        if "this is fine" in message.content:
            await message.channel.send("https://tenor.com/view/this-is-fine-fire-coffee-dog-gif-10959043")


client = SaboClient()
client.update_lists()
client.run('NzUyNzc4NDMzODU1MDk0Nzk1.X1cljA.IeBOG_KkcbM9Qb66q0CTqPghJVE')
