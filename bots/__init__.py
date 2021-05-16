class Room():
    def __init__(self, room_id='', player_id='', mega=False, dynamax=False, switch=False):
        self.id = room_id
        self.primary_player = player_id
        self.mega = mega
        self.dynamax = dynamax
        self.switch = switch
    def __str__(self):
        output = 'ID: ' + self.id + '\nPrimary Player: ' + self.primary_player + '\nMega Evolution Possible: ' + str(self.mega) + '\nDynamax Possible: ' + str(self.dynamax) + '\n'
        return output

class Player():
    def __init__(self, room='', id='', name=''):
        self.room = room
        self.id = id
        self.name = name
    def __str__(self):
        output = 'Room: ' + self.room + '\nID: ' + self.id + '\nName: ' + self.name + '\n'
        return output

class Pokemon():
    def __init__(self, room='', player='', name='', species='', types=[], gender='', moves=[], item=''):
        self.room = room
        self.player = player
        self.name = name
        self.species = species
        self.types = types
        self.gender = gender
        self.moves = moves
        self.item = item
    def __str__(self):
        t = ''
        m = ''
        if len(self.types) > 0:
            t = ', '.join(self.types)
        if len(self.moves) > 0:
            m = ', '.join(self.moves)
        output = 'Room: ' + self.room + '\nPlayer: ' + self.player + '\nName: ' + self.name + '\nSpecies: ' + self.species + '\nTypes: ' + t + '\nGender: ' + self.gender + '\nMoves: ' + m + '\nItem: ' + self.item + '\n'
        return output