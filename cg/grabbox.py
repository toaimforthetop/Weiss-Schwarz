from card import IMG
import tkinter as tk

class GrabBox(tk.Toplevel):
	def __init__(self, *args, **kwargs):
		super(GrabBox, self).__init__(*args, **kwargs)
		self.geometry('600x500')
		self.title('Select Card')
		self.resizable(False, False)

	def setup(self, column, row):
		self.w = (self.winfo_width() / column) - 0.01
		self.h = (self.winfo_height() / row) - 0.01
		self.coord = [(r, c) for r in range(row) for c in range(column)]

	def __grab(self, img, card):
		img.place_forget()
		self.cards.remove(img)
		card.place(relx=0.27, rely=0.73)
		self.__organize()

	def __organize(self):
		for card, (r, c) in zip(self.cards, self.coord):
			card.place(
				relw=self.w, relh=self.h, 
				relx=0.005+(self.w+0.01)*c, rely=0.005+(self.h+0.01)*r)

	def __clear(self):
		for card in self.cards.keys():
			card.place_forget()
		self.cards.clear()

	def display(self, deck, info):
		self.cards = [IMG(
			self, img=card.img[1], info=info, 
			cmd=lambda s, c=card: self.__grab(s, c)) 
			for card in deck]
		self.__organize()
		for card in self.cards:
			card.set_img(card.winfo_width(), card.winfo_height())