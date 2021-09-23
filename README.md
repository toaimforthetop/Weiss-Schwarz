# Weiss Schwarz
Originally it was just made as a quick project to play the card game, weiss schwarz with a friend, due to some other programs either not having all the cards or required money to play on it. It lead me to creating this project. It was suppose to be able to switch between different type of card games but I just stop after a while and never got back to it and try to fix everything.

 Issues:
  - The bulk of the issues comes from you selecting x amount of cards and doing some other tasks which sometimes causes the cards that you selected to either expand or make duplicates.
  - When you select x amount of cards and try to click HOST?JOIN, the cards will move to the button.
  - Closing the HOST/JOIN window will cause error when you tried to reopen it.
   - You will need to reopent the whole program again
  - Sometimes when you select x amount of cards and you click away from it, it will move x amount of cards to clicked area.
   - Only way to solve this issue is to just close it and open it again
  - The other issue was that it was built under python tkinter but it was due to creating a workable program to just play the game with a friend within a short amount of time that I didn't think much of it.
  - Never wrote any documentation for the project or comments for the codes so that is going to be interesting.
  - The Host/Join button require you to open a port in your gateway in order to play with someone else, thus also lead to them knowing your IP Address.
   - Leave the port to 0.0.0.0 if you are hosting (It could be 127.0.0.1 but i dont remember).
   - If you or the other player leave, you will not know that person left.
  - Filter does not work in DECK EDITOR (or at least I never completed it).
  - From what I recalled, DECK EDITOR should be the only thing that should work without a problem but who knows.
  
  Card information was obtain from Weiss Schwarz Official Website and Images from TCG Player.
   - Will I get in trouble for this, probably but eh, when that day happens, happens.
   - I automated collecting card information from the website so when you see information of the card not what it suppose to be, now you know.
    - You can fix this problem by going into info folder, search the card by the card no. and change it there.
   - Some cards do not have card information (could be the other way around -> no image for the card info)
    - You can solve this by just adding the Card Image or Card Information or Both, just make sure to name them with by thier card no. along with its rarity.
     - Examples:
      - AB_W31-E001R.txt (text file) AB_W31-E001R.jpg (image file)
      - AB_W31-E001.txt (text file)  AB_W31-E001.jpg (image file)
      - if the examples is not enough, you can compare both file name in pic folder and info folder
  
  Keys:
   - For set amount of cards selected:
     - w: Pop a window out for you to select a card.
      - Right Click: It will move selected card to left bottom size of your screen.
       - If i recall it will be faced the same as the main window card.
       - Everything will be displayed in ordered like in Deck Editor, do i know why, nope.
     - Left Click: It will just show information of selected card on main window.
    - s: Shuffle x amount of cards you selected.
   - For Single Cards Only (If i recall it should work the same for set amount of cards you selected but I'm not sure):
     - r: Rotate Card
     - t: Show Card to player (Opponent Only)
     - f: Flip Card to player (Owner Only)
     - e: Flip & Show card to both players (Owner & Opponent).
   - For Deck Editor:
     - Both side LEFT CLICK, it should just display information on far left.
     - Left side when you press RIGHT CLICK, it will remove card from deck.
     - Right side when you press RIGHT CLICK, it will add card to deck.
