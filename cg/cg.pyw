import deckeditor
import infobox
from card import Card, OCard
import selectbox
import udp
import tkinter as tk

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

		self.infobox = infobox.InfoBox(self)
		self.infobox.place(relw=0.25, relh=0.97, relx=0, rely=0)
		self.infobox.display('pic/1.png')

		self.de_btn = tk.Button(self, text='DE', command=self.de_screen)
		self.de_btn.place(relw=0.06, relh=0.03, relx=0, rely=0.97)

		self.udp_btn = tk.Button(self, text='UDP', command=self.udp_placement)
		self.udp_btn.place(relw=0.06, relh=0.03, relx=0.06, rely=0.97)

		self.deckeditor = deckeditor.DeckEditor(self, info=self.infobox.display)
		self.get_pdeck()

		text = ''
		for card in self.pdeck:
			text += '{}:{} '.format(*card.img)
		self.udpui = udp.UDPUI(self, text, self.set_deck_msg, self.get_odeck)
		self.udpui.withdraw()

		self.sb = selectbox.SelectBox(self, info=self.infobox.display)
		self.sb.keybind()

	def udp_placement(self):
		if self.udpui.winfo_ismapped():
			self.sb.keybind()
			self.udpui.withdraw()
		else:
			# if selected before clicking udp button it will shift the cards
			# down to where the button is at, to solve this i place unbind 
			# here which cause cards to disappear to get cards back, just 
			# click de twice which should get it back
			# to solve this issue will be to find a way to make item not move
			# cards on release
			self.sb.unbind()
			self.udpui.deiconify()

	def set_deck_msg(self, msg_func):
		for card in self.pdeck:
			card.set_msg(msg_func)

	def get_odeck(self, deck):
		self.odeck = []
		for img in deck:
			e, i = img.split(':')
			self.odeck.append(OCard(self, img=(e, i)))

		for card in self.odeck:
			card.place(relw=self.CW, relh=self.CH, relx=0.27, rely=self.CH+0.02)
			card.keybind(self.CW, self.CH, self.infobox.display)
			card.update_idletasks()
			card.set_img('1.png')

	def de_screen(self):
		if self.deckeditor.winfo_ismapped():
			self.deckeditor.place_forget()
			self.get_pdeck()
			self.sb.keybind()
		else:
			self.sb.unbind()
			for card in self.pdeck:
				card.place_forget()
			self.deckeditor.place(relw=0.75, relh=1, relx=0.25, rely=0)
			self.pdeck = None

	def get_pdeck(self):
		with open('misc/load.txt', 'r', encoding='utf-8') as f:
			deck_name = f.read()

		with open(f'deck/{deck_name}', 'r', encoding='utf-8') as f:
			self.pdeck = [Card(self, img=(e, img)) 
				for e, img in enumerate(f.read().split('\n'))]

		for card in self.pdeck:
			card.place(relw=self.CW, relh=self.CH, relx=0.94, rely=0.73)
			card.keybind(self.CW, self.CH , self.infobox.display)
			card.update_idletasks()
			card.set_img('1.png')

if __name__ == '__main__':
	rt = Window()
	rt.mainloop()