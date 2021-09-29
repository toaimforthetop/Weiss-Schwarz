import os
import tkinter as tk
from PIL import ImageTk, Image
import locate

class Information(tk.Frame):
	def __init__(self, *args, **kwargs):
		super(Information, self).__init__(*args, **kwargs)

		self.img = tk.Label(self)
		self.img.place(relw=0.94, relh=0.6, relx=0, rely=0)

		self.txtbx = tk.Text(self, state='disable')
		self.txtbx.place(relw=1, relh=0.4, relx=0, rely=0.6)

		with open(locate.FORMAT, 'r', encoding='utf-8') as f:
			self.info_format = f.read()

	def __insert(self, information):
		self.txtbx.config(state='normal')
		self.txtbx.delete('1.0', 'end')
		self.txtbx.insert('end', information)
		self.txtbx.config(state='disable')

	def set_information(self, file_name):
		path = locate.INFOFLD.format(file_name)

		if not os.path.isfile(path):
			return self.__insert(f'Information not found: {path}')

		with open(path, 'r', encoding='utf-8') as f:
			lines = f.read().split('\n')
			text = dict(tuple(line.split(':', 1)) for line in lines[:15])
			text_line = [line.replace('Text:', '', 1) for line in lines[15:]]
			text['Text'] = '\n'.join(text_line)
			self.__insert(self.info_format.format(text))

	def set_image(self, file_name):
		self.img.image = locate.add_image(
			file_name, self.img.winfo_width(), self.img.winfo_height())
		self.img.config(image=self.img.image, anchor='center')

	def display(self, file_name):
		self.set_image(file_name)
		self.set_information('{}.txt'.format(file_name.rsplit('.', 1)[0]))