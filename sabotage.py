import discord
import random


import csv
import requests

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRc0bW1RxJc89pcW5Z070Vu4nTHBI9HgWE-VUVf-Ft38e16tj0NuWdLQE3w6Z4wnmCt_ZKSsBXyPxRE/pub?output=csv'
response = requests.get(url)
data = response.content.decode("utf-8").splitlines()
population = []
weights = []
for row in csv.reader(data, delimiter=','):
    population.append(f"*{row[0]}* `{row[1]}`")
    weights.append(float(row[2]))


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        print(message)
        if "draw" in message.content:
            amount_of_cards = message.content.split("draw ")[1]
            try:
                amount_of_cards = int(amount_of_cards)
            except Exception:
                print(message.content)

            cards = random.choices(population, weights=weights, k=amount_of_cards)
            await message.author.send("\n".join(cards))


client = MyClient()
client.run('NzUyNzc4NDMzODU1MDk0Nzk1.X1cljA.IeBOG_KkcbM9Qb66q0CTqPghJVE')
