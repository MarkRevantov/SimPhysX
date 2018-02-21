'''Main part of SimPhysX

Simulator of Physical Process
At moment all code in this file. In the future I'll apportion the file
There is only one scene: Simulation of Electrostatic fields
Author: Mikhail Gorokhoov
'''

import numpy as np
import pygame as pg
import tkinter as tk
from scipy import constants as const
from random import randint
'''Constants & literals'''
width = 1200
height = 700
resolution = (width, height)
fps_lim = 60
#Lenth of strings of information of fps, x, y, intensity and ect.
l_str = 40
font = 'Notosans 14'
font2 = 'Notosans 18'
pg.font.init()
font3 = pg.font.SysFont('Courier New', 28, bold='True')
'''Variables'''


tk_settings_is_open = False
# That's crutch
class ControlPanel:
    def __init__(self, world):
        self.world = world
        self.root = tk.Tk()
        self.root.title('Editing the Space')
        width = 600
        height = 600

        frm_main = tk.Frame(self.root, width=width + 60, height=height + 30)
        frm_main.pack()

        self.info_lab = tk.Label(frm_main, font=font2, text='You have 0 fields')
        self.info_lab.grid(row=1, column=1, columnspan=3)

        frm_add = tk.Frame(frm_main)
        frm_edit = tk.Frame(frm_main)
        frm_del = tk.Frame(frm_main)
        frm_id_get = tk.Frame(frm_main)
        frm_coord_get = tk.Frame(frm_main)
        frm_add.grid(row=2, column=1)
        frm_edit.grid(row=2, column=2)
        frm_del.grid(row=2, column=3)
        frm_id_get.grid(row=2, column=4)

        q_lab_add = tk.Label(frm_add, text='Charge (C): ', font=font)
        self.q_add = q_ent_add = tk.Entry(frm_add, font=font)
        x_lab_add = tk.Label(frm_add, text='Position x (m): ', font=font)
        self.x_add = x_ent_add = tk.Entry(frm_add, font=font)
        y_lab_add = tk.Label(frm_add, text='Position y (m): ', font=font)
        self.y_add = y_ent_add = tk.Entry(frm_add, font=font)

        btn_add = tk.Button(frm_add, text='Create a new field', font=font)
        btn_add.bind('<Button-1>', self.btn_new)

        q_lab_add.grid(row=1, column=1)
        q_ent_add.grid(row=1, column=2)
        x_lab_add.grid(row=2, column=1)
        x_ent_add.grid(row=2, column=2)
        y_lab_add.grid(row=3, column=1)
        y_ent_add.grid(row=3, column=2)
        btn_add.grid(row=4, column=1, columnspan=2)

        id_lab_edit = tk.Label(frm_edit, text='ID: ', font=font)
        self.id_edit = id_ent_edit = tk.Entry(frm_edit, font=font)
        q_lab_edit = tk.Label(frm_edit, text='Charge (C): ', font=font)
        self.q_edit = q_ent_edit = tk.Entry(frm_edit, font=font)
        x_lab_edit = tk.Label(frm_edit, text='Position x (m): ', font=font)
        self.x_edit = x_ent_edit = tk.Entry(frm_edit, font=font)
        y_lab_edit = tk.Label(frm_edit, text='Position y (m): ', font=font)
        self.y_edit = y_ent_edit = tk.Entry(frm_edit, font=font)

        btn_edit = tk.Button(frm_edit, text='Edit the field', font=font)
        btn_edit.bind('<Button-1>', self.btn_edit)

        id_lab_edit.grid(row=1, column=1)
        id_ent_edit.grid(row=1, column=2)
        q_lab_edit.grid(row=2, column=1)
        q_ent_edit.grid(row=2, column=2)
        x_lab_edit.grid(row=3, column=1)
        x_ent_edit.grid(row=3, column=2)
        y_lab_edit.grid(row=4, column=1)
        y_ent_edit.grid(row=4, column=2)
        btn_edit.grid(row=5, column=1, columnspan=2)

        id_lab_del = tk.Label(frm_del, text='ID: ', font=font)
        self.id_del = id_ent_del = tk.Entry(frm_del, font=font)

        btn_del = tk.Button(frm_del, text='Delete the field', font=font)
        btn_del.bind('<Button-1>', self.btn_del)
        btn_clear = tk.Button(frm_del, text='Clear the Space', font=font)
        btn_clear.bind('<Button-1>', self.btn_clear)
        id_lab_del.grid(row=1, column=1)
        id_ent_del.grid(row=1, column=2)
        btn_del.grid(row=2, column=1, columnspan=2)
        btn_clear.grid(row=3, column=1, columnspan=2)

        id_lab_id_get = tk.Label(frm_id_get, text='ID: ', font=font)
        self.id_ent_get = id_ent_id_get = tk.Entry(frm_id_get, font=font)
        btn_id_get = tk.Button(frm_id_get, text='View info about the field', font=font)
        btn_id_get.bind('<Button-1>', self.id_get)
        self.q_f_info = tk.Label(frm_id_get, text='q = ', font=font)
        self.x_f_info = tk.Label(frm_id_get, text='x = ', font=font)
        self.y_f_info = tk.Label(frm_id_get, text='y = ', font=font)
        id_lab_id_get.grid(row = 1, column=1)
        id_ent_id_get.grid(row=1, column=2)
        btn_id_get.grid(row=2, column=1, columnspan=2)
        self.q_f_info.grid(row=3, column=1, columnspan=2)
        self.x_f_info.grid(row=4, column=1, columnspan=2)
        self.y_f_info.grid(row=5, column=1, columnspan=2)

        id_lab_coord_get = tk.Label(frm_coord_get, text='Position x (m): ', font=font)
        id_lab_coord_get = tk.Label(frm_coord_get, text='Position y (m): ', font=font)
        btn_id_coord = tk.Button(frm_coord_get, text='View info about the point', font=font)
        self.root.protocol("WM_DELETE_WINDOW", self.tk_closing)
    def tk_closing(self):
        global tk_settings_is_open
        self.root.destroy()
        tk_settings_is_open = False
    def btn_new(self, event):
        print('You press ADD')
        q = float(self.q_add.get())
        x = float(self.x_add.get())
        y = float(self.y_add.get())
        self.world.new_field(q, (x, y))
        self.info_lab['text']='Now you have ' + str(len(world.get_fields())) + ' fields'
    def btn_edit(self, event):
        print('You press EDIT')
        id = int(self.id_edit.get())
        q = float(self.q_edit.get())
        x = float(self.x_edit.get())
        y = float(self.y_edit.get())
        self.world.set_field(id, q, (x, y))
        self.info_lab['text'] = 'You have ' + str(len(world.get_fields())) + ' fields'
    def btn_del(self, event):
        id = int(self.id_del.get())
        print('You have deleted the field with ', id)
        self.world.del_fields(id, id)
        self.info_lab['text'] = 'Now you have ' + str(len(world.get_fields())) + ' fields'
    def btn_clear(self, event):
        print('You have cleared teh space')
        self.world.set_fields([])
        self.info_lab['text'] = 'The space has been cleared'
    def id_get(self, event):
        id = int(self.id_ent_get.get())
        field = self.world.get_field(id)
        x, y = field.get_coord()
        self.q_f_info['text'] = 'q = ' + str(field.get_q()) +' C'
        self.x_f_info['text'] = 'x = ' + str(x) + ' m'
        self.y_f_info['text'] = 'y = ' + str(y) + ' m'
    def update(self):
        self.root.update()

