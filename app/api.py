import json
from bottle import HTTPResponse
from .snake import Moves


def ping_response():
    return HTTPResponse(
        status=200
    )


def start_response(color):
    assert type(color) is str, \
        "Color value must be string"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "color": color
        })
    )


def move_response(move):
    assert isinstance(move, Moves), \
        "Move must be one of [up, down, left, right]"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "move": move.value
        })
    )


def end_response():
    return HTTPResponse(
        status=200
    )
