from thread_func import threading
import tkinter as tk
import socket

class UDP(object):
	def __init__(self):
		super(UDP, self).__init__()
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def connect(self, host, port, buffer, msg):
		try:
			self.socket.connect((host, port))
			self.__buffer = buffer
			self.socket.sendto(msg.encode(), (host, port))
			return f'Connected to {host}:{port}\nSent.\n'
		except Exception as e:
			# return f'Failed to connect to server ({host}).\n'
			return f'{e}'

	def create(self, host, port, buffer):
		try:
			self.socket.bind((host, port))
			self.__buffer = buffer
			return f'Server {host}:{port} created.\nListening for Connection.\n'
		except:
			return f'Fail to create Server ({host}).\n'

	def set_info(self):
		self.__address = None
		while not self.__address:
			msg, self.__address = self.socket.recvfrom(self.__buffer)

		deck = msg.decode()
		return deck.split() if deck else []

	def send_msg(self, msg):
		self.socket.sendto(msg.encode(), self.__address)

	def receive_msg(self):
		return self.socket.recvfrom(self.__buffer)[0].decode()

class UDPUI(tk.Toplevel):
	def __init__(self, parent, player, set_msg, cmd):
		super(UDPUI, self).__init__(parent)
		self.geometry('320x120')
		self.title('Server')
		self.resizable(False, False)

		self.parent = parent
		self.udp = UDP()
		self.__cmd = cmd
		self.set_msg = set_msg
		self.player = player

		lbl = [0.15, 0.05]
		for e, txt in enumerate(['Host IP', 'Port', 'Buffer']):
			tk.Label(self, text=txt, anchor='e').place(
				relw=lbl[0], relx=lbl[1], rely=0.05+(0.20*e))

		validate = self.master.register(lambda char: char.isdigit())
		self.ip = tk.Entry(self)
		self.port = tk.Entry(
			self, validate='key', validatecommand=(validate, '%S'))
		self.buffer = tk.Entry(
			self, validate='key', validatecommand=(validate, '%S'))

		ent = [0.3, 0.22]
		txts = ['0.0.0.0', '8080', '1024']
		entrys = [self.ip, self.port, self.buffer]
		for e, (entry, txt) in enumerate(zip(entrys, txts)):
			entry.place(relw=ent[0], relx=ent[1], rely=0.05+(0.20*e))
			entry.delete(0, 'end')
			entry.insert(0, txt)

		btn = [0.2, 0.7]
		tk.Button(self, text='Host', 
			command=lambda: threading(self.__host)).place(
			relw=btn[0], relx=0.06, rely=btn[1])
		tk.Button(self, text='Join', 
			command=lambda: threading(self.__join)).place(
			relw=btn[0], relx=0.32, rely=btn[1])

		self.box = tk.Text(self, font=('Consolas', 10), state='disabled')
		self.box.place(relw=0.46, relh=1, relx=0.53)

	def __insert(self, txt):
		self.box['state'] = 'normal'
		self.box.insert('end', txt)
		self.box['state'] = 'disabled'

	def __host(self):
		self.__insert(self.udp.create(
			self.ip.get(), int(self.port.get()), int(self.buffer.get())))
		opp = self.udp.set_info()
		self.__insert('Receive\n')
		self.udp.send_msg(self.player)
		self.__insert('Sent\n')

		self.set_msg(lambda msg: self.udp.send_msg(msg))
		try: self.__cmd(opp)
		except: pass
		self.recieve_messages()

	def __join(self):
		try:
			self.__insert(self.udp.connect(
				self.ip.get(), int(self.port.get()), int(self.buffer.get()), 
				self.player))
		except:
			return
		opp = self.udp.set_info()
		self.__insert('Receive\n')

		self.set_msg(lambda msg: self.udp.send_msg(msg))
		try: self.__cmd(opp)
		except: pass
		self.recieve_messages()

	def recieve_messages(self):
		def movement(number, img, x, y):
			for c in self.parent.odeck:
				if c.img == (number, img):
					c.movement(float(x), float(y))
					break

		def state(number, img):
			for c in self.parent.odeck:
				if c.img == (number, img):
					c.flip()
					break

		def rotate(number, img, w, h):
			for c in self.parent.odeck:
				if c.img == (number, img):
					c.rotate(float(w), float(h))
					break

		msg_type = {
		'r': rotate,
		's': state,
		'm': movement,
		}

		while socket:
			info = self.udp.receive_msg().split(' ')
			print(*info[1:])
			msg_type[info[0]](*info[1:])