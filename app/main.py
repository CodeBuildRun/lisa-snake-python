import json
import os
import random
import bottle

from .api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    directions = ['up', 'down', 'left', 'right']
    # direction = random.choice(directions)
    # Make a list of all the bad coordinates and try to avoid them
    height = data["board"]["height"]
    width = data["board"]["width"]
    badCoords = []

    # Bad coordinates that my snake needs to avoid
    # 1. above and below the board
    for x in range(width):
        bad = (x, -1)
        badCoords.append(bad)
        bad = (x, height)
        badCoords.append(bad)
    # 2. left and right to the board
    for y in range(height):
        bad = (-1, y)
        badCoords.append(bad)
        bad = (width, y)
        badCoords.append(bad)
    # 3. snake bodies on the board
    for snake in data["board"]["snakes"]:
        for body in snake["body"]:
            bad = (body["x"], body["y"])
            badCoords.append(bad)
    possibleMoves = []

    # get coordinates of my snake head
    myHead = data["you"]["body"][0]

    # up
    coord = (myHead["x"], myHead["y"]-1)
    if coord not in badCoords:
        possibleMoves.append("up")
    # down
    coord = (myHead["x"], myHead["y"]+1)
    if coord not in badCoords:
        possibleMoves.append("down")
    # left
    coord = (myHead["x"]-1, myHead["y"])
    if coord not in badCoords:
        possibleMoves.append("left")
    # right
    coord = (myHead["x"]+1, myHead["y"])
    if coord not in badCoords:
        possibleMoves.append("right")

    # possible moves
    if len(possibleMoves) > 0:
        direction = random.choice(possibleMoves)
    else:
        direction = random.choice(directions)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()


def main():
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


if __name__ == '__main__':
    main()
