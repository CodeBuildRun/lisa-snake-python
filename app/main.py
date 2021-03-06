import os
import bottle

from .api import ping_response, start_response, move_response, end_response
from .snake import Snake


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
    """
    Because this is a stateful snake AI,
    initialize the snake state here using the
    request's data.
    """
    data = bottle.request.json

    color = snake.initialize(data)
    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    Using the data from the endpoint request object, the
    snake AI must choose a direction to move in.
    """
    direction = snake.move(data)
    return move_response(direction)


@bottle.post('/end')
def end():
    """
    If your snake AI was stateful,
    clean up any stateful objects here.
    """
    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

# Create a snake
snake = Snake()


def main():
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


if __name__ == '__main__':
    main()
