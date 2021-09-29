import tkinter as tk
import random
import math
from card import IMG
import locate

class Select(tk.Toplevel):
	def __init__(self, *args, **kwargs):
		super(Select, self).__init__(*args, **kwargs)
		self.WIDTH, self.HEIGHT = 600, 500
		self.spacing = 0.01

		self.title('Select Card')
		self.geometry(f'{self.WIDTH}x{self.HEIGHT}')		
		self.resizable(False, False)

	def __grab(self, img_card, card):
		img_card.place_forget() # remove the card from this window
		self.cards.remove(img_card)
		card.flip(card.img[1])
		card.display_to_opponent(locate.HIDDEN)
		card.location(relx=0.9, rely=0.6) # move the card from main window
		self.__organize()

	def __organize(self):
		window_edge_distance = 0.005
		for card, (r, c) in zip(self.cards, self.coord):
			card.place(
				relw=self.w, relh=self.h, 
				relx=window_edge_distance + ((self.w + self.spacing) * c), 
				rely=window_edge_distance + ((self.h + self.spacing) * r))

	def __clear(self):
		# the window should clear everything therefore this might not be
		# need but not sure yet
		for card in self.cards.keys():
			card.place_forget()
		self.cards.clear()

	def setup(self, column, row):
		# get the size of width and height base on the row and column wanted
		self.w = (self.winfo_width() / column) - self.spacing
		self.h = (self.winfo_height() / row) - self.spacing
		self.coord = [(r, c) for r in range(row) for c in range(column)]

	def display(self, cards):
		self.cards = [
		IMG(self, img=card.img[1], display=card.display,
			cmd=lambda s, c=card: self.__grab(s, c)) for card in cards]
		self.__organize()
		width, height = int(self.WIDTH * self.w), int(self.HEIGHT * self.h)
		for card in self.cards:
			card.set_img(width, height)

class ZoneOption(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(ZoneOption, self).__init__(*args, **kwargs)
		# does not delete any of the same window which might/might not cause 
		# problems later on
		# could resolve this by making a variable = to None and do a check
		# if exist, then delete it and create a new one otherwise new 
		zone_func = {
		'Deck': lambda: self.__display_window(self.zone[7]),
		'Waiting Room': lambda: self.__display_window(self.zone[8]),
		'Hand': lambda: self.__display_window(self.zone[12]),
		'Level': lambda: self.__display_window(self.zone[10]),
		'Memory': lambda: self.__display_window(self.zone[0]),
		'Clock': lambda: self.__display_window(self.zone[11]),
		'Shuffle All (Owner)': self.__shuffle_all,
		'Shuffle Deck': self.__shuffle_deck,
		'Reshuffle': self.__reshuffle,
		}

		self.name = tk.StringVar()
		self.name.set('Deck')
		self.name.trace('w', lambda *args: zone_func[self.name.get()]())
		self.opt = tk.OptionMenu(self, self.name, *zone_func.keys())
		self.opt.config(direction='above')
		self.opt.place(relw=1, relh=1, relx=0, rely=0)

	def __shuffle_all(self):
		self.cards.clear()
		self.__shuffle(self.deck)

	def __shuffle_deck(self):
		self.cards.clear()
		self.__exist_in_zone(self.zone[7])
		self.__shuffle(self.cards)

	def __reshuffle(self):
		self.cards.clear()
		self.__exist_in_zone(self.zone[8])
		self.__shuffle(self.cards)

	def __shuffle(self, cards):
		random.shuffle(cards)

		for card in cards:
			card.show = False
			card.angle = 180
			card.flip(locate.BACKIMG)
			card.display_to_opponent(locate.HIDDEN)
			card.rotate(0)
			card.location(0.365+(0.1*3), 0.61)
			card.set_image()
			card.tkraise()

	def __display_window(self, zone):
		self.cards.clear()
		self.__exist_in_zone(zone)
		temp = Select(self.master)
		temp.setup(9, 6)
		temp.display(self.cards)

	def __exist_in_zone(self, zone):
		# due to it checking the self.deck, it will not show the actual
		# position of the card if its on top or the bottom
		# when checking the any zone but it will show which card came first
		# for any zone other than deck unless __shuffle_all
		for card in self.deck:
			if (card.top() >= zone.top() and card.left() >= zone.left() and
				card.top() <= zone.bottom() and card.left() <= zone.right()):
				self.cards.append(card)

	def setup(self, deck, zone):
		self.deck = deck
		self.zone = zone
		self.cards = []