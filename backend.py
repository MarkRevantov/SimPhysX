import numpy as np
from scipy import constants as const

'''Classes'''
class ESField:
    '''ElectroStatic Field
    It has:
    q - float - charge
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
def canvas_to_real(coord, scale, width, height):
    x, y = coord
    x = (x - width/2)/scale
    y = (-y + height/2)/scale
    return (x, y)
def real_to_canv(coord, scale, width, height):
    x, y = coord
    x = int((x)*scale + width/2)
    y = int((-y)*scale + height/2)
    return (x, y)
def draw_potential(x_start, y_start, x_end, y_end, scale, step, point_size, x_pos, y_pos):
    for x in range(x_start, x_end, point_size * 5 // 2):
        for y in range(y_start, y_end, point_size * 5 // 2):



            '''
            coord = canvas_to_real((x + x_pos, y + y_pos), scale=scale, width=width, height=height)
            p = world.potential_is(coord)
            if 0 <= p and p < 255 * 10000:
                pg.draw.circle(screen, (255, 255 - p // 10000, 255 - p // 10000), (x0, y0), point_size)
            elif 255 * 10000 <= p:
                pg.draw.circle(screen, (255, 0, 0), (x, y), point_size)
            elif (-255) * 10000 <= p and p < 0:
                pg.draw.circle(screen, (255 + p // 10000, 255 + p // 10000, 255), (x0, y0), point_size)
            else:
                pg.draw.circle(screen, (0, 0, 255), (x, y), point_size)
    '''