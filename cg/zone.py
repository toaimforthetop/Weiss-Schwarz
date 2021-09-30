from tkinter import Label
import locate
from tkinter.messagebox import askyesno
import math

status = {
'Stock': lambda card: card_state(card, 90, False, False),
'Climax': lambda card: card_state(card, 90, True, True),
'Level': lambda card: card_state(card, 90, True, True),
'Memory': lambda card: card.rotate(90), # public zone with exceptions
'Deck': lambda card: card_state(card, 0, False, False),
'Waiting\nRoom': lambda card: card_state(card, 0, True, True),
'Clock': lambda card: card_state(card, 0, True, True),
'Hand': lambda card: card_state(card, 0, True, False),
'Select': lambda card: card_state(card, 0, True, True),
}

def card_state(card, angle, flip, state):
	card.display_to_opponent(locate.SHOW if state else locate.HIDDEN)
	card.flip(card.img[1] if flip else locate.BACKIMG)
	card.rotate(angle)

class Zone(Label):
	def __init__(self, *args, **kwargs):
		super(Zone, self).__init__(*args, **kwargs)
		self.cards = []

	def __to_location(self, card):
		x = self.top() / self.master.winfo_width()
		y = self.left() / self.master.winfo_height()
		card.location(x, y)
		card.leave_zone = self.leave

	def __enter(self, card):
		self.__to_location(card)
		self.cards.append(card)

	def __organize(self, side):
		zone_size = self.width() if side else self.height()
		card_size = self.cards[0].width() if side else self.cards[0].height()
		divided_by = (zone_size-card_size) / card_size
		length = math.ceil(len(self.cards) / divided_by)
		for e, card in enumerate(self.cards):
			x = self.top() + (card.width() / length) * (e if side else 0)
			y = self.left() + (card.height() / length) * (0 if side else e)
			relx = x / self.master.winfo_width()
			rely = y / self.master.winfo_height()
			card.location(relx, rely)

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

	def clear_all(self):
		for card in self.cards:
			card.leave_zone = lambda *args: None
		self.cards.clear()

	def leave(self, card):
		card.leave_zone = lambda *args: None
		self.cards.remove(card)

	def add(self, cards):
		for card in cards:
			card.leave_zone = self.leave
		self.cards.extend(cards)

	def add_to_bottom(self, card):
		self.__to_location(card)
		cards = [card] + self.cards
		self.cards = cards
		for card in self.cards:
			card.tkraise()

	def collision(self, card, zone='', extend=False, side=False, display=False):
		if (card.top() < self.top() > card.bottom() or 
			card.top() > self.bottom() < card.bottom() or
			card.left() < self.left() > card.right() or 
			card.left() > self.right() < card.right()):
			return False

		self.__enter(card)
		if extend: self.__organize(side)
		status.get(zone, lambda *args: None)(card)

		if display and card.status['bg'] != locate.SHOW:
			if askyesno('Confirmation', f'Do you want to show {card.img[1]}?'):
				card.display_to_opponent(locate.SHOW)
				card.flip(card.img[1])

		return True