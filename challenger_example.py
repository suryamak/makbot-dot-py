# -*- coding: utf-8 -*-
"""
An example client that challenges a player to
a random battle when PM'd, or accepts any
random battle challenge.
"""
import random
import showdown
import logging
import asyncio
from pprint import pprint

logging.basicConfig(level=logging.INFO)
with open('./txt/login.txt', 'rt') as f,\
     open('./txt/makbot_1v1_v1.txt', 'rt') as team:
    team1v1 = team.read()
    username, password = f.read().strip().splitlines()

class ChallengeClient(showdown.Client):
    # async def log(self, data):
    #      self.logger.debug(data)

    # async def on_login(self, login_response):
    #      await self.log(login_response)
    players = {}
    mega = False

    async def on_private_message(self, pm):
        if pm.recipient == self:
            # await self.cancel_challenge()
            await pm.author.challenge(team1v1, '1v1')
            # self.logger.debug("challenge sent")

    async def on_challenge_update(self, challenge_data):
        incoming = challenge_data.get('challengesFrom', {})
        for user, tier in incoming.items():
            if 'random' in tier:
                await self.accept_challenge(user, 'null')
            if '1v1' in tier:
                await self.accept_challenge(user, team1v1)
                # self.logger.debug("challenge accepted")

    async def on_room_init(self, room_obj):
        if room_obj.id.startswith('battle-'):
            await asyncio.sleep(3)
            await room_obj.say('hi im the makbot')
            # await asyncio.sleep(3)
            # await print("message sent")
            await asyncio.sleep(1)
            await room_obj.say("glhf")
            # await asyncio.sleep(3)
            # await print("message sent")
            # self.logger.debug("message sent")
            # await room_obj.forfeit()
            await asyncio.sleep(1)
            # await room_obj.leave()

    async def on_receive(self, room_id, inp_type, params):
        # print("ayylmao:", inp_type, params)
        if inp_type in ['player']:
            # await self.rooms[room_id].say("debug")
            # await asyncio.sleep(1)
            self.players[params[0]] = []
            await self.rooms[room_id].say("PLAYER UPDATE:" + str(self.players))
            await asyncio.sleep(1)
        elif inp_type in ['poke']:
            # await self.rooms[room_id].say("debug")
            # await asyncio.sleep(1)
            self.players[params[0]].append(params[1:])
            await self.rooms[room_id].say("POKE UPDATE:" + str(self.players))
            await asyncio.sleep(1)
            # try:
            #     print("AYYLMAO: ", inp_type, params)
            # except:
            #     pass
            # if inp_type is 'teampreview':
            #     await self.rooms[room_id].say("debug")
            #     await self.rooms[room_id].set_timer_on()
            #     # change this to switch pokemon
        elif inp_type in ['teampreview']:
            # await self.rooms[room_id].set_timer_on()
            # await asyncio.sleep(1)
            await self.rooms[room_id].start_poke(random.choice([1, 2, 3]))
            # await asyncio.sleep(1)
            # await self.rooms[room_id].start_poke(2)
        elif inp_type in ['request']:
            # await self.rooms[room_id].say(params[0])
            await asyncio.sleep(1)
            if 'canMegaEvo' in params[0]:
                self.mega = True
                # await self.rooms[room_obj].move(random.choice([1, 2, 3, 4]), True)
        elif inp_type in ['turn']:
            await self.rooms[room_id].say(self.mega)
            await asyncio.sleep(1)
            await self.rooms[room_id].move(random.choice([1, 2, 3, 4]), True if self.mega else False)
            if self.mega:
                self.mega = False
        # else:
        #     await self.rooms[room_obj].say("oof")

ChallengeClient(name=username, password=password).start()
# >> battle-gen7pu-944333225|/team 123456|2
# >> battle-gen7ru-944334464|/team 321456|3
# >> battle-gen7uu-944337541|/team 321456|2

# request ['{"active":[{"moves":[{"move":"Substitute","id":"substitute","pp":16,"maxpp":16,"target":"self","disabled":false},{"move":"Toxic","id":"toxic","pp":15,"maxpp":16,"target":"normal","disabled":false},{"move":"Leech Seed","id":"leechseed","pp":16,"maxpp":16,"target":"normal","disabled":false},{"move":"Leaf Storm","id":"leafstorm","pp":8,"maxpp":8,"target":"normal","disabled":false}]}],"side":{"name":"makbotdotpy","id":"p1","pokemon":[{"ident":"p1: Serperior","details":"Serperior, M","condition":"332/354 tox","active":true,"stats":{"atk":139,"def":226,"spa":187,"spd":226,"spe":357},"moves":["substitute","toxic","leechseed","leafstorm"],"baseAbility":"contrary","item":"leftovers","pokeball":"pokeball","ability":"contrary"}]},"rqid":6}']

# resp = ['{"active":[{"moves":[{"move":"Fire Blast","id":"fireblast","pp":8,"maxpp":8,"target":"normal","disabled":false},{"move":"Solar Beam","id":"solarbeam","pp":16,"maxpp":16,"target":"normal","disabled":false},{"move":"Dragon Pulse","id":"dragonpulse","pp":15,"maxpp":16,"target":"any","disabled":false},{"move":"Will-O-Wisp","id":"willowisp","pp":24,"maxpp":24,"target":"normal","disabled":false}],"canMegaEvo":true}],"side":{"name":"alphamak","id":"p2","pokemon":[{"ident":"p2: Charizard","details":"Charizard, M","condition":"192/297","active":true,"stats":{"atk":155,"def":192,"spa":317,"spd":207,"spe":328},"moves":["fireblast","solarbeam","dragonpulse","willowisp"],"baseAbility":"blaze","item":"charizarditey","pokeball":"pokeball","ability":"blaze"}]},"rqid":7}']
#
# if 'canMegaEvo' in resp[0]:
#     print('bruh')