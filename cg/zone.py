from tkinter import Label
import locate

def state(card, angle, flip, state):
	card.rotate(angle)
	card.display_to_opponent(locate.SHOW if state else locate.HIDDEN)
	card.flip(card.img[1] if flip else locate.BACKIMG)

class Zone(Label):
	def __init__(self, *args, **kwargs):
		super(Zone, self).__init__(*args, **kwargs)
		self.cards = []

	def __varify(self):
		count = 0
		while count != len(self.cards):
			if (self.cards[count].top() < self.top() or 
				self.cards[count].left() < self.left() or 
				self.cards[count].bottom() > self.bottom() or 
				self.cards[count].right() > self.right()):
				self.cards.remove(self.cards[count])
				count = count-1 if count > 0 else 0
			else:
				count += 1

	def __placement(self, card, side):
		for e, card in enumerate(self.cards):
			x = self.top() + (card.width() / 3  * (e if side else 0))
			relx = x / self.master.winfo_width()
			y = self.left() + (card.height() / 3 * (0 if side else e))
			rely = y / self.master.winfo_height()
			card.location(relx, rely)

	def __organize(self, card, side=False):
		self.__varify()
		if card in self.cards: return

		self.cards.append(card)
		self.__placement(card, side)

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

	def collision(
		self, card, status=lambda *args: None, extend=False, side=False):
		if card.top() < self.top() > card.bottom():
			return

		if card.top() > self.bottom() < card.bottom():
			return

		if card.left() < self.left() > card.right():
			return

		if card.left() > self.right() < card.right():
			return

		if extend:
			self.__organize(card, side)
		else:
			x = self.top() / self.master.winfo_width()
			y = self.left() / self.master.winfo_height()
			card.location(x, y)

		status(card)