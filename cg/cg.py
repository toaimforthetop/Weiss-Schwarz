import deckeditor
import infobox
from card import Card, OCard
import grabbox
import udp
import tkinter as tk
import random

class Zone(tk.Label):
    def __init(self, *args, **kwargs):
        super(Zone, self).__init__(*args, **kwargs)

    def top(self):
        return self.winfo_x()

    def left(self):
        return self.winfo_y()

    def bottom(self):
        return self.top() + self.winfo_width()

    def right(self):
        return self.left() + self.winfo_height()

    def width(self):
        return self.winfo_width()

    def height(self):
        return self.winfo_height()

    def zone_drop(self, card, rotate=False, angle=0):
        if card.top() < self.top() > card.bottom():
            return

        if card.top() > self.bottom() < card.bottom():
            return

        if card.left() < self.left() > card.right():
            return

        if card.left() > self.right() < card.right():
            return

        x = self.top() / card.master.winfo_width()
        y = self.left() / card.master.winfo_height()
        card.place(relx=x, rely=y)

        if rotate:
            card.angle = angle
            card.rotate(0.07, 0.1)

class Display(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)

        zone = {
        'Memory': self.memory,
        'Deck': self.deck,
        'Waiting Room': self.waitingroom,
        }

        self.zonebtn = [
        tk.Button(self, text=k, command=v)
        for k, v in zone.items()]
        for btn in self.zonebtn:
            btn.pack()

    def setup(self, playerdeck, playerzone, opponentdeck, opponentzone):
        self.pdeck = playerdeck
        self.pzone = playerzone
        self.odeck = opponentdeck
        self.ozone = opponentzone
        self.cards = []

    def memory(self):
        grabbox.GrabBox(self.master)

    def deck(self):
        self.cards.clear()
        self.existinzone(self.pdeck, self.pzone[0])
        temp = grabbox.GrabBox(self.master)
        temp.setup(9, 6)
        temp.display(self.cards, None)

    def waitingroom(self):
        grabbox.GrabBox(self.master)

    def existinzone(self, cards, zone):
        for card in cards:
            if card.top() == zone.top() and card.left() == zone.left():
                self.cards.append(card)

