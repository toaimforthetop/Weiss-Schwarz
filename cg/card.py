from tkinter import Label, Frame
import locate

class Card(Label):
	def __init__(self, *args, img=(0, locate.BACKIMG), **kwargs):
		super(Card, self).__init__(*args, **kwargs)
		self.angle = 0
		self.img = img
		self.size = None
		self.current_img = locate.BACKIMG
		self.collision = lambda *args: None
		self.display = lambda *args: None
		self.send_msg = lambda *args: None
		# these functions below are suppose to be use as a test for ocard
		# in placement without the need of connecting to test it out
		self.m = lambda *args: None
		self.r = lambda *args: None
		self.status = Frame(self)
		self.status.place(relw=0.1, relh=0.1, relx=0.9, rely=0)

	def __pressed(self, event):
		self.focus_set()
		self.tkraise()
		self.start = (event.x, event.y)
		self.bind('<B1-Motion>', self.__movement)
		self.bind('<ButtonRelease-1>', self.__released)
		self.display(self.current_img)

	def __movement(self, event):
		x = (self.winfo_x() - self.start[0] + event.x)
		y = (self.winfo_y() - self.start[1] + event.y)
		relx = x / self.master.winfo_width()
		rely = y / self.master.winfo_height()
		self.location(relx, rely)

	def __released(self, event):
		self.unbind('<B1-Motion>')
		self.unbind('<ButtonRelease-1>')
		self.collision(self)

	def __flip(self, event):
		self.flip(self.img[1] 
			if self.current_img == locate.BACKIMG 
			else locate.BACKIMG)

	def __rotate(self, event):
		self.rotate({0:90, 90:180, 180:0}[self.angle])

	def __display(self, event):
		self.display_to_opponent(locate.SHOW 
			if self.status['bg'] == locate.HIDDEN else locate.HIDDEN)

	def width(self):
		return self.winfo_width()

	def height(self):
		return self.winfo_height()

	def top(self):
		return self.winfo_x()

	def left(self):
		return self.winfo_y()

	def bottom(self):
		return self.top() + self.width()

	def right(self):
		return self.left() + self.height()

	def keybind(self):
		self.bind('<Button-1>', self.__pressed)
		self.bind('<r>', self.__rotate)
		self.bind('<f>', self.__flip)
		self.bind('<d>', self.__display)
		self.bind('<Button-3>', self.__flip, add='+')
		self.bind('<Button-3>', self.__display, add='+')
		
	def location(self, relx, rely):
		self.place(relx=relx, rely=rely)
		self.send_msg('m {} {} {} {}'.format(*self.img, relx, rely))
		self.m(relx, rely)

	def rotate(self, angle):
		self.angle = angle

		width = self.size[1] if self.angle == 90 else self.size[0]
		height = self.size[0] if self.angle == 90 else self.size[1]
		relw = width / self.master.winfo_width()
		relh = height / self.master.winfo_height()

		self.place(relw=relw, relh=relh)
		self.update_idletasks() # workaround for image issue
		# card label updates to the right size, card image does not
		# tried moving full code of set_img in here and replace resize with
		#  (width, height) but it does not work
		# even if the size is right, the image will not be updated
		self.set_img()
		self.send_msg('r {} {} {} {} {}'.format(*self.img, angle, relw, relh))
		self.r(angle, relw, relh)

	def display_to_opponent(self, state):
		self.status.config(bg=state)
		self.status.tkraise()
		self.send_msg('s {} {} {}'.format(*self.img, self.status['bg']))

	def flip(self, img):
		self.current_img = img
		self.set_img()

	def set_img(self):
		self.image = locate.add_image(
			self.current_img, self.width(), self.height(), self.angle)
		self.config(image=self.image, anchor='center')

# the information sent to other OCard works fine
# when card get set to where they have to rotate will cause the issue
# since i made it where movement is the reverse (mirror) of where the Card
# will be place, it in a sense make the point at bottom left corner
# due to this, the rotation becomes an issue; it will resize from the top left
# corner rather than the bottom right corner, thus resulting in the position
# of the image on opponent side to seem off
# to resolve this, you have to find a way where image will rotate (resize) 
# from the bottom left
class OCard(Label):
	def __init__(self, *args, img=(0, locate.BACKIMG), **kwargs):
		super(OCard, self).__init__(*args, **kwargs)
		self.img = img
		self.angle = 180
		self.current_img = locate.BACKIMG

	def keybind(self, info=print):
		self.__info = info
		self.bind('<Button-1>', self.__pressed)

	def __pressed(self, event):
		self.__info(self.current_img)

	def rotate(self, angle, w, h):
		self.angle = {0:180, 90:-90, 180:0}[angle]
		self.place(relw=w, relh=h)
		self.set_img()

	def flip(self, color):
		self.current_img = (self.img[1] 
			if color == locate.SHOW else locate.BACKIMG)
		self.set_img()

	def movement(self, x, y):
		self.place(relx=0.665-x+0.265, rely=0.61-y+0.29)

	def set_img(self):
		self.image = locate.add_image(
			self.current_img, self.winfo_width(), 
			self.winfo_height(), self.angle)
		self.config(image=self.image, anchor='center')

class IMG(Label):
	def __init__(
		self, *args, img=locate.BACKIMG, display=print, cmd=print, **kwargs):
		super(IMG, self).__init__(*args, **kwargs)
		self.img = img
		self.bind('<Button-1>', lambda e: display(self.img))
		self.bind('<Button-3>', lambda e: cmd(self))

	def set_img(self, w, h):
		self.image = locate.add_image(self.img, w, h)
		self.config(image=self.image, anchor='center')