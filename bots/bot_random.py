# -*- coding: utf-8 -*-
"""
A client that challenges and battles users in any randomized format.
"""
import random
import showdown
import logging
import asyncio


class Room():
    def __init__(self, room_id='', player_id='', mega=False, dynamax=False, switch=False):
        self.id = room_id
        self.primary_player = player_id
        self.mega = mega
        self.dynamax = dynamax
        self.switch = switch
    def print(self):
        output = 'ID: ' + self.id + '\nPrimary Player: ' + self.primary_player + '\nMega Evolution Possible: ' + str(self.mega) + '\nDynamax Possible: ' + str(self.dynamax) + '\n'
        return output

class ChallengeClient(showdown.Client):

    battle_rooms = []
    switch = False

    async def on_private_message(self, pm):
        if pm.recipient == self:
            await pm.author.challenge(None, 'gen8randombattle')

    async def on_challenge_update(self, challenge_data):
        incoming = challenge_data.get('challengesFrom', {})
        for user, tier in incoming.items():
            if 'random' in tier:
                await self.accept_challenge(user, None)

    async def on_room_init(self, room_obj):
        if room_obj.id.startswith('battle-'):
            self.battle_rooms.append(Room(room_id=room_obj.id))
            await self.opening_words(room_obj)

    async def on_receive(self, room_id, inp_type, params):
        if inp_type in ['request']:
            self.set_mega(room_id, 'canMegaEvo' in params[0])
            self.set_dynamax(room_id, 'canDynamax' in params[0])
            if 'forceSwitch' in params[0]:
                self.set_switch(room_id, True)
                await self.rooms[room_id].switch(random.choice([1, 2, 3, 4, 5, 6]))
        elif inp_type in ['turn']:
            await asyncio.sleep(1)
            self.set_switch(room_id, False)
            mega = self.get_mega(room_id)
            dynamax = self.get_dynamax(room_id)
            await self.rooms[room_id].move(random.choice([1, 2, 3, 4]), mega, dynamax)
        elif inp_type in ['win']:
            await self.closing_words(room_id, params[0])
        elif inp_type == 'error':
            await asyncio.sleep(1)
            if self.get_switch(room_id):
                await self.rooms[room_id].switch(random.choice([1, 2, 3, 4, 5, 6]))
            else:
                mega = self.get_mega(room_id)
                dynamax = self.get_dynamax(room_id)
                await self.rooms[room_id].move(random.choice([1, 2, 3, 4]), mega, dynamax)
    
    
    def set_switch(self, room_id, value):
        for i in range(len(self.battle_rooms)):
            if self.battle_rooms[i].id == room_id:
                self.battle_rooms[i].switch = value

    def get_switch(self, room_id):
        for room in self.battle_rooms:
            if room.id == room_id:
                return room.switch
    
    def set_mega(self, room_id, value):
        for i in range(len(self.battle_rooms)):
            if self.battle_rooms[i].id == room_id:
                self.battle_rooms[i].mega = value

    def get_mega(self, room_id):
        for room in self.battle_rooms:
            if room.id == room_id:
                return room.mega

    def set_dynamax(self, room_id, value):
        for i in range(len(self.battle_rooms)):
            if self.battle_rooms[i].id == room_id:
                self.battle_rooms[i].dynamax = value

    def get_dynamax(self, room_id):
        for room in self.battle_rooms:
            if room.id == room_id:
                return room.dynamax

    def get_primary_player(self, room_id):
        for room in self.battle_rooms:
            if room.id == room_id:
                return room.primary_player

    async def opening_words(self, room_obj):
        await room_obj.say('hi im the makbot, I pick moves at random and hope for the best')
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

logging.basicConfig(level=logging.INFO)
with open('./login/login.txt', 'rt') as f,\
     open('./teams/makbot_1v1_v1.txt', 'rt') as team:
    team1v1 = team.read()
    username, password = f.read().strip().splitlines()

client = ChallengeClient(name=username, password=password)
client.start()
client.upload_team(None)