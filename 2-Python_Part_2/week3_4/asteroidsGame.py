!#/usr/bin/python2
# Final project - Asteroids game 'Rice Rocks'

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
    group_copy = set(group)
    for item in group_copy:
        item.draw(canvas)
        if item.update():
            group.remove(item)

def group_collide(group, other_object):
    global explosion_group
    
    group_copy = set(group)
    for item in group_copy:
        if item.collide(other_object):
            group.remove(item)
            explosion_group.add(Sprite(other_object.get_pos(), [0, 0], 0, 0, explosion_image,
                                       explosion_info, explosion_sound))
            return True
    return False   

def group_group_collide(group, other_group):
    collisions = 0
    group_copy = set(group)
    for item in group_copy:
        if group_collide(other_group, item):
            group.discard(item)
            collisions += 1
    return collisions

def reset_game():
    global started, soundtrack, lives, score, rock_group
    
    started = False
    soundtrack.pause()
    soundtrack.rewind()
    lives = 3
    score = 0
    rock_group = set([])

def start_game():
    global started, soundtrack
    
    started = True
    soundtrack.set_volume(0.7)
    soundtrack.play()

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_pos(self):
        return self.pos
    
    def get_rad(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [130, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        self.angle += self.angle_vel
    
        # update position
        self.pos[0] = (self.vel[0] + self.pos[0]) % WIDTH
        self.pos[1] = (self.vel[1] + self.pos[1]) % HEIGHT
        
        # update velocity
            # add friction
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
            # add acceleration when thrusting
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += 0.1 * forward[0]
            self.vel[1] += 0.1 * forward[1]
    
    def do_thrust(self, value):
        self.thrust = value
        
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
        
    def increase_angle(self):
        self.angle_vel += 0.05

    def decrease_angle(self):
        self.angle_vel -= 0.05
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_position = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_velocity = [self.vel[0] + 3 * forward[0], self.vel[1] + 3 * forward[1]]
        a_missile = Sprite(missile_position, missile_velocity, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_pos(self):
        return self.pos
    
    def get_rad(self):
        return self.radius        
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        if self.animated:
            explosion_index = (self.age % self.lifespan) // 1
            explosion_center = [explosion_info.get_center()[0] + explosion_index * explosion_info.get_size()[0],
                                explosion_info.get_center()[1]]
            canvas.draw_image(explosion_image, explosion_center, explosion_info.get_size(),
                              self.pos, explosion_info.get_size()) 
            
            self.age += 0.03
    
    def update(self):
        self.angle += self.angle_vel
    
        # update position
        self.pos[0] = (self.vel[0] + self.pos[0]) % WIDTH
        self.pos[1] = (self.vel[1] + self.pos[1]) % HEIGHT  
        
        # increment the age of the sprite and check lifespan
        self.age += 1
        if self.lifespan and self.age >= self.lifespan:
            return True
        return False
        
    def collide(self, other_object):
        if dist(other_object.get_pos(), self.get_pos()) <= other_object.get_rad() + self.get_rad():
            return True
        return False
    
# handlers
def draw(canvas):
    global time, lives, score, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # determine collisions
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    score += group_group_collide(missile_group, rock_group)
    
    # game over
    if lives == 0:
        reset_game()
    
    # draw text and score
    canvas.draw_text('Lives: '+ str(lives), (40, 50), 36, "White", "monospace")
    canvas.draw_text('Score: '+ str(score), (590, 50), 36, "White", "monospace")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.decrease_angle()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.increase_angle()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.do_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increase_angle()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrease_angle()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.do_thrust(False)
        
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        start_game()
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    if started and len(rock_group) < 12:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3]
        rock_ang_vel = random.random() * 0.2 - 0.1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
        if dist(rock_pos, my_ship.get_pos()) > 2 * my_ship.get_rad():
            rock_group.add(a_rock)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([]) 
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
