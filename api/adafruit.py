import neopixel, board

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.grid_rain import Rain
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse

from . import animation

pixels = neopixel.NeoPixel(
			board.D18, 200, auto_write = False, 
			brightness=0.1, pixel_order = neopixel.RGB)

class AdafruitAnimation(animation.Animation):
    def __init__(self, name, params, cls, **kwargs):
        self._animation = cls(pixels, **kwargs)
        super().__init__(name, params, self._animation)
    
    def animate(self):
        self._animation.animate()
        pixels.show()

speed_param = animation.AnimationParam('speed', animation.ParamType.NUMBER, desc='Animation speed rate in seconds.', min=0)
color_param = animation.AnimationParam('color', animation.ParamType.COLOR, desc='Animation color.'),
bgcolor_param = animation.AnimationParam('background_color', animation.ParamType.COLOR, desc='Animation background color.')
tail_length_param = animation.AnimationParam('tail_length', animation.ParamType.NUMBER, desc='The length of the comet.', min=1)
reverse_param = animation.AnimationParam('reverse', animation.ParamType.BOOL, desc='Reverse direction of movement.')
bounce_param = animation.AnimationParam('bounce', animation.ParamType.BOOL, desc='Comet will bounce back and forth.')
period_param = animation.AnimationParam('period', animation.ParamType.NUMBER, desc='Period to pulse the LEDs over.')
breath_param = animation.AnimationParam('breath', animation.ParamType.NUMBER, desc='Duration to hold minimum and maximum intensity levels.')
min_intensity = animation.AnimationParam('min_intensity', animation.ParamType.NUMBER, desc='Lowest brightness level of the pulse.', min=0, max=1)
max_intensity = animation.AnimationParam('max_intensity', animation.ParamType.NUMBER, desc='Highest brightness level of the pulse.', min=0, max=1)

adafruit_animation_classes = [
    animation.AnimationClass(
        "blink", [ speed_param, color_param, bgcolor_param ], Blink
    ),
    animation.AnimationClass(
        'solid', [ color_param ], Solid
    ),
    animation.AnimationClass(
        'chase', [
            speed_param.
            anim.AnimationParam('size', animation.ParamType.NUMBER, desc='Number of pixels to turn on in a row.', min=1),
            animation.AnimationParam('spacing', animation.ParamType.NUMBER, desc='Number of pixels to turn off in a row.', min=0),
            reverse_param
        ], Chase
    ),
    animation.AnimationClass(
        'comet', [
            speed_param,
            color_param,
            bgcolor_param,
            tail_length_param,
            reverse_param,
            bounce_param
        ], Comet
    ),
    animation.AnimationClass(
        'pulse', [
            speed_param,
            color_param,
            period_param,
            breath_param,
            min_intensity,
            max_intensity
        ], Pulse
    ),
    animation.AnimationClass(
        'rainbow', [
            speed_param,
            period_param
        ], Rainbow
    )
]

def register_adafruit_animations(server):
    for cls in adafruit_animation_classes:
        server.add_animation_class(cls)
