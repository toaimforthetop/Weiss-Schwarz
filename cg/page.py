import tkinter as tk

class Page(tk.Frame):
	def __init__(self, *args, cmd=lambda *args: None, **kwargs):
		super(Page, self).__init__(*args, **kwargs)
		self.__cmd = cmd

		self.prev = tk.Button(self, text='<', command=self.__prev)
		self.prev.place(relw=0.1, relh=1, relx=0.2, rely=0)

		validate = self.master.register(self.__only_numbers)
		self.page_no = 1
		self.cur_pg = tk.Entry(self, justify='center')
		self.cur_pg.config(validate='key', validatecommand=(validate, '%S'))
		self.cur_pg.place(relw=0.2, relh=1, relx=0.3, rely=0)
		self.__insert(self.page_no)
		self.cur_pg.bind('<Return>', lambda e: self.__load())

		self.max_pg = tk.Label(self, font=('Monospace', 15), anchor='w')
		self.max_pg.place(relw=0.2, relh=1, relx=0.5, rely=0)

		self.next = tk.Button(self, text='>', command=self.__next)
		self.next.place(relw=0.1, relh=1, relx=0.7, rely=0)

	def __only_numbers(self, char):
		return char.isdigit()

	def __state(self):
		func = lambda l, r: 'disable' if l >= r else 'normal'
		self.prev['state'] = func(1, self.page_no)
		self.next['state'] = func(self.page_no, self.max())

	def __load(self):
		if self.cur_pg.get() and 1 <= int(self.cur_pg.get()) <= self.max():
			self.page_no = int(self.cur_pg.get())
			self.__state()
			self.__cmd(self.page_no)
		else:
			self.__insert(self.page_no)

	def __prev(self):
		self.page_no -= 1
		self.__state()
		self.__insert(self.page_no)
		self.__cmd(self.page_no)

	def __next(self):
		self.page_no += 1
		self.__state()
		self.__insert(self.page_no)
		self.__cmd(self.page_no)

	def __insert(self, page_no):
		self.cur_pg.delete(0, 'end')
		self.cur_pg.insert(0, page_no)

	def set_max(self, max_page):
		self.max_pg['text'] = f'/{max_page}'
		self.__state()

	def max(self):
		return int(self.max_pg['text'].replace('/', '', 1))

	def page(self, page_no=1):
		self.page_no = page_no
		self.__insert(self.page_no)