import random
import tkinter as tk
from info import Information
from mat import WeissSchwarz
import udp
from deckeditor import DeckEditor
import locate

class Window(tk.Tk):
	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		self.geometry('1300x900')
		self.resizable(False, False)

		self.information = Information(self)
		self.information.place(relw=0.3, relh=0.97, relx=0, rely=0)

		self.gamemat = WeissSchwarz(self)
		self.gamemat.place(relw=0.7, relh=1, relx=0.3, rely=0)

		self.playbtn = tk.Button(self, text='Play', command=self.playgame)
		self.playbtn.place(relw=0.1, relh=0.03, relx=0.6, rely=0.485)

		self.editor_btn = tk.Button(
			self, text='Deck Editor', command=self.displayDE)
		self.editor_btn.place(relw=0.06, relh=0.03, relx=0, rely=0.97)

		self.deckeditor = DeckEditor(self, info=self.information.display)

	def playgame(self):
		self.playbtn.place_forget()

		random.shuffle(self.gamemat.pdeck)
		for card in self.gamemat.pdeck:
			card.size = (card.width(), card.height())
			card.display = self.information.display
			card.status['bg'] = 'grey'
			card.set_img()
			card.keybind()
			card.tkraise()

		self.gamemat.option.place(relw=0.2, relh=0.03, relx=0, rely=0.97)

		self.udp_btn = tk.Button(self, text='HOST/JOIN', command=self.displayUDP)
		self.udp_btn.place(relw=0.06, relh=0.03, relx=0.06, rely=0.97)

		text = ' '.join('{}:{}'.format(*card.img) for card in self.gamemat.pdeck)
		self.udpui = udp.UDPUI(
			self.gamemat, text, self.set_deck_msg, 
			self.gamemat.get_odeck, self.information.display)
		self.udpui.withdraw()

	def set_deck_msg(self, msg_func):
		for card in self.gamemat.pdeck:
			card.send_msg = msg_func

	def displayUDP(self):
		# if you close the UDPUI it will cause errors because this was made
		# for just hiding the window and not destroy the window
		if self.udpui.winfo_ismapped():
			self.udpui.withdraw()
		else:
			self.udpui.deiconify()

	def displayDE(self):
		if self.deckeditor.winfo_ismapped():
			self.deckeditor.place_forget()
			self.gamemat.update_pdeck(locate.grab_deck(locate.load_init_deck()))
		else:
			for card in self.gamemat.pdeck: card.place_forget()
			self.deckeditor.place(relw=0.7, relh=1, relx=0.3, rely=0)

if __name__ == '__main__':
	main = Window()
	main.mainloop()