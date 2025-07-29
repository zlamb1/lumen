from flask import Flask, request
from flask_cors import CORS
import threading
from . import animation

app = Flask(__name__)
CORS(app)

class Server:
    def __init__(self):
        self.running = False
        self._animation = None
        self.animations = {}
        self.animations['rain'] = animation.AnimationClass('rain', [
            animation.AnimationParam('speed', animation.ParamType.NUMBER, desc='How fast the animation cycles.', min=0, max=10),
            animation.AnimationParam('reverse', animation.ParamType.BOOL, desc='Reverses the direction of the animation.')
        ], animation.MockAnimation)
        self.animations['chase'] = animation.AnimationClass('chase', [
            animation.AnimationParam('speed', animation.ParamType.NUMBER, desc='How fast the animation cycles.', min=0, max=10),
            animation.AnimationParam('reverse', animation.ParamType.BOOL, desc='Reverses the direction of the animation.')
        ], animation.MockAnimation)
        self.animations['solid'] = animation.AnimationClass('solid', [
            animation.AnimationParam('speed', animation.ParamType.NUMBER, desc='How fast the animation cycles.', min=0, max=10),
            animation.AnimationParam('color', animation.ParamType.COLOR, desc='Color of the animation.')
        ], animation.MockAnimation)

    def add_animation_class(self, name, animation):
        self.animations[name] = animation

    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, value):
        if self.running:
            self.running = False
            self.thread.join()
        self._animation = value
        if not value is None:
            self.run()

    def run(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def _animate(self):
        while self.running:
            self.animation.animate()

server = Server()

@app.route("/animations")
def animations():
    animations = []
    for animation_name in server.animations:
        animation = server.animations[animation_name]
        animations.append(animation.to_dict())
    return animations

@app.route("/animation")
def animation():
    animation = server.animation
    if animation == None:
        return ('', 204)
    else:
        return animation.state

@app.route('/animation/param/<name>', methods=['POST'])
def param(name):
    if server.animation == None:
        return ('', 204)
    value = server.animation.setparam(name, request.form['value'])
    if value is None:
        return ('', 400)
    return {
        'name': name,
        'value': value
    }

@app.route('/animation/<name>', methods=['POST'])
def setanimation(name):
    if not name in server.animations:
        return ('', 404)
    server.animation = server.animations[name].create(request.form)
    return server.animation.state

@app.route("/play", methods=['POST'])
def play():
    if server.animation is None:
        return ('', 404)
    server.animation.paused = False
    return ('', 200)

@app.route("/pause", methods=['POST'])
def pause():
    if server.animation is None:
        return ('', 404)
    server.animation.paused = True
    return ('', 200)