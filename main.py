'''Main part of SimPhysX

Simulator of Physical Process
There is only one scene: Simulation of Electrostatic fields
Author: Mikhail Gorokhoov
'''


import pygame as pg
from backend import *
from frontend import *

'''Constants & literals'''
width = 1200
height = 700
resolution = (width, height)
fps_lim = 60
l_str = 40 #Lenth of strings of information of fps, x, y, intensity and ect.
pg.font.init()
font_screen_info = pg.font.SysFont('Courier New', 28, bold='True')
'''Variables'''


#Canvas world
x_pos = 0
y_pos = 0

scale = 100

'''PreLoop'''
pg.init()
gameDisplay = pg.display.set_mode(resolution)
screen = pg.Surface(resolution)
pg.display.set_caption('SimPhysX - Electrostatic Fields')
clock = pg.time.Clock()
world = ESSpace()
x_mouse = 0
y_mouse = 0

'''PyGame Loop'''
crashed = False
while not crashed:
    clock.tick(fps_lim)

    '''Events'''
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB and not tk_settings_is_open:
                tk_settings_is_open = True
                panel = ControlPanel(world)
            if event.key == pg.K_UP:
                y_pos += -200
                print('You Press Up')
            if event.key == pg.K_DOWN:
                y_pos += 200
                print('You Press DOWN')
            if event.key == pg.K_LEFT:
                x_pos += -200
                print('You Press LEFT')
            if event.key == pg.K_RIGHT:
                print('You Press RIGHT')
                x_pos += 200
        if event.type == pg.MOUSEMOTION:
            x_mouse, y_mouse = pg.mouse.get_pos()

    gameDisplay.blit(screen, (0, 0))
    screen.fill((255, 255, 255))

    for x0 in range(0, width, 12):
        for y0 in range(0, height, 12):
            coord = canvas_to_real((x0, y0), scale=scale, width=width, height=height)
            p = world.potential_is(coord)
            if 0 <= p and p < 255 * 10000:
                pg.draw.circle(screen, (255, 255 - p // 10000, 255 - p // 10000), (x0 - x_pos, y0 + y_pos), 5)
            elif 255 * 10000 <= p:
                pg.draw.circle(screen, (255, 0, 0), (x0 - x_pos, y0 + y_pos), 5)
            elif (-255)*10000 <= p and p < 0:
                pg.draw.circle(screen, (255 + p // 10000, 255 + p // 10000, 255), (x0 - x_pos, y0 + y_pos), 5)
            else:
                pg.draw.circle(screen, (0, 0, 255), (x0 - x_pos, y0 + y_pos), 5)
    pg.draw.line(screen, (128, 128, 128), (width // 2 - x_pos, 0), (width // 2 - x_pos, height))
    pg.draw.line(screen, (128, 128, 128), (0, height // 2 - y_pos), (width, height // 2 - y_pos))
    for field in world.fields:
        coord = real_to_canv(coord=field.get_coord(), scale=scale, width=width, height=height)
        if field.get_q() > 0:
            pg.draw.circle(screen, (255, 60, 40),coord, 12)
        else:
            pg.draw.circle(screen, (40, 60, 255), coord, 12)


    coord = canvas_to_real(coord=(x_mouse, y_mouse), scale=scale, width=width, height=height)
    p = world.potential_is(coord)
    intensity = world.intensity_is(coord)
    x2 = coord[0]
    y2 = coord[1]

    #Information strings about fps, x, y, Intensity and ect.
    screen.blit(font_screen_info.render('fps: ' + str(round(clock.get_fps(), 2)), 1, (0, 0, 0)), (0, l_str*0))
    screen.blit(font_screen_info.render('x: ' + str(round(x2, 2)), 1, (0, 0, 0)), (0, l_str*1))
    screen.blit(font_screen_info.render('y: ' + str(round(y2, 2)), 1, (0, 0, 0)), (0, l_str*2))
    screen.blit(font_screen_info.render('Potential: ' + str(round(p, 2)), 1, (0, 0, 0)), (0, l_str*3))
    screen.blit(font_screen_info.render('Intensity: ' + str(intensity), 1, (0, 0, 0)), (0, l_str*4))

    pg.display.flip()
    if tk_settings_is_open == True:
        panel.update()

pg.quit()
quit()
