import pyglet
import random
import physical_object

pyglet.resource.path = ['game_resources']
pyglet.resource.reindex()
enemy_image = pyglet.resource.image('everett.png')
obstacle_image = pyglet.resource.image('obstacle.png')
health_icon = pyglet.resource.image('health.png')
shot_image = pyglet.resource.image('recursion_new_new.png')
health_icon = pyglet.resource.image('heart.png')

def monsters(number_of_monsters, player_position):
    monsters = []
    monsters_x_positions = random.sample(range(40,1200,40), number_of_monsters)
    monsters_y_positions = random.sample(range(40,600,40), number_of_monsters)
    for i in range(number_of_monsters):
        monster_x, monster_y, _ = player_position
        while not physical_object.distance((monster_x,monster_y),player_position):
            monster_x = monsters_x_positions[i]
            monster_y = monsters_y_positions[i]
        new_monster = physical_object.PhysicalObject(img = enemy_image)
        new_monster.x = monster_x
        new_monster.y = monster_y
        new_monster.velocity_x = random.randint(-3,3)*50
        new_monster.velocity_y = random.randint(-3,3)*50
        monsters.append(new_monster)
    return monsters

def obstacles(number_of_obstacles, player_position, monsters_positions):
    obstacles = []
    obstacles_x_positions = random.sample(range(40, 1200, 60), number_of_obstacles)
    obstacles_y_positions = random.sample(range(40, 600, 60), number_of_obstacles)
    for i in range(number_of_obstacles):
        obstacle_x, obstacle_y, _ = player_position

        while not physical_object.distance((obstacle_x,obstacle_y), player_position):
            obstacle_x = obstacles_x_positions[i]
            obstacle_y = obstacles_y_positions[i]

        new_obstacle = physical_object.PhysicalObject(img = obstacle_image)

        if [obstacle_x,obstacle_y] not in monsters_positions:
            new_obstacle.x = obstacle_x
            new_obstacle.y = obstacle_y

        obstacles.append(new_obstacle)

    return obstacles

def health_bar(number_of_icons, batch=None):
    health_bar = []
    for i in range(number_of_icons):
        new_sprite = pyglet.sprite.Sprite( img = health_icon, x = 10 + i * 30, y= 10, batch=batch)
        new_sprite.scale = 0.2
        health_bar.append(new_sprite)
    return health_bar

def shot(player):
    import math
    new_shot = physical_object.PhysicalObject(img =shot_image )
    angle_radians = -math.radians(player.rotation)
    shot_speed = math.sqrt(player.velocity_x**2+player.velocity_y**2) + 300
    #new_shot.velocity_x = math.cos(angle_radians) * (player.velocity_x  + 300)
    #new_shot.velocity_y = math.sin(angle_radians) * (player.velocity_y + 300)

    new_shot.velocity_x = math.cos(angle_radians) * shot_speed
    new_shot.velocity_y = math.sin(angle_radians) * shot_speed
    new_shot.rotation = player.rotation
    if new_shot.velocity_x > 0:
        new_shot.x = player.x + 65
    else:
        new_shot.x = player.x - 65
    new_shot.y = player.y + (player.image.height*player.scale//4) * math.sin(player.rotation) #alebo 60

    player.shooting = False
    return new_shot
