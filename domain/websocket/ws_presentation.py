from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

from .game_state import GAME                     # garde ton état global “partie” si besoin
from websocket_service.broadcast import broadcast   # ← reste utilisé par Room
from .protocol.event_type import EventType
from .protocol.event_key import EventKey
from .protocol.event_value import EventValue
from .protocol.event_factory import event_factory

from domain.user.user_repository import UserRepository
from game.room import Room                        # ta classe Room

router = APIRouter()
rooms: dict[int, Room] = {}                       # clan_id → Room


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    game, _ = GAME[0]                            

    try:
        # ---------- LOGIN ----------
        event = json.loads(await websocket.receive_text())
        if event[EventKey.TYPE] != EventType.LOGIN:
            await websocket.close(); return

        player_id = event[EventValue.PLAYER_ID]
        user_profile = await UserRepository().get_by_id(player_id)

        clan_id = user_profile.guild_id           # room = clan
        room = rooms.setdefault(clan_id, Room(clan_id))

        # on enregistre le joueur dans la room
        await room.join(
            websocket,
            player_id,
            user_profile.username,
            clan_id
        )

        # ack login
        await websocket.send_text(json.dumps(
            event_factory(EventType.LOGIN, **{EventKey.MESSAGE: EventValue.OK})
        ))

        # ---------- ENVOI INFO JEU ----------
        await websocket.send_text(json.dumps(
            event_factory(
                EventType.GET_GAME_INFO,
                game={
                    "sumScore": game.sumScore,
                    "playerScore": room.public_player_list()  # méthode utilitaire
                },
            )
        ))

        # ---------- BOUCLE JEU ----------
        while True:
            event = json.loads(await websocket.receive_text())

            if event[EventKey.TYPE] == EventType.CLICK:
                game.score_increment()            # score global
                room.player_increment(player_id)  # score individuel
                
            payload_dict = event_factory(
                EventType.CLICKED,
                **{EventKey.SUMSCORE: game.sumScore},
                player=room.public_player(player_id)
            )
            print("Payload envoyé:", payload_dict)
            await room.broadcast(payload_dict)

    except WebSocketDisconnect:
        await room.leave(player_id)
