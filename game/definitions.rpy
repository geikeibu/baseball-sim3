init python:
    import random

    # Base class for all players, containing a name.
    class Player(object):
        def __init__(self, name):
            self.name = name

    # A class for fielders (position players) inheriting from Player.
    class Fielder(Player):
        def __init__(self, name, meet, power, run, defense, throwing):
            super(Fielder, self).__init__(name)
            self.position = "Fielder"
            # Pawapuro-style stats. Using a 1-100 scale for simplicity.
            self.meet = meet       # ミート (contact hitting)
            self.power = power     # パワー (power hitting)
            self.run = run         # 走力 (running speed)
            self.defense = defense   # 守備力 (fielding ability)
            self.throwing = throwing # 肩力 (throwing strength)

    # A class for pitchers, also inheriting from Player.
    class Pitcher(Player):
        def __init__(self, name, speed, control, stamina, breaking_balls):
            super(Pitcher, self).__init__(name)
            self.position = "Pitcher"
            self.speed = speed             # 球速 (max fastball velocity)
            self.control = control         # コントロール (pitching control)
            self.stamina = stamina         # スタミナ (pitching stamina)
            # breaking_balls is a dictionary, e.g., {'slider': 4, 'fork': 2}
            # The key is the pitch name, the value is its effectiveness/break.
            self.breaking_balls = breaking_balls

    # The Team class now manages the new player types.
    class Team:
        def __init__(self, name):
            self.name = name
            self.players = []
            self.wins = 0
            self.losses = 0
            self.draws = 0

        def add_player(self, player):
            self.players.append(player)

        def get_pitchers(self):
            """Returns a list of all pitchers on the team."""
            return [p for p in self.players if isinstance(p, Pitcher)]

        def get_fielders(self):
            """Returns a list of all fielders on the team."""
            return [p for p in self.players if isinstance(p, Fielder)]

        def get_starting_pitcher(self):
            """Selects a starting pitcher for a game."""
            pitchers = self.get_pitchers()
            if not pitchers:
                return None
            # A real game would have a rotation. For now, we'll pick the one with the highest stamina.
            # This is a good candidate for future improvement (e.g., tracking pitcher fatigue).
            return max(pitchers, key=lambda p: p.stamina)

        def get_offense_rating(self):
            """Calculates a general team offense rating based on fielder stats."""
            fielders = self.get_fielders()
            if not fielders:
                return 0
            # A weighted average of the team's contact and power hitting.
            avg_meet = sum(f.meet for f in fielders) / len(fielders)
            avg_power = sum(f.power for f in fielders) / len(fielders)
            return (avg_meet * 0.6) + (avg_power * 0.4)

        def get_defense_rating(self):
            """Calculates a general team defense rating based on fielder stats."""
            fielders = self.get_fielders()
            if not fielders:
                return 0
            # A weighted average of the team's fielding and throwing ability.
            avg_defense = sum(f.defense for f in fielders) / len(fielders)
            avg_throwing = sum(f.throwing for f in fielders) / len(fielders)
            return (avg_defense * 0.7) + (avg_throwing * 0.3)

# --- Data Initialization ---
# We will re-populate this with new players in the next step.
default persistent.teams = []

init python:
    # This block populates the game with sample teams and players if no persistent data exists.
    if not persistent.teams:
        # --- Create Dragons ---
        dragons = Team("Dragons")
        dragons.add_player(Fielder(name="D-Fielder1", meet=70, power=65, run=75, defense=80, throwing=70))
        dragons.add_player(Fielder(name="D-Fielder2", meet=65, power=75, run=60, defense=70, throwing=85))
        dragons.add_player(Fielder(name="D-Fielder3", meet=80, power=50, run=85, defense=65, throwing=60))
        dragons.add_player(Pitcher(name="D-Pitcher1", speed=150, control=80, stamina=85, breaking_balls={'slider': 4, 'curve': 3}))
        dragons.add_player(Pitcher(name="D-Pitcher2", speed=145, control=85, stamina=70, breaking_balls={'fork': 5}))

        # --- Create Tigers ---
        tigers = Team("Tigers")
        tigers.add_player(Fielder(name="T-Fielder1", meet=85, power=80, run=65, defense=60, throwing=65))
        tigers.add_player(Fielder(name="T-Fielder2", meet=75, power=70, run=70, defense=75, throwing=70))
        tigers.add_player(Fielder(name="T-Fielder3", meet=60, power=90, run=55, defense=50, throwing=60))
        tigers.add_player(Pitcher(name="T-Pitcher1", speed=155, control=70, stamina=90, breaking_balls={'cutter': 3, 'changeup': 4}))
        tigers.add_player(Pitcher(name="T-Pitcher2", speed=140, control=90, stamina=65, breaking_balls={'screwball': 4}))

        # --- Create Lions ---
        lions = Team("Lions")
        lions.add_player(Fielder(name="L-Fielder1", meet=75, power=88, run=70, defense=65, throwing=70))
        lions.add_player(Fielder(name="L-Fielder2", meet=82, power=75, run=75, defense=70, throwing=75))
        lions.add_player(Fielder(name="L-Fielder3", meet=68, power=80, run=80, defense=80, throwing=80))
        lions.add_player(Pitcher(name="L-Pitcher1", speed=152, control=75, stamina=88, breaking_balls={'sinker': 5, 'slider': 2}))
        lions.add_player(Pitcher(name="L-Pitcher2", speed=148, control=82, stamina=72, breaking_balls={'circlechange': 4}))

        # --- Create Hawks ---
        hawks = Team("Hawks")
        hawks.add_player(Fielder(name="H-Fielder1", meet=88, power=78, run=82, defense=85, throwing=80))
        hawks.add_player(Fielder(name="H-Fielder2", meet=79, power=82, run=78, defense=75, throwing=88))
        hawks.add_player(Fielder(name="H-Fielder3", meet=72, power=75, run=90, defense=90, throwing=75))
        hawks.add_player(Pitcher(name="H-Pitcher1", speed=160, control=85, stamina=92, breaking_balls={'splitter': 6, 'curve': 3}))
        hawks.add_player(Pitcher(name="H-Pitcher2", speed=142, control=88, stamina=75, breaking_balls={'shuuto': 4}))

        persistent.teams.extend([dragons, tigers, lions, hawks])
