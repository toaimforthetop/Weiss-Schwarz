import random
import tkinter as tk
import locate
from zone import Zone
from card import Card, OCard
import select
import math

class WeissSchwarz(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(WeissSchwarz, self).__init__(*args, **kwargs)

		tk.Frame(self, bg='red', bd=1).place(relh=1, relx=0.5, rely=0)
		tk.Frame(self, bg='red', bd=1).place(relw=1, relx=0, rely=0.5)

		self.player_zone()
		self.opponent_zone()

		self.odeck = []

		self.btns = []
		for e, text in enumerate(
			['Deck', 'Waiting Room', 'Level', 'Clock', 'Hand']):
			btn = tk.Button(self, text=text)
			btn.place(relw=0.1, relh=0.03, relx=0, rely=0.52+(0.04*e))
			self.btns.append(btn)

		self.btns.append(tk.Button(self, text='Bottom of Deck'))
		self.btns[-1].place(relw=0.1, relh=0.03, relx=0.65, rely=0.71+(0.12*2))

		for e, text in enumerate(
			['Shuffle All', 'Shuffle Deck', 'Reshuffle']):
			btn = tk.Button(self, text=text)
			btn.place(relw=0.1, relh=0.03, relx=0.9, rely=0.52+(0.04*e))
			self.btns.append(btn)

		for btn in self.btns:
			btn.config(command=self.zone_func[btn['text']])

	def player_zone(self):
		stock = Zone(self, text='Stock', relief='solid', bd=1)
		stock.place(relw=0.1, relh=0.3, relx=0.105, rely=0.52)

		climax = Zone(self, text='Climax', relief='solid', bd=1)
		climax.place(relw=0.1, relh=0.07, relx=0.235, rely=0.52)

		level = Zone(self, text='Level', relief='solid', bd=1)
		level.place(relw=0.1, relh=0.13, relx=0.235, rely=0.61) 

		top = [Zone(self, text=name, relief='solid', bd=1) 
		for name in ['CL', 'CC', 'CR']]
		for e, zone in enumerate(top):
			zone.place(relw=0.07, relh=0.1, relx=0.365+(0.1*e), rely=0.52)

		memory = Zone(self, text='Memory', relief='solid', bd=1)
		memory.place(relw=0.1, relh=0.07, relx=0.665, rely=0.52)

		bottom = [Zone(self, text=name, relief='solid', bd=1)  
		for name in ['BL', 'BR']]
		for e, zone in enumerate(bottom):
			zone.place(relw=0.07, relh=0.1, relx=0.415+(0.1*e), rely=0.64)

		right = [Zone(self, text=name, relief='solid', bd=1) 
		for name in ['Deck', 'Waiting\nRoom', 'Select']]
		for e, zone in enumerate(right):
			zone.place(relw=0.07, relh=0.1, relx=0.665, rely=0.61+(0.12*e))

		other = [Zone(self, text=name, relief='solid', bd=1) 
		for name in ['Clock', 'Hand']]
		for e, zone in enumerate(other):
			zone.place(relw=0.4, relh=0.1, relx=0.235, rely=0.76+(0.12*e))

		# its due to collision check to be able to grid out the cards
		self.pz = top + bottom + [memory, climax] + right + [stock, level] 
		self.pz.extend(other)

		self.zone_func = {
		'Deck': lambda: select.display_window(self, self.pz[7].cards),
		'Waiting Room': lambda: select.display_window(self, self.pz[8].cards),
		'Hand': lambda: select.display_window(self, self.pz[13].cards),
		'Level': lambda: select.display_window(self, self.pz[11].cards),
		'Memory': lambda: select.display_window(self, self.pz[0].cards),
		'Clock': lambda: select.display_window(self, self.pz[12].cards),
		'Shuffle All': lambda: select.shuffle_all(self.pz),
		'Shuffle Deck': lambda: select.shuffle(self.pz[7].cards),
		'Reshuffle': lambda: select.reshuffle(self.pz[7], self.pz[8]),
		'Bottom of Deck': lambda: select.place_bottom_of_deck(
			self.pz[7], self.pz[9]),
		}

	def opponent_zone(self):
		stock = Zone(self, text='Stock', relief='solid', bd=1)
		stock.place(relw=0.1, relh=0.3, relx=0.665+0.13, rely=0.18)

		climax = Zone(self, text='Climax', relief='solid', bd=1)
		climax.place(relw=0.1, relh=0.07, relx=0.665, rely=0.41)

		level = Zone(self, text='Level', relief='solid', bd=1)
		level.place(relw=0.1, relh=0.13, relx=0.665, rely=0.26)

		top = [Zone(self, text=name, relief='solid', bd=1) 
		for name in ['CR', 'CC', 'CL']]
		for e, zone in enumerate(top):
			zone.place(relw=0.07, relh=0.1, relx=0.365+(0.1*e), rely=0.38)

		memory = Zone(self, text='Memory', relief='solid', bd=1)
		memory.place(relw=0.1, relh=0.07, relx=0.235, rely=0.41)

		bottom = [Zone(self, text=name, relief='solid', bd=1)  
		for name in ['BR', 'BL']]
		for e, zone in enumerate(bottom):
			zone.place(relw=0.07, relh=0.1, relx=0.415+(0.1*e), rely=0.26)

		right = [Zone(self, text=name, relief='solid', bd=1) 
		for name in ['Deck', 'Waiting\nRoom']]
		for e, zone in enumerate(right):
			zone.place(relw=0.07, relh=0.1, relx=0.265, rely=0.29-(0.12*e))

		other = [Zone(self, text=name, relief='solid', bd=1)
		for name in ['Clock', 'Hand']]
		for e, zone in enumerate(other):
			zone.place(relw=0.4, relh=0.1, relx=0.365, rely=0.14-(0.12*e))

		self.oz = top + bottom + [memory, climax] + right + [stock, level]
		self.oz.extend(other)

	def set_deck_msg(self, msg_func):
		for card in self.pz[7].cards:
			card.send_msg = msg_func

	def collision(self, card):
		for zone in self.pz[:5]:
			if zone.collision(card, zone['text'], False, False, True):
				return

		for zone in self.pz[5:10]:
			if zone.collision(card, zone['text']):
				return

		for zone in self.pz[10:12]:
			if zone.collision(card, zone['text'], True):
				return

		for zone in self.pz[12:14]:
			if zone.collision(card, zone['text'], True, True):
				return

	def update_pdeck(self, imgs):
		if not self.pdeck: return

		for e, (card, img) in enumerate(zip(self.pdeck, imgs)):
			card.place(relw=0.07, relh=0.1, relx=0.665, rely=0.61)
			card.current_img = locate.BACKIMG
			card.img = (e, img)
			card.set_img()

	def set_opponent_deck(self, deck, display):
		for img in deck:
			card = OCard(self, img=tuple(img.split(':')))
			card.place(relw=0.07, relh=0.1, relx=0.265, rely=0.29)
			card.keybind(display)
			card.update_idletasks()
			card.set_img()
			self.odeck.append(card)

	def set_player_deck(self, display):
		deck = locate.grab_deck(locate.load_init_deck())
		if '' in deck and len(deck) == 1: return # if nothing exist in the file

		self.pz[7].add(
			[Card(self, img=(e, img)) for e, img in enumerate(deck)])
		random.shuffle(self.pz[7].cards)

		for card in self.pz[7].cards:
			card.leave_zone = self.pz[7].leave
			card.collision = self.collision
			card.display = display
			card.status['bg'] = 'grey'
			card.place(relw=0.07, relh=0.1, relx=0.665, rely=0.61)
			card.update_idletasks()
			card.size = (card.winfo_width(), card.winfo_height())
			card.set_img()
			card.keybind()
			card.tkraise()