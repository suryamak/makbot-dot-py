# -*- coding: utf-8 -*-
"""
A client that challenges and battles users in the Gen 7 1v1 format.
"""
import random
import showdown
import logging
import asyncio
import re

from . import Room, Player, Pokemon

class ChallengeClient(showdown.Client):

    battle_rooms = []
    players = []
    pokemon = []


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
            self.battle_rooms.append(Room(room_id=room_obj.id))
            await self.opening_words(room_obj)
            await self.dt_opp_poke(room_obj)

    async def on_receive(self, room_id, inp_type, params):
        if inp_type in ['player']:
            await self.add_player(room_id, params[0], params[1])
        elif inp_type in ['poke']:
            species, gender = params[1].split(", ")
            self.pokemon.append(Pokemon(room=room_id, player=params[0], species=species, types=[], moves=[], gender=gender, item='unknown'))
        elif inp_type in ['teampreview']:
            await self.rooms[room_id].start_poke(random.choice([1, 2, 3]))
        elif inp_type in ['request']:
            if 'canMegaEvo' in params[0]:
                self.set_mega(room_id, True)
        elif inp_type in ['turn']:
            await asyncio.sleep(1)
            mega = self.get_mega(room_id)
            await self.rooms[room_id].move(random.choice([1, 2, 3, 4]), True if mega else False)
            if mega:
                self.set_mega(room_id, False)
        elif inp_type in ['win']:
            await self.closing_words(room_id, params[0])
        elif inp_type in ['raw']:
            await self.find_typing(room_id, params[0])
        elif inp_type in ['switch']:
            raw_player_id, nickname = params[0].split(': ')
            raw_species = params[1]
            self.set_nickname(raw_player_id, nickname, raw_species)
        elif inp_type in ['move']:
            raw_player_id_user, user = params[0].split(': ')
            move = params[1]
            self.set_move(raw_player_id_user, user, move)
        elif inp_type == 'error':
            await asyncio.sleep(1)
            mega = self.get_mega(room_id)
            await self.rooms[room_id].move(random.choice([1, 2, 3, 4]), True if mega else False)
    
    def set_mega(self, room_id, value):
        for i in range(len(self.battle_rooms)):
            if self.battle_rooms[i].id == room_id:
                self.battle_rooms[i].mega = value

    def get_mega(self, room_id):
        for room in self.battle_rooms:
            if room.id == room_id:
                return room.mega

    def get_primary_player(self, room_id):
        for room in self.battle_rooms:
            if room.id == room_id:
                return room.primary_player

    def set_nickname(self, raw_player_id, nickname, raw_species):
        for i in range(len(self.pokemon)):
            if self.pokemon[i].player in raw_player_id and self.pokemon[i].species in raw_species:
                self.pokemon[i].name = nickname

    def set_move(self, raw_player_id, user, move):
        for i in range(len(self.pokemon)):
            if self.pokemon[i].player in raw_player_id and self.pokemon[i].name == user:
                if move not in self.pokemon[i].moves:
                    self.pokemon[i].moves.append(move)

    async def add_player(self, room_id, player_id, player_name):
        self.players.append(Player(room_id, player_id, player_name))
        if player_name == self.name:
                for i in range(len(self.battle_rooms)):
                    if self.battle_rooms[i].id == room_id:
                        self.battle_rooms[i].primary_player = player_id

    async def opening_words(self, room_obj):
        await room_obj.say('hi im the makbot')
        await asyncio.sleep(1)
        await room_obj.say("glhf")
        await asyncio.sleep(1)

    async def closing_words(self, room_id, raw_data):
        if self.name in raw_data:
            await self.rooms[room_id].say("lol gg")
        else:
            await self.rooms[room_id].say("ggwp")
        await asyncio.sleep(1)
        await self.rooms[room_id].leave()
    
    async def dt_opp_poke(self, room_obj):
        for poke in self.pokemon:
            if poke.player != self.get_primary_player(room_obj.id):
                await room_obj.say('!dt ' + poke.species)
                await asyncio.sleep(1)
    
    async def find_typing(self, room_id, raw_data):
        types = re.findall(r'(?<=_blank">)(\w+)|(?<=alt=")(\w+)', raw_data)
        if len(types) > 0:
            for i in range(len(self.pokemon)):
                if self.pokemon[i].player != self.get_primary_player(room_id):
                    if self.pokemon[i].species == types[0][0]:
                        for match in types[1:]:
                            self.pokemon[i].types.append(match[1])

logging.basicConfig(level=logging.INFO)
with open('./login/login.txt', 'rt') as f,\
     open('./teams/makbot_1v1_v1.txt', 'rt') as team:
    team1v1 = team.read()
    username, password = f.read().strip().splitlines()

client = ChallengeClient(name=username, password=password)
client.start()

print('BATTLE ROOMS')
for room in client.battle_rooms:
    print(room)
print('PLAYERS')
for player in client.players:
    print(player)
print('POKEMON')
for poke in client.pokemon:
    print(poke)