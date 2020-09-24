import pyglet, math
from pyglet import shapes, clock
from pyglet.gl import *
from pyglet.window import key, mouse
import random as rdm

class Ray:
    def __init__(self, degree, x, y, n, turn):
        self.rad = degree*(math.pi/(2*n)) - turn*(2*math.pi/n)
        self.x, self.y = x, y
        self.dest_x = math.sin(self.rad);
        self.dest_y = math.cos(self.rad);
        
    def distance_to_wall (self, line):
        wall = self.intersect(line)
        dist = ((self.x - wall[0])**2 + (self.y - wall[1])**2)**0.5
        return dist
    
    def intersect(self, line):
        boundary = line.position
        x1, y1, x2, y2 = self.x, self.y, self.x + 2000*self.dest_x, self.y + 2000*self.dest_y #ray coords
        x3, y3, x4, y4 = boundary[0], boundary[1], boundary[2], boundary[3]
        det = ((x1 - x2)*(y3 - y4)) - ((y1 - y2)*(x3 - x4))
        if det == 0:
            return None
        t = (((x1 - x3)*(y3 - y4)) - ((y1 - y3)*(x3 - x4)))/det
        u = - (((x1 - x2)*(y1 - y3)) - ((y1 - y2)*(x1 - x3)))/det
        if u>=0 and u<=1 and t>=0 and t<=1:
            return (int(x3 + u*(x4 - x3)), int(y3 + u*(y4 - y3)))
        return None

fps = clock.Clock()
screen_res = 900
window = pyglet.window.Window(screen_res, screen_res)
batch = pyglet.graphics.Batch()
rays_batch = pyglet.graphics.Batch()

###Global vars###                           
turn = [0]                              # how much to turn
xy = [(250,250)]                        # location of source
w, a, s, d = False, False, False, False # pressed state of movement keys

lines = [] #array of walls
### window borders ###
lines.append(shapes.Line(0,0,0,500, width=1, color=(0, 255, 255), batch=batch))
lines.append(shapes.Line(0,0,500,0, width=1, color=(0, 255, 255), batch=batch))
lines.append(shapes.Line(500,0,500,500, width=1, color=(0, 255, 255), batch=batch))
lines.append(shapes.Line(500,500,0,500, width=1, color=(0, 255, 255), batch=batch))
   
lines.append(shapes.Line(50,0,50,200, width=5, color=(0, 255, 0), batch=batch))
lines.append(shapes.Line(50,200,200,200, width=5, color=(0, 255, 0), batch=batch))
lines.append(shapes.Line(0,420,200,420, width=5, color=(0, 255, 0), batch=batch))
lines.append(shapes.Line(350,500,350,100, width=5, color=(0, 255, 0), batch=batch))
lines.append(shapes.Line(350,350,450,350, width=5, color=(0, 255, 0), batch=batch))

### calculate and draw rays ###
ray_class = [] # store ray classes
def find_intersect(ray):
    dist = []
    int_point = []
    for line in lines:
        intersect = ray.intersect(line)
        if intersect != None:
            int_point.append(intersect)
            dist.append(ray.distance_to_wall(line))
    distance = min(dist)
    point = int_point[dist.index(distance)]
    return distance, point[0], point[1]

walls = []
def create_rays(source_x , source_y, turn):
    global n
    n = 200
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(10)
    glBegin(GL_LINES) 
    glColor3f(255,0,0)
    for i in range(int(screen_res/5)):
        glVertex2i(5*(2*i + 1), 0)
        glVertex2i(5*(2*i + 1), int(screen_res/2))
    glEnd() 
    glLineWidth(math.ceil(screen_res/n))
    glBegin(GL_LINES) 
    glColor3f(0,255,0)
    for i in range(n):
        ray_class.append(Ray(i, source_x, source_y, n, turn))
        dist, end_x, end_y = find_intersect(ray_class[i])
        theta = (math.pi*(n - 1 - 2*i))/(4*n - 4)
        p_dist = dist * math.cos(theta)
        x = (screen_res/(2*n))*(2*i + 1)
        y = int(5000.0 / (p_dist + 1))
        glVertex2i(int(x), int(screen_res/2) + y)                          #OPENGL line start
        glVertex2i(int(x), int(screen_res/2) - y)                          #OPENGL line end
    glEnd()

### Render ###
@window.event
def on_draw():
    rays_batch.draw()
    #batch.draw()
    fps.tick()
    print(int(fps.get_fps()))

### Input Handling ###
@window.event
def on_key_press(symbol, modifiers): #Looks for a keypress
    global w, a, s, d
    if symbol == key.W:
        w = True
    elif symbol == key.A:
        a = True
    elif symbol == key.S:
        s = True
    elif symbol == key.D:
        d = True

@window.event
def on_key_release(symbol, modifiers):
    global w, a, s, d
    if symbol == key.W:
        w = False
    elif symbol == key.A:
        a = False
    elif symbol == key.S:
        s = False
    elif symbol == key.D:
        d = False

@window.event                       
def on_mouse_motion(x, y, dx, dy):
    turn[0] -= dx/3.0

### Update position and direction ###
def update(dt):
    ray_class.clear()
    walls.clear()
    xy[0] = ((xy[0][0]), (xy[0][1]))
    create_rays(xy[0][0], xy[0][1], turn[0])
    rad = (math.pi/4) - turn[0]*(2.0*math.pi/n)
    sin_o = 2*math.sin(rad)
    cos_o = 2*math.cos(rad)
    if w == True:
        xy[0] = (int(xy[0][0] + sin_o), int(xy[0][1] + cos_o))
    elif s == True:
        xy[0] = (int(xy[0][0] - sin_o), int(xy[0][1] - cos_o)) 
    if d == True:
        xy[0] = (int(xy[0][0] + cos_o), int(xy[0][1] - sin_o))
    elif a == True:
        xy[0] = (int(xy[0][0] - cos_o), int(xy[0][1] + sin_o))

create_rays(250, 250, 0)
pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
