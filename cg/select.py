import tkinter as tk
import random
import math
from card import IMG
import locate
from tkinter.messagebox import askyesno

def place_bottom_of_deck(deck, cards_to_deck):
	question = 'Are you sure you want to put at bottom of deck {}?'
	name_of_card = [card.img[1] for card in cards_to_deck.cards]
	if not askyesno('Confirmation', question.format(name_of_card)):
		return # if cancel or close

	# send bottom card which is first card in first rather than top
	while len(cards_to_deck.cards):
		card = cards_to_deck.cards[0] 
		card.leave_zone(card)
		deck.add_to_bottom(card)

def shuffle_all(zone):
	if not askyesno('Confirmation','Do you want to Shuffle All?'):
		return

	for z in zone:
		if z == zone[7]: continue
		zone[7].add(z.cards) # add each zone to deck zone
		z.clear_all() # then clear all zone out

	shuffle(zone[7].cards)

def reshuffle(deck, waiting_room):
	deck.add(waiting_room.cards)
	waiting_room.clear_all()
	shuffle(deck.cards)

def shuffle(cards):
	random.shuffle(cards)

	for card in cards:
		card.flip(locate.BACKIMG)
		card.display_to_opponent(locate.HIDDEN)
		card.rotate(0)
		card.location(0.665, 0.61)
		card.set_img()
		card.tkraise()

def display_window(root, cards):
	temp = Select(root)
	temp.setup(9, 6) # (10, 6) works too
	temp.display(cards)

class Select(tk.Toplevel):
	def __init__(self, *args, **kwargs):
		super(Select, self).__init__(*args, **kwargs)
		self.WIDTH, self.HEIGHT = 600, 500
		self.spacing = 0.01

		self.title('Select Card')
		self.geometry(f'{self.WIDTH}x{self.HEIGHT}')		
		self.resizable(False, False)

	def __grab(self, select_card, main_card):
		select_card.place_forget() # remove the card from this window
		self.cards.remove(select_card)
		card = main_card
		card.leave_zone(card)
		card.flip(card.img[1])
		card.display_to_opponent(locate.HIDDEN)
		card.location(relx=0.665, rely=0.85) # move the card from main window
		self.__organize()
		self.destroy()

	def __organize(self):
		window_edge_distance = 0.005
		for card, (r, c) in zip(self.cards, self.coord):
			card.place(
				relw=self.w, relh=self.h, 
				relx=window_edge_distance + ((self.w + self.spacing) * c), 
				rely=window_edge_distance + ((self.h + self.spacing) * r))

	def setup(self, column, row):
		# get the size of width and height base on the row and column wanted
		self.w = (self.winfo_width() / column) - self.spacing
		self.h = (self.winfo_height() / row) - self.spacing
		self.coord = [(r, c) for r in range(row) for c in range(column)]

	def display(self, cards):
		self.cards = [
		IMG(self, img=card.img[1], display=card.display,
			cmd=lambda s, m=card: self.__grab(s, m))  for card in cards]
		self.__organize()
		width, height = int(self.WIDTH * self.w), int(self.HEIGHT * self.h)
		for card in self.cards:
			card.set_img(width, height)