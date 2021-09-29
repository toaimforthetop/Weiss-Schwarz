from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno
from PIL import ImageTk, Image

def folder_format(location, folder):
	return '{}/'.format(location) + '{}/'.format(folder) + '{}'

def location(count=0):
	with open('misc/location.txt', 'r', encoding='utf-8') as f:
		return f.readline().replace('\n', '')

def save(file_name, text):
	with open(DECKFLD.format(file_name), 'w', encoding='utf-8') as f:
		f.write(text)

def delete(file_name):
	if not askyesno(
		'Confirmation', f'Are you sure you want to delete {file_name}?'):
		return False # if cancel or close

	os.remove(DECKFLD.format(file_name))
	return True

def save_as(text):
	name_for_file = askstring('Save As', 'Name of Deck')
	if not name_for_file: return False # if cancel or close

	while f'{name_for_file}.txt' in os.listdir(f'{location()}/{DECKS}'):
		name_for_file += '_'

	file_name = f'{name_for_file}.txt'
	with open(DECKFLD.format(file_name), 'x', encoding='utf-8') as f:
		f.write(text)

	return True

def load_init_deck():
	with open(LOADDECK, 'r', encoding='utf-8') as f:
		return f.read()

def update_init_load(text):
	with open(LOADDECK, 'w', encoding='utf-8') as f:
		f.write(text)

def grab_deck(file_name):
	with open(DECKFLD.format(file_name), 'r', encoding='utf-8') as f:
		return f.read().split('\n')

def add_image(file_name, width, height, angle=0):
	try: img = Image.open(PICFLD.format(file_name))
	except: img = Image.open(PICFLD.format(BACKIMG))
	rotate_img = img.rotate(angle, expand=True)
	resize_img = rotate_img.resize((width, height), Image.ANTIALIAS)
	return ImageTk.PhotoImage(resize_img)

INFO = 'info'
PIC = 'pic'
DECKS = 'decks'
INFOFLD = folder_format(location(), INFO)
PICFLD = folder_format(location(), PIC)
DECKFLD = folder_format(location(), DECKS)
FORMAT = f'{location()}/format.txt'
LOADDECK = f'{location()}/load.txt'
BACKIMG = '1.png'
SHOW = 'red'
HIDDEN = 'grey'