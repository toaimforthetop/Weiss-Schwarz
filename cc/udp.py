from thread_func import threading
import tkinter as tk
import socket

class UDPUI(tk.Label):
	def __init__(self, *args, root, deck, grab, set_msg, **kwargs):
		super(UDPUI, self).__init__(*args, **kwargs)
		self.player = deck
		self.grab = grab
		self.set_msg = set_msg
		self.root = root

		self.entry = tk.Entry(self)
		self.entry.insert(0, '127.0.0.1')
		self.entry.place(relw=0.8, relx=0.1, rely=0.2)

		self.host = tk.Button(
			self, text='Host', command=lambda: threading(self.__host))
		self.host.place(relw=0.2, relh=0.25, relx=0.1, rely=0.6)

		self.join = tk.Button(
			self, text='Join', command=lambda: threading(self.__join))
		self.join.place(relw=0.2, relh=0.25, relx=0.4, rely=0.6)

		self.cancel = tk.Button(self, text='Cancel', command=self.__cancel)
		self.cancel.place(relw=0.2, relh=0.25, relx=0.7, rely=0.6)

		self.PORT = 25565
		self.BUFFER = 1024

	def __cancel(self):
		self.place_forget()

	def __join(self):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			try:
				s.connect((self.entry.get(), self.PORT))
				print(f'Connected to {self.entry.get()}:{self.PORT}')
			except:
				self.entry.delete(0, 'end')
				self.entry.insert(0, 'bind error')
				return

			try:
				text = ''
				for card in self.player:
					text += '{}:{} '.format(*card.img)
				s.sendto(text.encode(), (self.entry.get(), self.PORT))
				print('Sent')			
			except:
				self.entry.delete(0, 'end')
				self.entry.insert(0, 'send error')
				return

			try:
				opp_names = self.get_opp(s)
				print('Recieved')	
			except:
				self.entry.delete(0, 'end')
				self.entry.insert(0, 'get opp deck error')
				return

			self.place_forget()
			self.grab(opp_names)
			self.set_msg(lambda msg: s.sendto(msg.encode(), self.address))
			self.recieve_messages(s)

	def __host(self):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			try:
				s.bind((self.entry.get(), self.PORT))
				print(f'{self.entry.get()}:{self.PORT} created.')
				print('Listening for connection.')
			except: 
				self.entry.delete(0, 'end')
				self.entry.insert(0, 'bind error')
				return

			try:
				opp_names = self.get_opp(s)
				print('Recieved')	
			except:
				self.entry.delete(0, 'end')
				self.entry.insert(0, 'get opp deck error')
				return

			try:
				text = ''
				for card in self.player:
					text += '{}:{} '.format(*card.img)
				s.sendto(text.encode(), self.address)
				print('Sent')			
			except:
				self.entry.delete(0, 'end')
				self.entry.insert(0, 'send error')
				return

			self.place_forget()
			self.grab(opp_names)
			self.set_msg(lambda msg: s.sendto(msg.encode(), self.address))
			self.recieve_messages(s)

	def recieve_messages(self, socket):
		def movement(number, img, x, y):
			for c in self.root.odeck:
				if c.img == (number, img):
					c.movement(float(x), float(y))
					break

		def state(number, img):
			for c in self.root.odeck:
				if c.img == (number, img):
					c.flip()
					break

		def rotate(number, img, w, h):
			for c in self.root.odeck:
				if c.img == (number, img):
					c.rotate(float(w), float(h))
					break

		msg_type = {
		'r': rotate,
		's': state,
		'm': movement,
		}

		while socket:
			info = socket.recvfrom(self.BUFFER)[0].decode().split(' ')
			print(*info[1:])
			msg_type[info[0]](*info[1:])

	def get_opp(self, socket):
		self.address = None
		while not self.address:
			msg, self.address = socket.recvfrom(self.BUFFER)

		deck = msg.decode()
		return deck.split() if deck else []