class PlayMat(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(PlayMat, self).__init__(*args, **kwargs)

        self.playerZone()
        self.oppoenentZone()

    def get_pdeck(self, info):
        with open(f'deck/KanColle Deck.txt', 'r', encoding='utf-8') as f:
            self.pdeck = [Card(self, img=(e, img)) 
                for e, img in enumerate(f.read().split('\n'))]

        random.shuffle(self.pdeck)
        for card in self.pdeck:
            card.tkraise()
            card.collision = self.collide_to_zone
            card.place(relw=0.07, relh=0.1, relx=0.665, rely=0.6)
            card.keybind(0.07, 0.1, info)
            card.update_idletasks()
            card.set_img()

        self.odeck = []

    def collide_to_zone(self, card):
        for zone in self.pz[:7]:
            zone.zone_drop(card, True, 180)

        self.pmemory.zone_drop(card, True)
        self.pclimax.zone_drop(card, True)
        self.pstock.zone_drop(card)
        self.plevel.zone_drop(card)
        self.pclock.zone_drop(card)
        self.phand.zone_drop(card)

    def playerZone(self):
        self.pstock = Zone(self, text='Stock', relief='solid', bd=1)
        self.pstock.place(relw=0.098, relh=0.3, relx=0.115, rely=0.5)
        self.pclimax = Zone(self, text='Climax', relief='solid', bd=1)
        self.pclimax.place(relw=0.098, relh=0.071, relx=0.235, rely=0.5)
        self.plevel = Zone(self, text='Level', relief='solid', bd=1)
        self.plevel.place(relw=0.098, relh=0.12, relx=0.235, rely=0.6)
        self.pclock = Zone(self, text='Clock', relief='solid', bd=1)
        self.pclock.place(relw=0.4, relh=0.1, relx=0.235, rely=0.75)
        self.phand = Zone(self, text='Hand', relief='solid', bd=1)
        self.phand.place(relw=0.4, relh=0.1, relx=0.235, rely=0.86)
        self.pmemory = Zone(self, text='Memory', relief='solid', bd=1)
        self.pmemory.place(relw=0.098, relh=0.071, relx=0.665, rely=0.5)

        texts = ['Deck', 'Waiting\nRoom', 'CR', 'CC', 'CL', 'BR', 'BL', 'Memory']
        self.pz = [Zone(self, text=txt, relief='solid', bd=1) for txt in texts]
        self.pz[0].place(relw=0.07, relh=0.1, relx=0.665, rely=0.6)
        self.pz[1].place(relw=0.07, relh=0.1, relx=0.665, rely=0.73)
        self.pz[2].place(relw=0.07, relh=0.1, relx=0.565, rely=0.5)
        self.pz[3].place(relw=0.07, relh=0.1, relx=0.465, rely=0.5)
        self.pz[4].place(relw=0.07, relh=0.1, relx=0.365, rely=0.5)
        self.pz[5].place(relw=0.07, relh=0.1, relx=0.515, rely=0.63)
        self.pz[6].place(relw=0.07, relh=0.1, relx=0.415, rely=0.63)

    def oppoenentZone(self):
        self.ostock = Zone(self, text='Stock', relief='solid', bd=1)
        self.ostock.place(relw=0.098, relh=0.3, relx=0.785, rely=0.19)
        self.oclimax = Zone(self, text='Climax', relief='solid', bd=1)
        self.oclimax.place(relw=0.098, relh=0.071, relx=0.665, rely=0.42)
        self.olevel = Zone(self, text='Level', relief='solid', bd=1)
        self.olevel.place(relw=0.098, relh=0.12, relx=0.665, rely=0.27)
        self.oclock = Zone(self, text='Clock', relief='solid', bd=1)
        self.oclock.place(relw=0.4, relh=0.1, relx=0.365, rely=0.14)
        self.ohand = Zone(self, text='Hand', relief='solid', bd=1)
        self.ohand.place(relw=0.4, relh=0.1, relx=0.365, rely=0.03)
        self.omemory = Zone(self, text='Memory', relief='solid', bd=1)
        self.omemory.place(relw=0.098, relh=0.071, relx=0.235, rely=0.42)

        texts = ['Deck', 'Waiting\nRoom', 'CL', 'CC', 'CR', 'BL', 'BR', 'Memory']
        self.oz = [Zone(self, text=txt, relief='solid', bd=1) for txt in texts]
        self.oz[0].place(relw=0.07, relh=0.1, relx=0.265, rely=0.29)
        self.oz[1].place(relw=0.07, relh=0.1, relx=0.265, rely=0.16)
        self.oz[2].place(relw=0.07, relh=0.1, relx=0.565, rely=0.39)
        self.oz[3].place(relw=0.07, relh=0.1, relx=0.465, rely=0.39)
        self.oz[4].place(relw=0.07, relh=0.1, relx=0.365, rely=0.39)
        self.oz[5].place(relw=0.07, relh=0.1, relx=0.515, rely=0.26)
        self.oz[6].place(relw=0.07, relh=0.1, relx=0.415, rely=0.26)

class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.geometry('1300x900')

        self.infobox = infobox.InfoBox(self)
        self.infobox.place(relw=0.3, relh=0.97, relx=0, rely=0)

        self.btn = tk.Button(self, text='play', command=self.play)
        self.btn.place(relw=0.06, relh=0.03, relx=0, rely=0.97)

    def play(self):
        self.playmat = PlayMat(self)
        self.playmat.place(relw=0.7, relh=1, relx=0.3, rely=0)
        self.playmat.get_pdeck(self.infobox.display)

        self.bind('<q>', self.displayzone)
        self.btn.place_forget()

    def displayzone(self, event):
        temp = Display(self)
        temp.setup(
            self.playmat.pdeck, self.playmat.pz, 
            self.playmat.odeck, self.playmat.oz)

if __name__ == '__main__':
    main = Window()
    main.mainloop()