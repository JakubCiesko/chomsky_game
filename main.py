import pyglet
import load as load
import player_object as player_object
from pyglet.window import key



def load_player_object(initial_health: int):
    player = player_object.Player(x=400, y=300)
    player.health = initial_health
    player.is_shot_or_player = True
    return player


def load_monsters(player):
    return load.monsters(14, player.position)


def load_health_bar(player, batch):
    return load.health_bar(player.health//50,batch)


def load_obstacles(no_of_obstacles, monsters, player):
    monster_positions = []
    for monster in monsters:
        monster_positions.append(monster.position)
    return load.obstacles(no_of_obstacles, player.position, monster_positions)

def load_game_objects():
    player = load_player_object(500)
    monsters = load_monsters(player)
    obstacles = load_obstacles(2, monsters, player)
    health_bar = load_health_bar(player, main_batch)
    shots = []
    game_objects = [player] + monsters + obstacles
    for object in game_objects:
        object.scale = 0.2
        if object in obstacles:
            object.scale = 0.3
        if object in monsters:
            object.is_monster = True
    return player, monsters, obstacles, health_bar, shots, game_objects


def handle_shot_collision(shots, game_objects):
    for i in range(len(shots)):
        for j in range(len(game_objects)):
            shot = shots[i]
            obj = game_objects[j]
            if obj.collides_with(shot) and not obj.dead and obj not in obstacles:
                if obj != game_objects[0]:
                    obj.image = enemy_dead_image
                obj.handle_collision_with_shot(shot)
                shot.handle_collision_with_shot(obj)
            if obj in obstacles and obj.collides_with(shot):
                shot.velocity_x = - shot.velocity_x
                shot.velocity_y = - shot.velocity_y
    return


def load_game_screen_graphics():
    back_ground = pyglet.image.load('background.png')
    back_ground_sprite = pyglet.sprite.Sprite(img=back_ground)
    return back_ground_sprite


def remove_dead_objects(game_objects, shots):
    for obj in game_objects:
        if obj.dead:
            game_objects.remove(obj)
    for shot in shots:
        if shot.dead:
            shots.remove(shot)
    return


def obstacle_collision(obstacles, game_objects):
    for obstacle in obstacles:
        for object in game_objects:
            if obstacle.collides_with(object):
                object.velocity_x = - object.velocity_x
                object.velocity_y = - object.velocity_y
    return


def handle_object_collision(game_objects):
    for i in range(len(game_objects)):
        for j in range(1, len(game_objects)):
            obj1 = game_objects[i]
            obj2 = game_objects[j]
            if obj1.collides_with(obj2):
                obj1.handle_collision_with(obj2)
                obj2.handle_collision_with(obj1)
                if obj1 == player and obj2 in monsters:
                    obj2.in_fight = True

    return


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return

def get_image_scaled_center(game_object):
    game_object_scale = game_object.scale
    game_object_image = game_object.image
    width, height = game_object_image.width, game_object_image.height
    extra_x = width//2*game_object_scale
    extra_y = height//2*game_object_scale
    return [game_object.position[0] + extra_x, game_object.position[1] + extra_y]


def update_healthbar(player, health_bar):
    health = player.health//50
    if player.dead:
        for i in range(len(health_bar)):
            health_bar.pop()
    if len(health_bar)>0:
        for i in range(len(health_bar)-health):
            health_bar.pop()
    return

def load_music():
    music = pyglet.resource.media('hudba_hra.mp3')
    music.play()
    return

game_window = pyglet.window.Window(fullscreen= True)

#game = False
pyglet.resource.path = ['game_resources']
pyglet.resource.reindex()

enemy_dead_image = pyglet.resource.image('everett_dead.png')

enemy_image = pyglet.resource.image('everett.png')
#background_main_menu = pyglet.image.load('main_menu.png')
#main_menu = pyglet.sprite.Sprite(img=background_main_menu)
background = load_game_screen_graphics()
load_music()

main_batch = pyglet.graphics.Batch()

player, monsters, obstacles, health_bar, shots, game_objects = load_game_objects()

game_window.push_handlers(player.key_handler)
keys = key.KeyStateHandler()
game_window.push_handlers(key)



def draw_primitives(batch):
    primitives = []
    x,y = player.position
    x1,y1 = get_image_scaled_center(player)
    primitives.append(pyglet.shapes.Circle(x,y, 10, color=(50, 225, 30), batch=batch))
    primitives.append(pyglet.shapes.Circle(x1, y1, 10, color=(100, 100, 50), batch=batch))
    for obstacle in obstacles:
        x,y = obstacle.position
        x1,y1 = get_image_scaled_center(obstacle)
        primitives.append(pyglet.shapes.Circle(x, y, 30, color=(50, 225, 30), batch=batch))
        primitives.append(pyglet.shapes.Circle(x1, y1, 30, color=(100, 100, 50), batch=batch))
    for monster in monsters:
        x, y = get_image_scaled_center(monster)
        primitives.append(pyglet.shapes.Circle(x,y, 10, color=(50, 225, 30), batch=batch))
    for shot in shots:
        x1,y1 = get_image_scaled_center(shot)
        x,y = shot.position
        primitives.append(pyglet.shapes.Circle(x,y,10, color = (50,225,30), batch=batch))
        primitives.append(pyglet.shapes.Circle(x1, y1, 10, color=(100, 100, 50), batch=batch))
    return primitives

@game_window.event
def on_draw():
    import math
    game_window.clear()
    background.draw()
    #primitives = draw_primitives(main_batch)
    for object in game_objects:
        object.draw()
    for shot in shots:
        shot.is_shot_or_player = True
        if shot.velocity_x == 0:
            shot.velocity_x += 10
        shot_angle = math.atan2(shot.velocity_y, shot.velocity_x)
        if shot.velocity_y == 0:
            shot_angle = 0
        shot.rotation = 180 - math.degrees(shot_angle)
        shot.draw()

    for monster in monsters:
        if not player.collides_with(monster):
            monster.in_fight = False

    main_batch.draw()
    #main_menu.draw()


def update(dt):
    import random
    player.update(dt)
    for monster in monsters:
        monster.update(dt)
    for shot in shots:
        shot.scale = 0.5
        shot.update(dt)
        center_image(shot.image)
    for object in game_objects:
        if object == player:
            center_image(object.image)
    handle_object_collision(game_objects)
    handle_shot_collision(shots,game_objects)
    obstacle_collision(obstacles,game_objects)
    a = random.randint(1, 16)
    if a % 11 == 0:
        for monster in monsters:
            if not monster.in_fight:
                monster.image = enemy_image
        remove_dead_objects(game_objects,shots)

    update_healthbar(player, health_bar)

@game_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE and player in game_objects:
        shots.append(load.shot(player))



if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()