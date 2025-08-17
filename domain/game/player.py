class Player:
    def __init__(self, websocket, player_id, username, guild_id):
        self.ws = websocket
        self.id = player_id
        self.username = username
        self.guild_id = guild_id
        self.score = 0
        
    def score_increment(self):
        self.score += 1
