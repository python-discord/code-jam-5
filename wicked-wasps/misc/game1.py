from table import GameBoard
from random import choices, shuffle
from characters import Characters as char

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

    def cards(self):
        pass

    def _start_phase(self):
        self.turn_count += 1
        if self.turn_count % 3 == 0:
            self.voting()

    def voting(self):
        players = [player.name for player in self.players]
        while True:
            eliminated = input('who to remove?')
            try:
                player = players.index(eliminated)
            except ValueError:
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
        print('\n'.join(options))
        while True:
            try:
                enact = int(input('Enact 1, 2 or 3: '))
                if enact not in [1, 2, 3]:
                    raise ValueError
            except ValueError:
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
        if self.boss[0].eliminated:
            self.boss_removed = True
        return sum(1 for item in self.enacted if item in negatives) >= 3 or self.boss[0].eliminated
        # return len(self.players) > 2


x = Game1(['AXAS', 'AE', 'BTE', 'CJ', 'SHLX', 'SNP', 'CHK'])

while not x.game_over():
    x.next_turn().show()
    print(f'{x.active.name}, role: {str(x.active).title()}')
    x.run()

if x.boss_removed:
    print(f'halting of {x.boss[0]} {x.boss[0].name} was successful')
else:
    print('unsuccessful')
