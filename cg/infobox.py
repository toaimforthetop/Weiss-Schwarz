from PIL import ImageTk, Image
import page
import tkinter as tk
import os

PIC_FLD = 'pic/{}'

class InfoBox(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(InfoBox, self).__init__(*args, **kwargs)

		self.img = tk.Label(self)
		self.img.place(relw=0.94, relh=0.6, relx=0, rely=0)

		self.box = tk.Text(self, state='disable')
		self.box.place(relw=1, relh=0.4, relx=0, rely=0.6)

		with open('misc/format infobox.txt', 'r', encoding='utf-8') as f:
			self.info_format = f.read()

	def __insert(self, msg):
		self.box.config(state='normal')
		self.box.delete('1.0', 'end')
		self.box.insert('end', msg)
		self.box.config(state='disable')

	def display(self, name):
		self.set_img(name)
		self.set_info('{}.txt'.format(name.rsplit('.')[0]))

	def set_img(self, name):
		try: img = Image.open(PIC_FLD.format(name))
		except: img = Image.open(PIC_FLD.format('1.png'))
		# initial image will not show, doesn't work when call from itself
		# will show afterward when called from a input
		# cause is due to resize not updating
		resize = (self.img.winfo_width(), self.img.winfo_height())
		resize_img = img.resize(resize, Image.ANTIALIAS)
		self.img.image = ImageTk.PhotoImage(resize_img)
		self.img.config(image=self.img.image, anchor='center')

	def set_info(self, name):
		path = f'info/{name}'

		if not os.path.isfile(path):
			return self.__insert(f'Information Not Found: {path}')
		
		with open(path, 'r', encoding='utf-8') as f:
			lines = f.read().split('\n')
			text = dict(tuple(line.split(':', 1)) for line in lines[:15])
			text_line = [line.replace('Text:', '', 1) for line in lines[15:]]
			text['Text'] = '\n'.join(text_line)
			self.__insert(self.info_format.format(text))