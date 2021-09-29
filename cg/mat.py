import tkinter as tk
import locate
from zone import Zone, state
from card import Card, OCard
from select import ZoneOption

class WeissSchwarz(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(WeissSchwarz, self).__init__(*args, **kwargs)

		tk.Frame(self, bg='red', bd=1).place(relh=1, relx=0.5, rely=0)
		tk.Frame(self, bg='red', bd=1).place(relw=1, relx=0, rely=0.5)

		self.playerzone()
		self.opponentzone()

		self.odeck = []
		self.get_pdeck()

		self.option = ZoneOption(self)
		self.option.setup(self.pdeck, self.pz)

	def update_pdeck(self, imgs):
		if not self.pdeck: return

		for e, (card, img) in enumerate(zip(self.pdeck, imgs)):
			card.place(relw=0.07, relh=0.1, relx=0.665, rely=0.61)
			card.current_img = locate.BACKIMG
			card.img = (e, img)
			card.set_img()

	def get_odeck(self, deck, display):
		for img in deck:
			card = OCard(self, img=tuple(img.split(':')))
			card.place(relw=0.07, relh=0.1, relx=0.265, rely=0.29)
			card.keybind(display)
			card.update_idletasks()
			card.set_img()
			self.odeck.append(card)

	def get_pdeck(self):
		deck = locate.grab_deck(locate.load_init_deck())
		if '' in deck and len(deck) == 1: return # nothing exist in the file

		self.pdeck = [Card(self, img=(e, img)) for e, img in enumerate(deck)]

		for card in self.pdeck:
			card.collision = self.collision
			card.place(relw=0.07, relh=0.1, relx=0.665, rely=0.61)

	def collision(self, card):
		for zone in self.pz[:9]:
			zone.collision(
				card, 
				self.status_for_zone.get(zone['text'], lambda *args: None))
		
		for zone in self.pz[9:11]:
			zone.collision(
				card, 
				self.status_for_zone.get(zone['text'], lambda *args: None),
				True)

		for zone in self.pz[11:13]:
			zone.collision(
				card, 
				self.status_for_zone.get(zone['text'], lambda *args: None),
				True, True)

	def playerzone(self):
		self.status_for_zone = {
		'Stock': lambda card: state(card, 90, False, False),
		'Climax': lambda card: state(card, 90, True, True),
		'Level': lambda card: state(card, 90, True, True),
		'Memory': lambda card: card.rotate(90), # public zone with exceptions
		'Deck': lambda card: state(card, 0, False, False),
		'Waiting\nRoom': lambda card: state(card, 0, True, True),
		'Clock': lambda card: state(card, 0, True, True),
		'Hand': lambda card: state(card, 0, True, False),
		}

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
		for name in ['Deck', 'Waiting\nRoom']]
		for e, zone in enumerate(right):
			zone.place(relw=0.07, relh=0.1, relx=0.665, rely=0.61+(0.12*e))

		other = [Zone(self, text=name, relief='solid', bd=1) 
		for name in ['Clock', 'Hand']]
		for e, zone in enumerate(other):
			zone.place(relw=0.4, relh=0.1, relx=0.235, rely=0.76+(0.12*e))

		# its due to collision check to be able to grid out the cards
		self.pz = [memory, climax] + top + bottom + right + [stock, level] 
		self.pz.extend(other)

	def opponentzone(self):
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

		self.oz = [memory, climax] + top + bottom + right + [stock, level]
		self.oz.extend(other)