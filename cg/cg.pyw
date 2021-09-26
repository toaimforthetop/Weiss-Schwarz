import deckeditor
import infobox
from card import Card, OCard
import grabbox
import udp
import tkinter as tk
import random

class Zone(tk.Label):
	def __init(self, *args, **kwargs):
		super(Zone, self).__init__(*args, **kwargs)

	def top(self):
		return self.winfo_x()

	def left(self):
		return self.winfo_y()

	def bottom(self):
		return self.top() + self.winfo_width()

	def right(self):
		return self.left() + self.winfo_height()

	def width(self):
		return self.winfo_width()

	def height(self):
		return self.winfo_height()

	def zone_drop(self, card, *, rotate=True, angle=180, show=False, flip=False, hide=False):
		if card.top() < self.top() > card.bottom():
			return

		if card.top() > self.bottom() < card.bottom():
			return

		if card.left() < self.left() > card.right():
			return

		if card.left() > self.right() < card.right():
			return

		x = self.top() / card.master.winfo_width()
		y = self.left() / card.master.winfo_height()
		card.placement(x, y)

		if rotate:
			card.angle = angle
			card.rotate()

		if show:
			card.show = True
			card.state()

		if hide:
			card.cur_img = card.img[1]
			card.flip()
			card.show = False
			card.state()

		if flip:
			card.cur_img = '1.png'
			card.flip()

class Display(tk.Toplevel):
	def __init__(self, *args, **kwargs):
		super(Display, self).__init__(*args, **kwargs)

		zone = {
		'Deck': self.deck,
		'Waiting Room': self.waitingroom,
		'Shuffle All': self.shuffle_all,
		}

		self.zonebtn = [
		tk.Button(self, text=k, command=v)
		for k, v in zone.items()]
		for btn in self.zonebtn:
			btn.pack()

	def setup(self, playerdeck, playerzone, opponentdeck, opponentzone):
		self.pdeck = playerdeck
		self.pzone = playerzone
		self.odeck = opponentdeck
		self.ozone = opponentzone
		self.cards = []

	def shuffle_all(self):
		random.shuffle(self.pdeck)

		for card in self.pdeck:
			card.show = False
			card.angle = 180
			card.cur_img = '1.png'
			card.set_img()
			card.place(relx=0.8, rely=0.6)
			card.tkraise()
			card.rotate()

	def deck(self):
		self.cards.clear()
		self.existinzone(self.pdeck, self.pzone[0])
		temp = grabbox.GrabBox(self.master)
		temp.setup(9, 6)
		temp.display(self.cards, None)

	def waitingroom(self):
		self.cards.clear()
		self.existinzone(self.pdeck, self.pzone[1])
		temp = grabbox.GrabBox(self.master)
		temp.setup(9, 6)
		temp.display(self.cards, None)

	def existinzone(self, cards, zone):
		for card in cards:
			if card.top() == zone.top() and card.left() == zone.left():
				self.cards.append(card)