'''Classes'''
# ElectroStatic Field
class ESField:
    '''ElectroStatic Field
    It has:
    q - int - charge
    coord - numpy array(2) - coordinats
    '''
    def __init__(self, q, coord):
        self.q = q
        self.coord = np.array(coord)
        self.e = 1
        self.k = 1 / (4 * const.pi * const.epsilon_0)

    '''sets'''
    def set_q(self, q):
        self.q = q
    def set_coord(self, coord):
        self.coord = np.array(coord)
    def set(self, q, coord):
        self.set_coord(coord)
        self.set_q(q)

    '''gets'''
    def get_q(self):
        return self.q
    def get_coord(self):
        return self.coord

    '''ises'''
    def intensity_is(self, point):
        # r_v - radius-vector
        r_v = point - self.get_coord()
        # r_s - radius-scalar
        r_s = sum(r_v ** 2) ** 0.5
        if r_s >= 10**(-6):
            return (self.k / self.e) * self.get_q() / (r_s ** 3) * r_v
        else:
            return 0
    def potential_is(self, point):
        r_v = point - self.get_coord()
        r_s = sum(r_v ** 2) ** 0.5
        return (self.k / self.e) * (self.get_q() / r_s)
# Spaces of Fields. It has fields
class ESSpace:
    def __init__(self):
        self.fields = []
    def intensity_is(self, point):
        E = np.array([0.0,0.0])
        # The superposition principle
        # E = E0 + E1 + E2 + ... + En
        fields = self.get_fields()
        for field in fields:
            E += field.intensity_is(point)
        return E
    def potential_is(self, point):
        phi = 0
        # The superposition principle
        # phi = phi0 + phi1 + phi2 + ... + phin
        for field in self.get_fields():
            phi += field.potential_is(point)
        return phi
    def Forse_is(self, id):
        field = self.get_field(id)
        return (field.get_q())*self.intensity_is(field.get_coord(),id)
    def get_field(self, id):
        return self.fields[id]
    def get_fields(self):
        return self.fields
    def set_field(self, id, q, coord):
        self.fields[id].set(q, coord)
    def set_fields(self, fields):
        self.fields = fields
    def add_fields(self, fields):
        self.fields+fields
    def new_field(self, q, coord):
        self.fields.append(ESField(q, coord))
    def del_fields(self, left_id, right_id):
        for id in range(left_id, right_id+1):
            self.fields.pop(id)
