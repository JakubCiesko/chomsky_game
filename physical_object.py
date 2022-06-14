import pyglet
import math

pyglet.resource.path = ['game_resources']
pyglet.resource.reindex()
enemy_fight_image = pyglet.resource.image('everett_in_fight.png')

def get_image_scaled_center(game_object):
    game_object_scale = game_object.scale
    game_object_image = game_object.image
    width, height = game_object_image.width, game_object_image.height
    extra_x = width//2*game_object_scale
    extra_y = height//2*game_object_scale
    return [game_object.position[0] + extra_x, game_object.position[1] + extra_y]

def distance(point_1 = (0,0), point_2 = (0,0)):
    return math.sqrt((point_1[0]-point_2[0])**2+(point_1[1]-point_2[1])**2)



class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.dead = False
        self.is_shot_or_player = False
        self.is_monster = False
        self.in_fight = False

    def update_image_in_fight(self):
        if self.in_fight:
            self.image = enemy_fight_image


    def check_bounds(self):
        min_x = 20
        min_y = 20
        max_x = 1460
        max_y = 780

        velocity_1 = - self.velocity_x
        velocity_2 = - self.velocity_y

        if self.x < min_x:
            self.velocity_x = velocity_1
        elif self.x > max_x:
            self.velocity_x = velocity_1
        if self.y < min_y:
            self.velocity_y = velocity_2
        elif self.y > max_y:
            self.velocity_y = velocity_2

    def update(self, dt):
        if self.velocity_x or self.velocity_y:
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
        else:
            self.velocity_x += 50
            self.velocity_y += 50

        self.check_bounds()
        self.update_image_in_fight()

    def collides_with(self, other_object):
        if not self.is_shot_or_player:
            actual_distance = distance(get_image_scaled_center(self), other_object.position)
            if actual_distance <= 60:
                return True
            return False
        elif self.is_shot_or_player and other_object.is_shot_or_player:
            actual_distance = distance(self.position, other_object.position)
            if actual_distance <= 60:
                return True
            return False
        elif self.is_shot_or_player and other_object.is_monster:
            actual_distance = distance(get_image_scaled_center(self), other_object.position)
            if actual_distance <= 80:
                return True
            return False

    def handle_collision_with(self, other_object):
        self.velocity_y = - self.velocity_y
        self.velocity_x = - self.velocity_x

    def handle_collision_with_shot(self, shot):
        self.dead = True

