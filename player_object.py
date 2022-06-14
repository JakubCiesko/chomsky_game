import pyglet
from physical_object import PhysicalObject

from pyglet.window import key
import math


pyglet.resource.path = ['game_resources']
pyglet.resource.reindex()
player_shoot_image = pyglet.resource.image('chomsky_mouth.png')
player_image = pyglet.resource.image('chomsky.png')

class Player(PhysicalObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs, img = player_image)
        self.rotation = 0
        self.thrust = 0
        self.rotate_speed = 200.0
        self.keys = dict(left=False, right=False, up=False, down=False)
        self.key_handler = key.KeyStateHandler()
        self.shooting = False
        self.dead = False
        self.health = 0

    def update(self, dt):
        super(Player, self).update(dt)
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        elif self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
        elif self.key_handler[key.DOWN]:
            self.thrust = 300
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x -= force_x
            self.velocity_y -= force_y
        elif self.key_handler[key.UP]:
            self.thrust = 300
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y

        self.image = player_image
        if self.key_handler[key.SPACE]:
            self.image = player_shoot_image
            self.shooting = True

    def handle_collision_with(self, other_object):
        self.health -= 1
        if self.health == 0:
            self.dead = True

    def handle_collision_with_shot(self, shot):
        self.health -= 1
        if self.health == 0:
            self.dead = True

    def check_bounds(self):
        min_x = 20
        min_y = 20
        max_x = 1460
        max_y = 780
        if self.x < min_x:
            self.x = min_x
        elif self.x > max_x:
            self.x = max_x
        if self.y < min_y:
            self.y = min_y
        elif self.y > max_y:
            self.y = max_y