class Window(tk.Tk):
	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		self.geometry('1600x900')
		self.title('CG')

		actual_card_sz = [63, 88] # millimeter
		pixel_conv, in_game_sz = 3.7795275591, 3.4
		self.update_idletasks()
		w = actual_card_sz[0] * pixel_conv / self.winfo_width() / in_game_sz
		h = actual_card_sz[1] * pixel_conv / self.winfo_height() / in_game_sz
		self.CW = w
		self.CH = h

		self.playerZone()
		self.oppoenentZone()

		self.infobox = infobox.InfoBox(self)
		self.infobox.place(relw=0.25, relh=0.97, relx=0, rely=0)
		self.infobox.display('pic/1.png')

		self.de_btn = tk.Button(self, text='Deck Editor', command=self.deckeditor_screen)
		self.de_btn.place(relw=0.06, relh=0.03, relx=0, rely=0.97)

		self.udp_btn = tk.Button(self, text='HOST/JOIN', command=self.udp_placement)
		self.udp_btn.place(relw=0.06, relh=0.03, relx=0.06, rely=0.97)

		self.deckeditor = deckeditor.DeckEditor(self, info=self.infobox.display)
		self.get_pdeck()

		text = ' '.join('{}:{}'.format(*card.img) for card in self.pdeck)
		self.udpui = udp.UDPUI(self, text, self.set_deck_msg, self.get_odeck)
		self.udpui.withdraw()

		self.odeck = []
		self.bind('<q>', self.displayzone)

	def displayzone(self, event):
		temp = Display(self)
		temp.setup(self.pdeck, self.pz, self.odeck, self.oz)

	def udp_placement(self):
		# if you close the UDPUI it will cause errors because this was made
		# for just hiding the window and not destroy the window
		if self.udpui.winfo_ismapped():
			self.udpui.withdraw()
		else:
			self.udpui.deiconify()

	def set_deck_msg(self, msg_func):
		for card in self.pdeck:
			card.set_msg(msg_func)

	def deckeditor_screen(self):
		if self.deckeditor.winfo_ismapped():
			self.deckeditor.place_forget()
			self.get_pdeck()
		else:
			for card in self.pdeck:
				card.place_forget()
			self.deckeditor.place(relw=0.75, relh=1, relx=0.25, rely=0)
			self.pdeck = None

	def get_odeck(self, deck):
		for img in deck:
			e, i = img.split(':')
			self.odeck.append(OCard(self, img=(e, i)))

		for card in self.odeck:
			card.place(relw=self.CW, relh=self.CH, relx=0.27, rely=self.CH+0.02)
			card.keybind(self.CW, self.CH, self.infobox.display)
			card.update_idletasks()
			card.set_img()

	def get_pdeck(self):
		with open('misc/load.txt', 'r', encoding='utf-8') as f:
			deck_name = f.read()

		with open(f'deck/{deck_name}', 'r', encoding='utf-8') as f:
			self.pdeck = [Card(self, img=(e, img)) 
				for e, img in enumerate(f.read().split('\n'))]

		for card in self.pdeck:
			card.place(relw=self.CW, relh=self.CH, relx=0.8, rely=0.6)
			card.keybind(self.CW, self.CH , self.infobox.display)
			card.collision = self.collide_to_zone
			card.update_idletasks()
			card.set_img()

	def collide_to_zone(self, card):
		self.pz[0].zone_drop(card, hide=True)
		self.pz[1].zone_drop(card, show=True, flip=True)
		for zone in self.pz[2:7]:
			zone.zone_drop(card)

		self.pmemory.zone_drop(card, angle=0)
		self.pclimax.zone_drop(card, angle=0, show=True, flip=True)
		self.pstock.zone_drop(card, rotate=False, hide=True)
		self.plevel.zone_drop(card, rotate=False, show=True, flip=True)
		self.pclock.zone_drop(card, show=True, flip=True)
		self.phand.zone_drop(card, hide=True, flip=True)

	def playerZone(self):
		self.pstock = Zone(self, text='Stock', relief='solid', bd=1)
		self.pstock.place(relw=0.061, relh=0.3, relx=0.3, rely=0.5)
		self.pclimax = Zone(self, text='Climax', relief='solid', bd=1)
		self.pclimax.place(relw=0.061, relh=0.078, relx=0.4, rely=0.5)
		self.plevel = Zone(self, text='Level', relief='solid', bd=1)
		self.plevel.place(relw=0.061, relh=0.12, relx=0.4, rely=0.6)
		self.pclock = Zone(self, text='Clock', relief='solid', bd=1)
		self.pclock.place(relw=0.3, relh=self.CH, relx=0.48, rely=0.75)
		self.phand = Zone(self, text='Hand', relief='solid', bd=1)
		self.phand.place(relw=0.3, relh=self.CH, relx=0.48, rely=0.86)
		self.pmemory = Zone(self, text='Memory', relief='solid', bd=1)
		self.pmemory.place(relw=0.061, relh=0.078, relx=0.8, rely=0.5)

		texts = ['Deck', 'Waiting\nRoom', 'CR', 'CC', 'CL', 'BR', 'BL', 'Memory']
		self.pz = [Zone(self, text=txt, relief='solid', bd=1) for txt in texts]
		self.pz[0].place(relw=self.CW, relh=self.CH, relx=0.8, rely=0.6)
		self.pz[1].place(relw=self.CW, relh=self.CH, relx=0.8, rely=0.73)
		self.pz[2].place(relw=self.CW, relh=self.CH, relx=0.7, rely=0.5)
		self.pz[3].place(relw=self.CW, relh=self.CH, relx=0.6, rely=0.5)
		self.pz[4].place(relw=self.CW, relh=self.CH, relx=0.5, rely=0.5)
		self.pz[5].place(relw=self.CW, relh=self.CH, relx=0.65, rely=0.63)
		self.pz[6].place(relw=self.CW, relh=self.CH, relx=0.55, rely=0.63)

	def oppoenentZone(self):
		self.ostock = Zone(self, text='Stock', relief='solid', bd=1)
		self.ostock.place(relw=0.061, relh=0.3, relx=0.9, rely=0.19)
		self.oclimax = Zone(self, text='Climax', relief='solid', bd=1)
		self.oclimax.place(relw=0.061, relh=0.078, relx=0.8, rely=0.42)
		self.olevel = Zone(self, text='Level', relief='solid', bd=1)
		self.olevel.place(relw=0.061, relh=0.12, relx=0.8, rely=0.27)
		self.oclock = Zone(self, text='Clock', relief='solid', bd=1)
		self.oclock.place(relw=0.3, relh=self.CH, relx=0.48, rely=0.14)
		self.ohand = Zone(self, text='Hand', relief='solid', bd=1)
		self.ohand.place(relw=0.3, relh=self.CH, relx=0.48, rely=0.03)
		self.omemory = Zone(self, text='Memory', relief='solid', bd=1)
		self.omemory.place(relw=0.061, relh=0.078, relx=0.4, rely=0.42)

		texts = ['Deck', 'Waiting\nRoom', 'CL', 'CC', 'CR', 'BL', 'BR', 'Memory']
		self.oz = [Zone(self, text=txt, relief='solid', bd=1) for txt in texts]
		self.oz[0].place(relw=self.CW, relh=self.CH, relx=0.41, rely=0.29)
		self.oz[1].place(relw=self.CW, relh=self.CH, relx=0.41, rely=0.16)
		self.oz[2].place(relw=self.CW, relh=self.CH, relx=0.7, rely=0.39)
		self.oz[3].place(relw=self.CW, relh=self.CH, relx=0.6, rely=0.39)
		self.oz[4].place(relw=self.CW, relh=self.CH, relx=0.5, rely=0.39)
		self.oz[5].place(relw=self.CW, relh=self.CH, relx=0.65, rely=0.26)
		self.oz[6].place(relw=self.CW, relh=self.CH, relx=0.55, rely=0.26)

if __name__ == '__main__':
	rt = Window()
	rt.mainloop()