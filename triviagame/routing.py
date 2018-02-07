from channels import route, include

channel_routing = [
    include("trivia.routing.websocket_routing"),

    include("trivia.routing.custom_routing"),
]
