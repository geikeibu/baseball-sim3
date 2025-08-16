init python:
    import random

    class Player:
        def __init__(self, name, offense, defense, pitching):
            self.name = name
            self.offense = offense
            self.defense = defense
            self.pitching = pitching

    class Team:
        def __init__(self, name):
            self.name = name
            self.players = []
            self.wins = 0
            self.losses = 0
            self.draws = 0

        def add_player(self, player):
            self.players.append(player)

        def get_avg_offense(self):
            if not self.players:
                return 0
            # For simplicity, we'll average offense over all players, including pitchers
            return sum(p.offense for p in self.players) / len(self.players)

        def get_avg_defense(self):
            if not self.players:
                return 0
            return sum(p.defense for p in self.players) / len(self.players)

        def get_avg_pitching(self):
            # A more realistic model would select a starting pitcher, but for now, we average
            pitchers = [p for p in self.players if p.pitching > 0]
            if not pitchers:
                return 0
            return sum(p.pitching for p in pitchers) / len(pitchers)

    # --- Sample Data ---
    # We will define teams and players as persistent objects so their stats (wins/losses) are saved.
    # We use "default" instead of "define" for data that is expected to change.

default persistent.teams = []

init python:
    if not persistent.teams:
        # Create sample teams only if they don't exist in persistent data
        dragons = Team("Dragons")
        dragons.add_player(Player("D-Player1", 80, 70, 10))
        dragons.add_player(Player("D-Player2", 75, 65, 10))
        dragons.add_player(Player("D-Player3", 60, 80, 10))
        dragons.add_player(Player("D-Pitcher1", 30, 50, 85))

        tigers = Team("Tigers")
        tigers.add_player(Player("T-Player1", 85, 60, 10))
        tigers.add_player(Player("T-Player2", 70, 70, 10))
        tigers.add_player(Player("T-Player3", 65, 75, 10))
        tigers.add_player(Player("T-Pitcher1", 40, 60, 80))

        lions = Team("Lions")
        lions.add_player(Player("L-Player1", 90, 55, 10))
        lions.add_player(Player("L-Player2", 72, 68, 10))
        lions.add_player(Player("L-Player3", 68, 72, 10))
        lions.add_player(Player("L-Pitcher1", 35, 55, 88))

        hawks = Team("Hawks")
        hawks.add_player(Player("H-Player1", 88, 65, 10))
        hawks.add_player(Player("H-Player2", 78, 78, 10))
        hawks.add_player(Player("H-Player3", 55, 85, 10))
        hawks.add_player(Player("H-Pitcher1", 25, 65, 90))

        persistent.teams.extend([dragons, tigers, lions, hawks])
