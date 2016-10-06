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
missile_group = set([])
started = False

explosion_group = set([])

rock_group = set([])

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
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def angle_vel_to_vel(ang, radius, angle_vel):
    direction1 = angle_to_vector(ang)
    direction2 = [-direction1[1], direction1[0]]
    return [angle_vel*radius*direction2[0],angle_vel*radius*direction2[1]]

def process_sprite_group(sprites, canvas):
    for i in list(sprites):
        i.draw(canvas)
    for i in list(sprites):
        i.update()
        if i.age > i.lifespan:
            sprites.remove(i)
        if i.pos[0] + i.radius < 0 or i.pos[0] -i.radius > 800 or i.pos[1] + i.radius < 0 or i.pos[1] - i.radius > 600:
            sprites.remove(i)
        
def group_collide(group, other_object):
    global boom, explosion_group
    boom = False
    removing = set([])
    for i in group:
        if i.collide(other_object):
            new_explosion = Sprite(i.pos, [0,0], i.angle, i.angle_vel, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)
            removing.add(i)
            boom = True
    group.difference_update(removing)
    
def group_group_collide(group1, group2):
    global boom, score
    for i in group1:
        group_collide(group2, i)
        if boom:
            group1.discard(i)
            score += 1
    
    
    
    
    
    
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
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]+90, self.image_center[1]],self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def shoot(self):
        vv = angle_vel_to_vel(self.angle, self.radius, self.angle_vel)
        vvv = [self.vel[0]+6*angle_to_vector(self.angle)[0]+vv[0], self.vel[1]+6*angle_to_vector(self.angle)[1]+vv[1]] 
        ppos = [self.pos[0]+40*angle_to_vector(self.angle)[0], self.pos[1]+40*angle_to_vector(self.angle)[1]]
        missile_group.add(Sprite(ppos, vvv, 0, 0, missile_image, missile_info, missile_sound))
        

    def update(self):
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH
        if self.pos[1] > HEIGHT:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= (1-0.0005)
        self.vel[1] *= (1-0.0005)
        if self.thrust:
            self.vel[0] += 0.1*angle_to_vector(self.angle)[0]
            self.vel[1] += 0.1*angle_to_vector(self.angle)[1]
        self.angle_vel *= (1-0.0005)
        self.angle += self.angle_vel
    
    
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
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
                current_explosion_index = (self.age % 24) // 1
                current_explosion_center = [self.image_center[0] +  current_explosion_index * self.image_size[0], self.image_center[1]]
                canvas.draw_image(self.image, current_explosion_center, [128,128], self.pos, [128,128]) 
                self.age += 1
        
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
    def collide(self, other_object):
        return dist(self.pos, other_object.pos) < self.radius + other_object.radius

        
           
def draw(canvas):
    global time, my_ship, missiles, started, rock_group, lives, score, time1
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # draw ship and sprites
    my_ship.draw(canvas)

    process_sprite_group(missile_group, canvas)  
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    group_collide(rock_group, my_ship)
    if boom:
        lives -= 1
    group_group_collide(rock_group, missile_group)
    # update ship and sprites
    my_ship.update()

        
    # draw splash screen if not started
    if not started or lives <= 0:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        lives = 3
        score = 0
        started = False
        
def keydown(key):
    global my_ship, a_missile
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
        ship_thrust_sound.play()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel += -0.05
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel += 0.05
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shooting = True
        my_ship.shoot()
    
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    
def keyup(key):
    global my_ship
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
        ship_thrust_sound.rewind()
    elif key == simplegui.KEY_MAP["left"]:
        pass
        #my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:
        pass
        #my_ship.angle_vel = 0
        
    
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, my_ship, score
    if not started:
        rock_group = set([])
    else:
        if len(rock_group) > 12:
            pass
        else:
            pos = [random.randint(0,800),random.randint(0,600)]
            if dist(my_ship.pos, pos) < 150:
                pass
            else:
                vel = [(score//10+1)*random.random()*random.choice([1,-1]), (score//10+1)*random.random()*random.choice([1,-1])]
                ang = 0.5*random.random()
                ang_vel = 0.05*random.random()
                rock = Sprite(pos,vel,ang,ang_vel,asteroid_image,asteroid_info)
                rock_group.add(rock)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
