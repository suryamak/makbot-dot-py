# -*- coding: utf-8 -*-
"""
A client that challenges and battles users in the Gen 7 1v1 format.
"""
import random
import showdown
import logging
import asyncio
import re


class Pokemon():
    def __init__(self, name='', type=[], gender='', moves=[], item=''):
        self.name = name
        self.type = type
        self.gender = gender
        self.moves = moves
        self.item = item

class ChallengeClient(showdown.Client):

    players = {}
    mega = False

    async def on_private_message(self, pm):
        if pm.recipient == self:
            await pm.author.challenge(team1v1, '1v1')

    async def on_challenge_update(self, challenge_data):
        incoming = challenge_data.get('challengesFrom', {})
        for user, tier in incoming.items():
            if 'random' in tier:
                await self.accept_challenge(user, 'null')
            if '1v1' in tier:
                await self.accept_challenge(user, team1v1)

    async def on_room_init(self, room_obj):
        if room_obj.id.startswith('battle-'):
            await asyncio.sleep(3)
            await room_obj.say('hi im the makbot')
            await asyncio.sleep(1)
            await room_obj.say("glhf")
            await asyncio.sleep(1)
            for player in self.players:
                if self.players[player]['name'] != 'makbotdotpy':
                    for poke in self.players[player]['pokemon']:
                        await room_obj.say("!dt " + poke['name'])
                        await asyncio.sleep(1)

    async def on_receive(self, room_id, inp_type, params):
        if inp_type in ['player']:
            self.players[params[0]] = {'name': params[1], 'pokemon': []}
        elif inp_type in ['poke']:
            name, gender = params[1].split(", ")
            poke = {'name': name, 'type': [], 'gender': gender, 'moves': [], 'item': ''}
            # self.players[params[0]].append(Pokemon(name=name, gender=gender))
            self.players[params[0]]['pokemon'].append(poke)
        elif inp_type in ['teampreview']:
            await self.rooms[room_id].start_poke(random.choice([1, 2, 3]))
        elif inp_type in ['request']:
            await asyncio.sleep(1)
            if 'canMegaEvo' in params[0]:
                self.mega = True
        elif inp_type in ['turn']:
            await asyncio.sleep(1)
            await self.rooms[room_id].move(random.choice([1, 2, 3, 4]), True if self.mega else False)
            if self.mega:
                self.mega = False
        elif inp_type in ['win']:
            if 'makbotdotpy' in params[0]:
                await self.rooms[room_id].say("lol gg")
            else:
                await self.rooms[room_id].say("ggwp")
            await asyncio.sleep(1)
            await self.rooms[room_id].leave()
        elif inp_type in ['raw']:
            types = re.findall(r'(?<=_blank">)(\w+)|(?<=alt=")(\w+)', params[0])
            if len(types) > 0:
                for player in self.players:
                    if self.players[player]['name'] != 'makbotdotpy':
                        for i in range(len(self.players[player]['pokemon'])):
                            if self.players[player]['pokemon'][i]['name'] in types[0]:
                                for match in types[1:]:
                                    self.players[player]['pokemon'][i]['type'].append(match[1])
                                await self.rooms[room_id].say(self.players[player]['pokemon'][i])
        elif inp_type in ['switch']:
            await self.rooms[room_id].say("[debug] a pokemon has switched in")
            

logging.basicConfig(level=logging.INFO)
with open('./login/login.txt', 'rt') as f,\
     open('./teams/makbot_1v1_v1.txt', 'rt') as team:
    team1v1 = team.read()
    username, password = f.read().strip().splitlines()

ChallengeClient(name=username, password=password).start()
