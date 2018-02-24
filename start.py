'''Main part of SimPhysX

Simulator of Physical Process
There is only one scene: Simulation of Electrostatic fields
Author: Mikhail Gorokhoov
'''

import pygame as pg
import threading
from backend import *
from frontend import *

'''Constants & literals'''
width = 1920
height = 1080
resolution = (width, height)
fps_lim = 60
l_str = 40  # Lenth of strings of information of fps, x, y, intensity and ect.
pg.font.init()
font_screen_info = pg.font.SysFont('Courier New', 28, bold='True')
'''Variables'''

# Canvas world
x_pos = 0
y_pos = 0

scale = 100
step = 200
point_size = 4

'''PreLoop'''
pg.init()
gameDisplay = pg.display.set_mode(resolution, pg.DOUBLEBUF)
screen = pg.Surface(resolution)
screen.set_alpha(None)
pg.display.set_caption('SimPhysX - Electrostatic Fields')
clock = pg.time.Clock()
world = ESSpace()
x_mouse = 0
y_mouse = 0
# count_of_threads = 4
# part = height // count_of_threads
print_info = True
panel = ControlPanel(world)
panel.root.deiconify()
update_screen = True
'''
class drawing_with_threads(threading.Thread):
    def __init__(self, screen, world):
        threading.Thread.__init__(self)
        self.screen = screen
        self.world = world
    def run(self):
        print(self.getName(),'has been started!')
    def draw(self, start, end):
        global width, height, scale, x_pos, y_pos, point_size
        for x0 in range(0, width, point_size*3):
            for y0 in range(start, end, point_size*3):
                coord = canvas_to_real((x0, y0), scale=scale, width=width, height=height)
                p = self.world.potential_is(coord)
                if 0 <= p and p < 255 * 10000:
                    pg.draw.circle(self.screen, (255, 255 - p // 10000, 255 - p // 10000), (x0 - x_pos, y0 + y_pos), point_size)
                elif 255 * 10000 <= p:
                    pg.draw.circle(self.screen, (255, 0, 0), (x0 - x_pos, y0 + y_pos), point_size)
                elif (-255) * 10000 <= p and p < 0:
                    pg.draw.circle(self.screen, (255 + p // 10000, 255 + p // 10000, 255), (x0 - x_pos, y0 + y_pos), point_size)
                else:
                    pg.draw.circle(self.screen, (0, 0, 255), (x0 - x_pos, y0 + y_pos), point_size)

threads = [drawing_with_threads(screen, world) for i in range(count_of_threads)]
for thread in threads:
    thread.start()
'''

'''PyGame Loop'''
crashed = False
while not crashed:
    clock.tick(fps_lim)
    '''Events'''
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                print('You Press UP')
                y_pos += int(-step)
                update_screen = True
            if event.key == pg.K_DOWN:
                print('You Press DOWN')
                y_pos += int(step)
                update_screen = True
            if event.key == pg.K_LEFT:
                print('You Press LEFT')
                x_pos += int(-step)
                update_screen = True
            if event.key == pg.K_RIGHT:
                print('You Press RIGHT')
                x_pos += int(step)
                update_screen = True
            if event.key == pg.K_EQUALS:
                scale *= 1.25
                step /=1.25
                print('step =', step, '\nscale =', scale)
                update_screen = True
            if event.key == pg.K_MINUS:
                scale /= 1.25
                step *= 1.25
                print('step =', step, '\nscale =', scale)
                update_screen = True
            if event.key == pg.K_i:
                if print_info:
                    print_info = False
                else:
                    print_info = True
        if event.type == pg.MOUSEMOTION:
            x_mouse, y_mouse = pg.mouse.get_pos()

    gameDisplay.blit(screen, (0, 0))
    if update_screen:
        screen.fill((255, 255, 255))

        # threads[0].draw(0, part)
        # threads[1].draw(part, height)
        # threads[0].join()
        # threads[1].join()
        for x0 in range(0, width, point_size * 5 // 2):
            for y0 in range(0, height, point_size * 5 // 2):
                coord = canvas_to_real((x0 + x_pos, y0 + y_pos), scale=scale, width=width, height=height)
                p = world.potential_is(coord)
                if 0 <= p and p < 255 * 10000:
                    pg.draw.circle(screen, (255, 255 - p // 10000, 255 - p // 10000), (x0, y0), point_size)
                elif 255 * 10000 <= p:
                    pg.draw.circle(screen, (255, 0, 0), (x0, y0), point_size)
                elif (-255) * 10000 <= p and p < 0:
                    pg.draw.circle(screen, (255 + p // 10000, 255 + p // 10000, 255), (x0, y0), point_size)
                else:
                    pg.draw.circle(screen, (0, 0, 255), (x0, y0), point_size)

        pg.draw.line(screen, (128, 128, 128), (width // 2 - x_pos, 0), (width // 2 - x_pos, height))
        pg.draw.line(screen, (128, 128, 128), (0, height // 2 - y_pos), (width, height // 2 - y_pos))

        for field in world.fields:
            coord = real_to_canv(coord=field.get_coord(), scale=scale, width=width, height=height)
            coord = (coord[0] - x_pos, coord[1] - y_pos)
            if field.get_q() > 0:
                pg.draw.circle(screen, (255, 60, 40), coord, 12)
            else:
                pg.draw.circle(screen, (40, 60, 255), coord, 12)
        background = pg.Surface.copy(screen)
    else:
        screen.blit(source=background, dest=(0, 0))

    # Information strings about fps, x, y, Intensity and ect.
    if print_info:
        fps = str(round(clock.get_fps(), 2))
        coord = canvas_to_real(coord=(x_mouse+x_pos, y_mouse+y_pos), scale=scale, width=width, height=height)
        x2 = str(round(coord[0], 5))
        y2 = str(round(coord[1], 5))
        p = str(round(world.potential_is(coord), 5))
        intensity = str(world.intensity_is(coord).round(5))

        screen.blit(font_screen_info.render('fps: ' + fps, 1, (0, 0, 0)), (0, l_str * 0))
        screen.blit(font_screen_info.render('x: ' + x2 + ' m', 1, (0, 0, 0)), (0, l_str * 1))
        screen.blit(font_screen_info.render('y: ' + y2 + ' m', 1, (0, 0, 0)), (0, l_str * 2))
        screen.blit(font_screen_info.render('Potential: ' + p + ' V', 1, (0, 0, 0)), (0, l_str * 3))
        screen.blit(font_screen_info.render('Intensity: ' + intensity + ' N/C', 1, (0, 0, 0)), (0, l_str * 4))

    #if update_screen:
    #    pg.display.flip()
    #else:
    #    pg.display.update((0, 0, width // 2, l_str * 5))
    pg.display.flip()
    panel.update()
    update_screen = panel.update_it()

pg.quit()
quit()
