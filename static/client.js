const ws = new WebSocket("ws://localhost:8000/ws/player_1");

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    // route to appropriate panel based on message.type
};

ws.send(JSON.stringify({
    type: "game_event",
    action: "player_action",
    payload: {...}
}));