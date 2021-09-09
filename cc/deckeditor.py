from page import Page
from card import IMG
from thread_func import threading
from search import FilterSearch
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.simpledialog import askstring
import os
import math

DECK_FLR = 'deck/'

class Box(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(Box, self).__init__(*args, **kwargs)

	def setup(self, column, row):
		self.w = (self.winfo_width() / column) - 0.01
		self.h = (self.winfo_height() / row) - 0.01
		self.coord = [(r, c) for r in range(row) for c in range(column)]

	def display(self, imgs, info=print, cmd=print):
		self.cards = [IMG(self, img=i, info=info, cmd=cmd) for i in imgs]
		self.organize()
		for card in self.cards:
			card.set_img(card.winfo_width(), card.winfo_height())

	def organize(self):
		for card, (r, c) in zip(self.cards, self.coord):
			card.place(
				relw=self.w, relh=self.h, 
				relx=0.005+(self.w+0.01)*c, rely=0.005+(self.h+0.01)*r)

	def forget(self):
		for card in self.cards:
			card.place_forget()

	def clear(self):
		self.forget()
		self.cards.clear()

	def add(self, card, info=print, cmd=print):
		self.cards.append(IMG(self, img=card.img, info=info, cmd=cmd))
		self.organize()
		self.cards[-1].set_img(card.winfo_width(), card.winfo_height())

	def remove(self, card):
		card.place_forget()
		self.cards.remove(card)
		self.organize()

class CardList(tk.Frame):
	def __init__(self, *args, info=print, cmd=print, **kwargs):
		super(CardList, self).__init__(*args, **kwargs)
		self.info = info
		self.cmd = cmd
		self.get_imgs()

		self.page = Page(self, cmd=self.__load_page)
		self.page.place(relw=1, relh=0.03, relx=0, rely=0.03)
		self.page.set_max(math.ceil(len(self.imgs) / (9 * 9)))

		self.box = Box(self, relief='solid', bd=1)
		self.box.place(relw=1, relh=0.94, relx=0, rely=0.06)
		self.box.setup(9, 9)
		self.box.display(self.imgs[:(9*9)], self.info, self.cmd)

		self.search = tk.Entry(self)
		self.search.place(relw=0.85, relh=0.03, relx=0, rely=0)
		self.search.bind('<Return>', lambda e: self.__search())

		tk.Button(self, text='Q', command=self.__search).place(
			relw=0.075, relh=0.03, relx=0.85, rely=0)
		tk.Button(self, text='F', 
			command=lambda: FilterSearch(self, cmd=self.filter_search)).place(
			relw=0.075, relh=0.03, relx=0.925, rely=0)
		tk.Button(self, text='Clear', command=self.clear).place(
			relw=0.075, relh=0.03, relx=0.85, rely=0.03)

	def get_imgs(self):
		self.imgs = os.listdir('pic/')
		self.imgs.sort()
		self.imgs = self.imgs[1:]

	def __search(self):
		self.box.clear()

		searched = []
		for img in self.imgs:
			try:
				path = 'info/{}.txt'.format(img.rsplit('.')[0])
				with open(path, 'r', encoding='utf-8') as f:
					if self.search.get().lower() in f.read().lower():
						searched.append(img)
			except: print(path)

		self.imgs.clear()
		self.imgs = searched
		self.page.set_max(math.ceil(len(self.imgs) / (9*9)))
		self.page.page(1 if self.imgs else 0)
		self.__load_page(1 if self.imgs else 0)

	def filter_search(self):
		pass

	def clear(self):
		self.search.delete(0, 'end')
		self.get_imgs()
		self.page.set_max(math.ceil(len(self.imgs) / (9 * 9)))
		self.__load_page(1)
		self.page.page()

	def __load_page(self, page_no):
		start = (9 * 9) * (page_no - 1)
		end = (9 * 9) * page_no
		self.box.clear()
		self.box.display(self.imgs[start:end], self.info, self.cmd)

class DeckFile(tk.Frame):
	LOAD_TXT = 'misc/load.txt'
	def __init__(self, *args, info=print, **kwargs):
		super(DeckFile, self).__init__(*args, **kwargs)
		self.info = info

		self.deck_name = tk.StringVar()
		with open(self.LOAD_TXT, 'r', encoding='utf-8') as f: name = f.read()
		self.deck_name.set(name)
		self.deck_name.trace('w', lambda *args: self.__load_deck())
		self.opt = tk.OptionMenu(self, self.deck_name, '')
		self.__update_menu()
		self.opt.place(relw=0.8, relh=0.03, relx=0, rely=0)

		self.save = tk.Button(self, text='Save', command=self.__save)
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
		self.box.setup(9, 9)
		self.box.display(
			self.set_deck(self.deck_name.get()), self.info, self.remove)
		self.__state()

	def __update_menu(self):
		self.opt['menu'].delete(0, 'end')

		for n in os.listdir(DECK_FLR):
			self.opt['menu'].add_command(
				label=n, command=lambda x=n: self.deck_name.set(x))

	def __update_load(self, name):
		self.deck_name.set(name)
		with open(self.LOAD_TXT, 'w', encoding='utf-8') as f: f.write(name)
		self.__update_menu()

	def __save(self):
		path = f'{DECK_FLR}{self.deck_name.get()}'
		with open(path, 'w', encoding='utf-8') as f:
			f.write('\n'.join([card.img for card in self.box.cards]))

	def __delete(self):
		if not tk.messagebox.askyesno('Confirmation',
			f'Are you sure you want to delete {self.deck_name.get()}?'):
			return

		os.remove(f'{DECK_FLR}{self.deck_name.get()}')
		decks = os.listdir(DECK_FLR)
		self.__update_load(decks[-1] if decks else '')

	def __save_as(self):
		file_name = askstring('Save As', 'Name of Deck')
		if not file_name: return

		while file_name +'.txt' in os.listdir(DECK_FLR):
			file_name += '_'

		txt_file_name = file_name +'.txt'
		path = f'{DECK_FLR}{txt_file_name}'
		with open(path, 'x', encoding='utf-8') as f:
			f.write('\n'.join([card.img for card in self.box.cards]))

		self.__update_load(txt_file_name)

	def __sort(self):
		self.box.cards.sort(key=lambda card: card.img)
		self.box.forget()
		self.box.organize()

	def __clear(self):
		self.box.clear()
		self.clear['state'] = 'disable'
		self.sort['state'] = 'disable'

	def __load_deck(self):
		self.box.clear()
		self.box.display(
			self.set_deck(self.deck_name.get()), self.info, self.remove)
		self.__update_load(self.deck_name.get())
		self.__state()

	def __state(self):
		if self.box.cards:
			self.clear['state'] = 'normal'
			self.sort['state'] = 'normal'
			self.delete['state'] = 'normal'
			self.save['state'] = 'normal'
		else:
			self.clear['state'] = 'disable'
			self.sort['state'] = 'disable'
			self.delete['state'] = 'disable'
			self.save['state'] = 'disable'

	def set_deck(self, file_name):
		with open(f'{DECK_FLR}/{file_name}', 'r', encoding='utf-8') as f:
			return f.read().split('\n')

	def add(self, card_img):
		self.box.add(card_img, self.info, self.remove)

	def remove(self, card):
		self.box.remove(card)

class DeckEditor(tk.Frame):
	def __init__(self, *args, info, **kwargs):
		super(DeckEditor, self).__init__(*args, **kwargs)

		self.dl = DeckFile(self, info=info)
		self.dl.place(relw=0.5, relh=1, relx=0, rely=0)

		self.cl = CardList(self, info=info, cmd=self.dl.add)
		self.cl.place(relw=0.5, relh=1, relx=0.5, rely=0)