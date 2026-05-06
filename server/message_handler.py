async def handle_message(player_id: str, message: dict):
    if message["action"] == "narrative":
        # route to Director
        pass
    elif message["action"] == "attack":
        # route to game engine
        pass