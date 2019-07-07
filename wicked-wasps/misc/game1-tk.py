from table import GameBoard
from random import choices, shuffle
from characters import Characters as char
from tkinter import Tk, Label, Button, simpledialog
from PIL import Image, ImageTk


positives = ['Impose zero emmisions in urban centres',
             'Convert grazing land to arable farming use',
             'Provide grants for hydoponics',
             'Stricter punishments on illegal logging',
             'Major investment in renewable energy technology']

negatives = ['Continued use of fossil fuels',
             'Cattle production',
             'Increased access to air travel',
             'Reintroduce CFCs',
             'Fund climate change deniers',
             'Abandon environmental treaties',
             'Produce low cost diesel vehicles']


class Game1(GameBoard):
    def initial_setup(self):
        self.enacted = []
        self.discarded = []
        self.cards = choices(negatives, k=7) + choices(positives, k=5)
        shuffle(self.cards)
        self.boss = [player for player in self.players if str(player) == 'Zilla']
        self.boss_removed = False

    def _players(self, members):
        num = len(members)
        acts = num//2+1
        shuffle(members)
        roles = [char.Zilla] + [char.Denier]*(num-acts-1) + [char.Activist]*acts
        shuffle(roles)
        players = []
        for role, player, position in zip(
            roles,
            members, self.seats
        ):
            players.append(role(player, position))
        return players

    def _cards(self):
        pass

    def _start_phase(self):
        self.turn_count += 1
        if self.turn_count % 3 == 0:
            self.voting()

    def voting(self):
        players = [player.name for player in self.players]
        while True:
            if self.root:
                eliminated = simpledialog.askstring(title=f'{self.active}' ,prompt='Who to remove? ')
            else:
                eliminated = input('who to remove?')
            try:
                player = players.index(eliminated)
            except (ValueError, TypeError):
                print('Not an option')
                continue
            break
        self.players[player].eliminated = True

    def _mid_phase(self, amount=3):
        options = []
        for _ in range(amount):
            card = self.cards.pop()
            self.discarded.append(card)
            options.append(card)
        prompt = '\n'.join(options)+'\nEnact 1, 2 or 3: '
        while True:
            try:
                if self.root:
                    enact = int(simpledialog.askstring(title='Executive Order', prompt=prompt))
                else:
                    enact = int(input(prompt))
                if enact not in [1,2,3]:
                    raise ValueError
            except (ValueError, TypeError):
                continue
            break
        self.enacted.append(options[int(enact) - 1])

    def _end_phase(self):
        if len(self.cards) <= 3:
            self.cards += self.discarded
            self.discarded = []
            shuffle(self.cards)
        elimed = [player for player in self.players if player.eliminated
                  and player not in self.eliminated]
        if elimed:
            for player in elimed:
                self.eliminated.append(player)
                self.players.remove(player)
        self.active.is_active = False

    def game_over(self):
        if self.boss[0].eliminated == True:
            self.boss_removed = True
        return sum(1 for item in self.enacted if item in negatives) >= 3 or self.boss[0].eliminated
        # return len(self.players) > 2

class Root(Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.board = Label(self, text='1234')  # can't get label to work...
        self.board.img = ImageTk.PhotoImage(game.next_turn())
        self.board.pack()
        self.board.configure(image=self.board.img)
        btn = Button(self, text='Next Turn', command=self.update_image)
        btn.pack()

    def update_image(self):
        self.board.img = ImageTk.PhotoImage(self.game.next_turn())
        self.board.config(image=self.board.img)
        self.game.run(self)


def main():
    game = Game1(['AXAS', 'AE', 'BTE', 'CJ', 'SHLX', 'SNP', 'CHK'])
    x = Root(game)
    x.mainloop()

if __name__ == '__main__':
    main()
