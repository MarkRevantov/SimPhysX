import tkinter as tk

font = 'Notosans 14'
font2 = 'Notosans 18'
tk_settings_is_open = False

'''GUI'''
class ControlPanel:
    def __init__(self, world):
        self.world = world
        self.root = tk.Tk()
        self.root.title('Editing the Space')
        self.update_screen = True
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
        self.info_lab['text']='Now you have ' + str(len(self.world.get_fields())) + ' fields'
        self.update_screen = True
    def btn_edit(self, event):
        print('You press EDIT')
        id = int(self.id_edit.get())
        q = float(self.q_edit.get())
        x = float(self.x_edit.get())
        y = float(self.y_edit.get())
        self.world.set_field(id, q, (x, y))
        self.info_lab['text'] = 'You have ' + str(len(self.world.get_fields())) + ' fields'
        self.update_screen = True
    def btn_del(self, event):
        id = int(self.id_del.get())
        print('You have deleted the field with ', id)
        self.world.del_fields(id, id)
        self.info_lab['text'] = 'Now you have ' + str(len(self.world.get_fields())) + ' fields'
        self.update_screen = True
    def btn_clear(self, event):
        print('You have cleared teh space')
        self.world.set_fields([])
        self.info_lab['text'] = 'The space has been cleared'
        self.update_screen = True
    def id_get(self, event):
        id = int(self.id_ent_get.get())
        field = self.world.get_field(id)
        x, y = field.get_coord()
        self.q_f_info['text'] = 'q = ' + str(field.get_q()) +' C'
        self.x_f_info['text'] = 'x = ' + str(x) + ' m'
        self.y_f_info['text'] = 'y = ' + str(y) + ' m'
        self.update_screen = True
    def update(self):
        self.root.update()
    def update_it(self):
        x = self.update_screen
        self.update_screen = False
        return x