'''Functions'''
#def render_map():
def canvas_to_real(coord):
    global scale
    x, y = coord
    x = (x - width/2)/scale
    y = (-y + height/2)/scale
    return (x, y)
def real_to_canv(coord):
    global scale, width, height, x_pos, y_pos
    x, y = coord
    x = int((x)*scale + width/2)
    y = int((-y)*scale + height/2)
    return (x, y)


#if there were some changes (drawing fields for example) it will be True until the next frame
#At the first time it's true because that's new simulating
#change = True

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
    if tk_settings_is_open:
        pass
        #change = True

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
            #change = True
        if event.type == pg.MOUSEMOTION:
            x_mouse, y_mouse = pg.mouse.get_pos()

    gameDisplay.blit(screen, (0, 0))
    screen.fill((255, 255, 255))
#if change:
    for x0 in range(0, width, 12):
        for y0 in range(0, height, 12):
            coord = canvas_to_real((x0, y0))
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
        coord = real_to_canv(field.get_coord())
        if field.get_q() > 0:
            pg.draw.circle(screen, (255, 60, 40),coord, 12)
        else:
            pg.draw.circle(screen, (40, 60, 255), coord, 12)


    coord = canvas_to_real((x_mouse, y_mouse))
    p = world.potential_is(coord)
    inten = world.intensity_is(coord)
    x2 = coord[0]
    y2 = coord[1]

    #Information strings about fps, x, y, Intensity and ect.
    screen.blit(font3.render('fps:' + str(round(clock.get_fps(), 2)), 1, (0, 200, 0)), (0, l_str*0))
    screen.blit(font3.render('x:' + str(round(x2, 2)), 1, (0, 200, 0)), (0, l_str*1))
    screen.blit(font3.render('y:' + str(round(y2, 2)), 1, (0, 200, 0)), (0, l_str*2))
    screen.blit(font3.render('Potential:' + str(round(p, 2)), 1, (0, 200, 0)), (0, l_str*3))
    screen.blit(font3.render('Intensity:' + str(inten), 1, (0, 200, 0)), (0, l_str*4))

    # if change:
    #     pg.display.flip()
    # else:
    #     pg.display.update(((0,0),(500, l_str*5)))
    pg.display.flip()
    if tk_settings_is_open == True:
        panel.update()

    #change = False
pg.quit()
quit()
