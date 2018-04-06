from channels import route
from .consumers import ws_connect, ws_disconnect, ws_receive, create_room, join_room, game_info_request, handle_answer

# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We _could_ path match here if we wanted.
websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive),

]

# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("trivia.receive", create_room, type="^CREATE_GAME$"),
    route("trivia.receive", join_room, type="^JOIN_GAME$"),
    route("trivia.receive", game_info_request, type="^GAME_INFO_REQUEST$"),
    route("trivia.receive", handle_answer, type="^SEND_ANSWER$")
]
