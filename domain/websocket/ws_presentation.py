from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

from .game_state import GAME, PLAYER
from websocket_service.broadcast import broadcast
from game.player import Player
from .protocol.event_type import EventType
from .protocol.event_key import EventKey
from .protocol.event_value import EventValue
from .protocol.event_factory import event_factory

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    game, connected = GAME[0]

    try:
        # --- LOGIN ---
        message = await websocket.receive_text()
        event = json.loads(message)
        if event[EventKey.TYPE] != EventType.LOGIN:
            await websocket.close()
            return

        username = event[EventValue.USERNAME]
        PLAYER[id(websocket)] = Player(username)
        connected.add(websocket)

        await websocket.send_text(json.dumps(
            event_factory(EventType.LOGIN, **{EventKey.MESSAGE: EventValue.OK})
        ))

        # --- SEND GAME INFO ---
        players = [
            {"username": p.username, "sumScore": p.sumScore}
            for p in PLAYER.values()
        ]
        await websocket.send_text(json.dumps(
            event_factory(
                EventType.GET_GAME_INFO,
                game={"sumScore": game.sumScore, "playerScore": players}
            )
        ))

        # --- GAME LOOP ---
        while True:
            message = await websocket.receive_text()
            event = json.loads(message)

            if event[EventKey.TYPE] == EventType.CLICK:
                game.score_increment()
                PLAYER[id(websocket)].score_increment()

                await broadcast(connected, json.dumps(
                    event_factory(
                        EventType.CLICKED,
                        **{EventKey.SUMSCORE: game.sumScore},
                        player={
                            "username": PLAYER[id(websocket)].username,
                            "sumScore": PLAYER[id(websocket)].sumScore
                        }
                    )
                ))

    except WebSocketDisconnect:
        connected.discard(websocket)
        PLAYER.pop(id(websocket), None)
