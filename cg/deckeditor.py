from page import Page
from card import IMG
from thread_func import threading
from search import FilterSearch
from PIL import Image, ImageTk
import tkinter as tk
import os
import math
import locate

class Box(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(Box, self).__init__(*args, **kwargs)

class CardList(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(CardList, self).__init__(*args, **kwargs)

		self.page = Page(self)
		self.page.place(relw=1, relh=0.03, relx=0, rely=0.03)

		self.box = Box(self, relief='solid', bd=1)
		self.box.place(relw=1, relh=0.94, relx=0, rely=0.06)

		self.search = tk.Entry(self)
		self.search.place(relw=0.85, relh=0.03, relx=0, rely=0)

		tk.Button(self, text='Q').place(
			relw=0.075, relh=0.03, relx=0.85, rely=0)
		tk.Button(self, text='F', 
			command=lambda: FilterSearch(self)).place(
			relw=0.075, relh=0.03, relx=0.925, rely=0)
		tk.Button(self, text='Clear').place(
			relw=0.075, relh=0.03, relx=0.85, rely=0.03)

class DeckProfile(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(DeckProfile, self).__init__(*args, **kwargs)

		self.deck_name = tk.StringVar()
		self.deck_name.set(locate.load_init_deck())
		self.deck_name.trace('w', lambda *args: self.__load_selected_deck())
		self.opt = tk.OptionMenu(self, self.deck_name, '')
		self.__update_option_list()
		self.opt.place(relw=0.8, relh=0.03, relx=0, rely=0)

		self.save = tk.Button(self, text='Save', 
			command=lambda: locate.save(
				self.deck_name.get(),
				[card.img for card in self.box.cards]))
		self.save.place(relw=0.1, relh=0.03, relx=0.8, rely=0)

		self.delete = tk.Button(self, text='Delete', command=self.__delete)
		self.delete.place(relw=0.1, relh=0.03, relx=0.7, rely=0.03)

		tk.Button(self, text='Save As', command=self.__save_as).place(
			relw=0.1, relh=0.03, relx=0.8, rely=0.03)

		self.sort = tk.Button(self, text='Sort', command=self.__sort)
		self.sort.place(relw=0.1, relh=0.03, relx=0.9, rely=0.03)

		self.clear = tk.Button(self, text='Clear', command=self.__clear)
		self.clear.place(relw=0.1, relh=0.03, relx=0.9, rely=0)

		self.box = Box(self, relief='solid', bd=1)
		self.box.place(relw=1, relh=0.94, relx=0, rely=0.06)

	def __load_selected_deck(self):
		print(locate.grab_deck(self.deck_name.get()))
		self.__update(self.deck_name.get())

	def __update_option_list(self):
		self.opt['menu'].delete(0, 'end')

		for n in os.listdir(f'{locate.location()}/decks'):
			self.opt['menu'].add_command(
				label=n, command=lambda x=n: self.deck_name.set(x))

	def __update(self, name):
		self.deck_name.set(name)
		locate.update_init_load(name)
		self.__update_option_list()

	def __status(self):
		self.save['state'] = 'normal' if self.box.cards else 'disable'
		self.clear['state'] = self.save['state']
		self.sort['state'] = self.save['state']
		self.delete['state'] = self.save['state']
	
	def __clear(self):
		self.clear['state'] = 'disable'
		self.sort['state'] = 'disable'

	def __delete(self):
		if not locate.delete(self.deck_name.get()): return
		decks = os.listdir(locate.DECKFLD)
		self.__update(decks[-1] if decks else '')

	def __save_as(self):
		if not locate.save_as([card.img for card in self.box.cards]): return
		self.__update(txt_file_name)

	def __sort(self):
		# self.box.cards.sort(key=lambda card: card.img)
		pass

class DeckEditor(tk.Frame):
	def __init__(self, *args, info, **kwargs):
		super(DeckEditor, self).__init__(*args, **kwargs)

		self.deckprofile = DeckProfile(self)
		self.deckprofile.place(relw=0.5, relh=1, relx=0, rely=0)

		self.cardlist = CardList(self)
		self.cardlist.place(relw=0.5, relh=1, relx=0.5, rely=0)