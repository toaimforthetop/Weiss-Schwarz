import grabbox
import tkinter as tk
import random

class SelectBox(object):
	def __init__(self, root, *, info=print):
		super(SelectBox, self).__init__()
		self.__root = root
		self.__info = info
		self.items = []
		self.__lines = [tk.Frame(
			self.__root, highlightbackground='blue', highlightthickness=1) 
			for i in range(4)]

	def keybind(self):
		self.__root.bind('<Button-1>', self.__pressed)
		self.__root.bind('<s>', lambda e: self.__shuffle())
		self.__root.bind('<w>', lambda e: self.__view())
		self.__root.bind('<f>', lambda e: self.__flip())
		self.__root.bind('<t>', lambda e: self.__state())
		self.__root.bind('<e>', lambda e: self.__flip(), add='+')
		self.__root.bind('<e>', lambda e: self.__state(), add='+')

	def unbind(self):
		self.__box_release()
		self.__item_release()
		self.__root.unbind('<Button-1>')
		self.__root.unbind('<s>')
		self.__root.unbind('<w>')
		self.__root.unbind('<f>')
		self.__root.unbind('<t>')
		self.__root.unbind('<e>')

	def __view(self):
		try: self.grab.destroy()
		except: pass

		self.grab = grabbox.GrabBox(self.__root)
		self.grab.setup(9, 6)
		self.grab.display(self.items, self.__info)
		self.clear_items()

	def __shuffle(self):
		if not self.items: return

		random.shuffle(self.items)

		for card in self.items:
			card.show = False
			card.angle = 0
			card.cur_img = '1.png'
			card.set_img()
			card.place(relx=0.94, rely=0.73)
			card.tkraise()

	def __flip(self):
		for card in self.items:
			card.flip()

	def __state(self):
		for card in self.items:
			card.state()

	def __pressed(self, event):
		if event.widget is self.__root:
			self.__root.focus()
			self.clear_items()
			self.__start = (event.x, event.y)
			self.__root.bind('<B1-Motion>', self.__box_movement)
			self.__root.bind('<ButtonRelease-1>', lambda e: self.__box_release())
		else:
			self.__item_press(event)

	def clear_items(self):
		if not self.items: return
		
		for item in self.items:
			item.highlight()
			self.__root.pdeck.append(item)
		self.items.clear()

	# for selected box
	def __draw_rect(self, end):
		width = end[0] - self.__start[0]
		height = end[1] - self.__start[1]
		new_w = abs(width)
		new_h = abs(height)
		x_edge = self.__start[0] + width
		y_edge  = self.__start[1] + height
		x_flip = x_edge if width < 0 else self.__start[0]
		y_flip = y_edge if height < 0 else self.__start[1]

		self.__lines[0].place(w=new_w, h=0, x=x_flip, y=self.__start[1])
		self.__lines[1].place(w=new_w, h=0, x=x_flip, y=y_edge)
		self.__lines[2].place(w=0, h=new_h, x=self.__start[0], y=y_flip)
		self.__lines[3].place(w=0, h=new_h, x=x_edge, y=y_flip)

	def __hit_box(self, obj, end):
		box_w = abs(end[0] - self.__start[0]) / 2
		box_h = (end[1] - self.__start[1]) / 2
		box_x = self.__lines[0].winfo_x() + box_w
		box_y = self.__lines[0].winfo_y() + box_h

		obj_w, obj_h = obj.winfo_width() / 2, obj.winfo_height() / 2
		obj_x, obj_y = obj.winfo_x() + obj_w, obj.winfo_y() + obj_h

		width = abs(box_x - obj_x) < box_w + obj_w
		height = abs(box_y - obj_y) < abs(box_h) + obj_h
		return width and height

	def __overlap(self, end):
		for card in self.__root.pdeck:
			if self.__hit_box(card, end) and card not in self.items:
				card.config(relief='raised', bg='green')
				self.items.append(card)
				self.__root.pdeck.remove(card)
			elif not self.__hit_box(card, end) and card in self.items:
				self.items.remove(card)
				self.__root.pdeck.append(card)
				card.highlight()

	def __box_movement(self, event):
		self.__draw_rect((event.x, event.y))
		self.__overlap((event.x, event.y))

	def __box_release(self):
		self.__root.unbind('<B1-Motion>')
		self.__root.unbind('<ButtonRelease-1>')

		self.__start = None
		for line in self.__lines:
			line.place_forget()

		# for moving item
	def __item_press(self, event):
		if self.items:
			self.__root.bind(
				'<ButtonRelease-1>', lambda e: self.__item_release())
			self.__widget = event.widget

			for card in self.items:
				if card != self.__widget:
					card.place_forget()
		else:
			# to remove all highlighted cards that are not selected
			for card in self.__root.pdeck:
				card.highlight()

	def __move_to_target(self, card):
		x = self.__widget.winfo_x() / self.__root.winfo_width()
		y = self.__widget.winfo_y() / self.__root.winfo_height()
		card.place(relw=self.__root.CW, relh=self.__root.CH, relx=x, rely=y)
		card.highlight()

	def __item_release(self):
		self.__root.unbind('<B1-Motion>')
		self.__root.unbind('<ButtonRelease-1>')
		
		for card in self.items:
			self.__move_to_target(card)
		self.__widget = None