from PIL import Image, ImageTk
from thread_func import threading
import tkinter as tk

BACK_IMG = '1.png'
PIC_FLD = 'pic/{}'

class Card(tk.Label):
	def __init__(self, *args, img=(0, BACK_IMG), **kwargs):
		super(Card, self).__init__(*args, **kwargs)
		self.img = img
		self.angle = 0
		self.cur_img = BACK_IMG
		self.show = False
		self.__msg = lambda *args: None

	def set_msg(self, msg=print):
		self.__msg = msg

	def keybind(self, w, h, info=print):
		self.__info = info
		self.bind('<Configure>', lambda e: threading(self.update_image))
		self.bind('<Button-1>', self.__pressed)
		self.bind('<Button-3>', lambda e: self.__focus())
		self.bind('<f>', lambda e: self.flip())
		self.bind('<t>', lambda e: self.state())
		self.bind('<r>', lambda e: self.__rotate(w, h))
		self.bind('<e>', lambda e: self.__state(), add='+')
		self.bind('<e>', lambda e: self.flip(), add='+')

	def update_image(self):
		self.set_img()

	def __rotate(self, w, h):
		self.angle = {0:90, 90:180, 180:0}[self.angle]

		sh, sw = self.master.winfo_height(), self.master.winfo_width()
		width = (h * sh / sw) if self.angle == 90 else w
		height = (w * sw / sh) if self.angle == 90 else h

		self.place(relw=width, relh=height)
		self.set_img()

		self.__msg('r {} {} {} {}'.format(*self.img, width, height))

	def state(self):
		self.show = not self.show
		self.highlight()
		self.__msg('s {} {}'.format(*self.img))

	def __focus(self):
		if self.focus_get() == self:
			self.master.focus()
		else:
			self.focus_set()

		self.highlight()

	def flip(self):
		self.cur_img = self.img[1] if self.cur_img == BACK_IMG else BACK_IMG
		self.set_img()

	def __pressed(self, e):
		self.focus_set()
		self.tkraise()
		self.start = [e.x, e.y]
		self.bind('<B1-Motion>', self.__movement)
		self.bind('<ButtonRelease-1>', self.__released)
		self.__info(self.cur_img)

	def __movement(self, e):
		x = (self.winfo_x() - self.start[0] + e.x) / self.master.winfo_width()
		y = (self.winfo_y() - self.start[1] + e.y) / self.master.winfo_height()
		self.place(relx=x, rely=y)
		self.__msg('m {} {} {} {}'.format(*self.img, x, y))

	def __released(self, e):
		self.unbind('<B1-Motion>')
		self.unbind('<ButtonRelease-1>')

	def highlight(self):
		if self.focus_get() == self:
			self.config(relief='raised', bg='cyan')
		elif self.show:
			self.config(relief='raised', bg='red')
		else:
			self.config(relief='flat', bg='white')

	def set_img(self):
		try: img = Image.open(PIC_FLD.format(self.cur_img))
		except: img = Image.open(PIC_FLD.format(BACK_IMG))
		rotate_img = img.rotate(self.angle, expand=True)
		resize = (self.winfo_width(), self.winfo_height())
		resize_img = rotate_img.resize(resize, Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(resize_img)
		self.config(image=self.image, anchor='center')

class OCard(tk.Label):
	def __init__(self, *args, img=(0, BACK_IMG), **kwargs):
		super(OCard, self).__init__(*args, **kwargs)
		self.img = img
		self.angle = 180
		self.cur_img = BACK_IMG

	def keybind(self, w, h, info=print):
		self.__info = info
		self.bind('<Configure>', lambda e: threading(self.update_image))
		self.bind('<Button-1>', self.__pressed)

	def __pressed(self, event):
		self.focus_set()
		self.tkraise()
		self.__info(self.cur_img)

	def update_image(self):
		self.set_img()

	def rotate(self, w, h):
		self.angle = {180:-90, -90:0, 0:180}[self.angle]
		self.place(relw=w, relh=h)
		self.set_img()

	def flip(self):
		self.cur_img = self.img[1] if self.cur_img == BACK_IMG else BACK_IMG
		self.set_img()

	def movement(self, x, y):
		self.place(relx=0.94-x+0.27, rely=0.73-y+0.1086922958172549)

	def set_img(self):
		try: img = Image.open(PIC_FLD.format(self.cur_img))
		except: img = Image.open(PIC_FLD.format(BACK_IMG))
		rotate_img = img.rotate(self.angle, expand=True)
		resize = (self.winfo_width(), self.winfo_height())
		resize_img = rotate_img.resize(resize, Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(resize_img)
		self.config(image=self.image, anchor='center')

class IMG(tk.Label):
	def __init__(self, *args, img=BACK_IMG, info=print, cmd=print, **kwargs):
		super(IMG, self).__init__(*args, **kwargs)
		self.img = img
		self.bind('<Configure>', lambda e: threading(self.update_image))
		self.bind('<Button-1>', lambda e: info(self.img))
		self.bind('<Button-3>', lambda e: cmd(self))

	def update_image(self):
		self.set_img(self.winfo_width(), self.winfo_height())

	def set_img(self, w, h):
		try: img = Image.open(PIC_FLD.format(self.img))
		except: img = Image.open(PIC_FLD.format(BACK_IMG))
		resize = img.resize((w, h), Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(resize)
		self.config(image=self.image, anchor='center')