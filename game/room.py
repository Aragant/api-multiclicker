from .player import Player
import json
from fastapi import WebSocket, WebSocketDisconnect
from domain.websocket.protocol.event_type import EventType
from domain.websocket.protocol.event_value import EventValue
from domain.websocket.protocol.event_factory import event_factory

class Room:
    def __init__(self, room_id: int):
        self.id = room_id
        self.players: dict[int, Player] = {}   # player_id -> Player

    # ---------- gestion des connexions ----------
    async def join(self, websocket: WebSocket, player_id: int,
                   username: str, guild_id: int) -> None:
        self.players[player_id] = Player(websocket, player_id, username, guild_id)

        # accusé de réception LOGIN
        await websocket.send_text(json.dumps(
            event_factory(EventType.LOGIN, message=EventValue.OK)
        ))

    async def leave(self, player_id: int) -> None:
        self.players.pop(player_id, None)

    # ---------- helpers publics ----------
    def public_player(self, player_id: int) -> dict:
        """
        Retourne la représentation « safe » d’un joueur pour l’UI :
        { "username": "...", "sumScore": n }
        """
        p = self.players[player_id]
        return {"username": p.username, "score": p.score}

    def public_player_list(self) -> list[dict]:
        """Liste prête à être mise dans l’événement GET_GAME_INFO."""
        return [self.public_player(pid) for pid in self.players]

    # ---------- mise à jour du score ----------
    def player_increment(self, player_id: int) -> None:
        self.players[player_id].score_increment()

    # ---------- diffusions ----------
    async def broadcast(self, payload: dict) -> None:
        """À tout le monde dans la room."""
        await self._send_to(lambda _p: True, payload)

    async def broadcast_to_clan(self, clan_id: int, payload: dict) -> None:
        """Seulement aux joueurs d’un clan."""
        await self._send_to(lambda p: p.guild_id == clan_id, payload)

    # ---------- interne ----------
    async def _send_to(self, predicate, payload: dict) -> None:
        dead: list[int] = []
        for p in self.players.values():
            if not predicate(p):
                continue
            try:
                await p.ws.send_text(json.dumps(payload))
            except WebSocketDisconnect:
                dead.append(p.id)

        for pid in dead:
            self.players.pop(pid, None)
