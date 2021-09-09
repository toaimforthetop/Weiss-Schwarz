import tkinter as tk
import math

class Range(tk.LabelFrame):
	def __init__(self, parent=None, text=''):
		super(Range, self).__init__(parent)
		self.config(relief='groove', bd=2, text=text)

		validate = parent.register(self.__only_numbers)

		self.min = tk.Entry(
			self, validate='key', validatecommand=(validate, '%S'))
		self.min.pack(side='left', anchor='w', expand='yes')

		tk.Label(self, text='-').pack(side='left', anchor='w', expand='yes')

		self.max = tk.Entry(
			self, validate='key', validatecommand=(validate, '%S'))
		self.max.pack(side='left', anchor='w', expand='yes')

		self.max_var = tk.StringVar()
		self.max_var.trace('w', self.__max_check)
		self.max.config(textvariable=self.max_var, justify='center')

		self.min_var = tk.StringVar()
		self.min_var.trace('w', self.__min_check)
		self.min.config(textvariable=self.min_var, justify='center')

	def __min_check(self, *args):
		if not self.min.get():
			return

		if not self.max.get() or int(self.min.get()) >= int(self.max.get()):
			self.max.delete(0, 'end')
			self.max.insert(0, self.min.get())

	def __max_check(self, *args):
		if not self.max.get():
			return

		if not self.min.get() or int(self.min.get()) >= int(self.max.get()):
			self.min.delete(0, 'end')
			self.min.insert(0, self.max.get())

	def __only_numbers(self, char):
		return char.isdigit()

	def range(self):
		r = [self.min.get(), self.max.get()]
		return r if r != ['', ''] else []

class CheckBar(tk.LabelFrame):
	def __init__(self, parent=None, text='', picks=[], row=2):
		super(CheckBar, self).__init__(parent)
		self.vars = {}
		column = math.ceil(len(picks) / row)
		coord = [(x, y) for x in range(row) for y in range(column)]
		for pick, (x, y) in zip(picks, coord):
			var = tk.IntVar()
			chk = tk.Checkbutton(self, text=pick, variable=var)
			if row == 1:
				chk.pack(side='left', anchor='w', expand=True)
			else:
				chk.grid(row=x, column=y, sticky='nsew')
			self.vars[pick] = var
		self.config(relief='groove', bd=2, text=text)

	def state(self):
		return [k for k, v in self.vars.items() if v.get() == 1]

class FilterSearch(tk.Toplevel):
	def __init__(self, *args, cmd=None, **kwargs):
		super(FilterSearch, self).__init__(*args, **kwargs)
		self.title('Filter Search')
		self.resizable(False, False)
		self.__cmd = cmd

		self.rarity = CheckBar(self, 'Rarity', self.__type('rarity'))
		self.rarity.grid(row=0, column=0, sticky='nsew')
		self.level = CheckBar(self, 'Level', [str(i) for i in range(4)], 1)
		self.level.grid(row=1, column=0, sticky='nsew')
		self.side = CheckBar(self, 'Side', ['Weiss', 'Schwarz'], 1)
		self.side.grid(row=2, column=0, sticky='nsew')
		self.option = CheckBar(self, 'Option', ['COUNTER', 'CLOCK'], 1)
		self.option.grid(row=3, column=0, sticky='nsew')
		self.soul = CheckBar(self, 'Soul', [str(i) for i in range(1, 4)], 1)
		self.soul.grid(row=4, column=0, sticky='nsew')

		self.trigger = CheckBar(self, 'Trigger', self.__type('trigger'))
		self.trigger.grid(row=0, column=1, sticky='nsew')
		self.color = CheckBar(self, 'Color', self.__type('color'), 1)
		self.color.grid(row=1, column=1, sticky='nsew')
		self.type = CheckBar(self, 'Type', self.__type('card type'), 1)
		self.type.grid(row=2, column=1, sticky='nsew')
		self.power = Range(self, 'Power')
		self.power.grid(row=3, column=1, sticky='nsew')
		self.cost = CheckBar(self, 'Cost', [str(i) for i in range(5)], 1)
		self.cost.grid(row=4, column=1, sticky='nsew')

		self.ent = tk.Entry(self)
		self.ent.grid(row=5, column=0, columnspan=2, sticky='nsew')

		tk.Button(self, text='Search', command=self.__search).grid(
			row=6, column=0, sticky='e')
		tk.Button(self, text='Cancel', command=lambda: self.destroy()).grid(
			row=6, column=1, sticky='w')

	def __type(self, name):
		path = 'misc/' + name + '.txt'
		with open(path, 'r', encoding='utf-8') as f:
			return f.read().split('\n')[:-1]
	
	def __search(self):
		items = {}
		
		if self.rarity.state(): items['Rarity'] = self.rarity.state()
		if self.level.state(): items['Level'] = self.level.state()
		if self.side.state(): items['Side'] = self.side.state()
		# if self.option.state(): items['Option'] = self.option.state()
		if self.soul.state(): items['Soul'] = self.soul.state()
		if self.trigger.state(): 
			trigger = list(
				map(lambda i: i.replace('None', ''), self.trigger.state()))
			items['Trigger'] = trigger
		if self.color.state(): items['Color'] = self.color.state()
		if self.type.state(): items['Type'] = self.type.state()
		if self.power.range(): items['Power'] = self.power.range()
		if self.cost.state(): items['Cost'] = self.cost.state()

		self.__cmd(self.ent.get(), items)