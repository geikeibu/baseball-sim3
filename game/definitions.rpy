init python:
    import random

    def _calculate_salary(overall):
        """
        Calculates a player's salary based on their overall rating.
        Salary is in 万円.
        """
        if overall < 50:
            base_salary = 400
        else:
            # Exponential growth for higher overall ratings
            base_salary = 400 + int(((overall - 50) / 10.0) ** 2.5 * 150)

        # Add some randomness
        random_factor = random.uniform(0.9, 1.1)
        salary = int(base_salary * random_factor)

        # Round to nearest 10万円 for cleaner numbers, with a minimum of 400.
        return max(400, round(salary / 10) * 10)

    # Base class for all players, containing a name.
    class Player(object):
        def __init__(self, name, age, contract_years=3, salary=5000):
            self.name = name
            self.age = age
            self.contract_years = contract_years
            self.salary = salary # In 万円, e.g., 5000万円

    # A class for fielders (position players) inheriting from Player.
    class Fielder(Player):
        def __init__(self, name, age, meet, power, run, defense, throwing, contract_years=3, salary=0):
            super(Fielder, self).__init__(name, age, contract_years, salary)
            self.position = "Fielder"
            self.meet = meet
            self.power = power
            self.run = run
            self.defense = defense
            self.throwing = throwing

            # If no salary is provided, calculate it based on overall stats.
            if salary == 0:
                self.salary = _calculate_salary(self.overall)

            # Batting stats
            self.at_bats = 0
            self.hits = 0
            self.home_runs = 0
            self.rbis = 0
            self.walks = 0

        @property
        def overall(self):
            # Weighted average of stats
            return int((self.meet * 0.25) + (self.power * 0.3) + (self.run * 0.15) + (self.defense * 0.2) + (self.throwing * 0.1))

        @property
        def batting_avg(self):
            if self.at_bats == 0:
                return 0.0
            return float(self.hits) / self.at_bats

    # A class for pitchers, also inheriting from Player.
    class Pitcher(Player):
        def __init__(self, name, age, speed, control, stamina, breaking_balls, contract_years=3, salary=0):
            super(Pitcher, self).__init__(name, age, contract_years, salary)
            self.position = "Pitcher"
            self.speed = speed
            self.control = control
            self.stamina = stamina
            self.breaking_balls = breaking_balls

            # If no salary is provided, calculate it based on overall stats.
            if salary == 0:
                self.salary = _calculate_salary(self.overall)

            # Add a fatigue attribute, 0 is fully rested, 100 is max fatigue.
            self.fatigue = 0
            # Pitching stats
            self.wins = 0
            self.losses = 0
            self.outs_recorded = 0
            self.earned_runs = 0
            self.strikeouts = 0
            self.walks_issued = 0

        @property
        def overall(self):
            # Weighted average of stats
            breaking_ball_rating = sum(self.breaking_balls.values()) * 3
            return int((self.speed * 0.1) + (self.control * 0.4) + (self.stamina * 0.2) + breaking_ball_rating)

        @property
        def era(self):
            if self.outs_recorded == 0:
                return 0.0
            return (float(self.earned_runs) * 27) / self.outs_recorded # 27 outs = 9 innings

        @property
        def innings_pitched(self):
            return float(self.outs_recorded) / 3.0

    # The Team class now manages the new player types and rotation.
    class Team:
        def __init__(self, name, initial_funds=100000):
            self.name = name
            self.players = []
            self.wins = 0
            self.losses = 0
            self.draws = 0
            # Add a rotation index to track which starter is next.
            self.rotation_index = 0

            # Financials
            self.funds = initial_funds # 資金 (in 万円, e.g. 100000 is 10億円)
            self.fans = 500000 # 観客動員数 (人)

            # --- Team Identity ---
            # 'balanced', 'power', 'speed', 'defense'
            self.philosophy = "balanced"
            self.coach = None

        def add_player(self, player):
            self.players.append(player)

        def get_pitchers(self):
            return [p for p in self.players if isinstance(p, Pitcher)]

        def get_fielders(self):
            return [p for p in self.players if isinstance(p, Fielder)]

        def get_starting_pitcher(self):
            """
            Selects a starting pitcher based on a rotation and fatigue.
            A pitcher is considered "rested" if their fatigue is below 40.
            """
            # For this simulation, we'll define the first 2 pitchers added as the "starting rotation".
            starters = [p for p in self.get_pitchers()][:2]
            if not starters:
                return None

            num_starters = len(starters)

            # Check the rotation up to two full cycles to find a rested pitcher.
            for _ in range(num_starters * 2):
                pitcher_to_check = starters[self.rotation_index]

                if pitcher_to_check.fatigue < 40:
                    # We found a rested pitcher. Select them.
                    self.rotation_index = (self.rotation_index + 1) % num_starters
                    return pitcher_to_check

                # This pitcher is fatigued, advance the index and check the next one.
                self.rotation_index = (self.rotation_index + 1) % num_starters

            # If no pitcher is rested after checking everyone twice,
            # we make an "emergency start" with the least fatigued pitcher.
            least_fatigued_pitcher = min(starters, key=lambda p: p.fatigue)
            # We still advance the rotation index to not get stuck on one tired pitcher.
            self.rotation_index = (starters.index(least_fatigued_pitcher) + 1) % num_starters
            return least_fatigued_pitcher

        def get_offense_rating(self):
            fielders = self.get_fielders()
            if not fielders:
                return 0
            avg_meet = sum(f.meet for f in fielders) / len(fielders)
            avg_power = sum(f.power for f in fielders) / len(fielders)
            return (avg_meet * 0.6) + (avg_power * 0.4)

        def get_defense_rating(self):
            fielders = self.get_fielders()
            if not fielders:
                return 0
            avg_defense = sum(f.defense for f in fielders) / len(fielders)
            avg_throwing = sum(f.throwing for f in fielders) / len(fielders)
            return (avg_defense * 0.7) + (avg_throwing * 0.3)

    def calculate_trade_value(player):
        """
        Calculates a player's trade value based on overall, age, and contract.
        """
        # Age modifier: younger players are more valuable
        if player.age < 25:
            age_modifier = 1.2
        elif player.age < 30:
            age_modifier = 1.0
        elif player.age < 35:
            age_modifier = 0.8
        else:
            age_modifier = 0.6

        # Contract modifier: longer contracts are slightly more valuable
        contract_modifier = 1.0 + (player.contract_years * 0.05)

        # Salary modifier: lower salary is more valuable
        salary_modifier = 1.0 + ((8000 - player.salary) / 10000.0)

        value = player.overall * age_modifier * contract_modifier * salary_modifier
        return int(value)


# --- Data Initialization ---
default persistent.teams = []

init python:
    if not persistent.teams:
        # --- Create Dragons ---
        dragons = Team("Dragons")
        dragons.add_player(Fielder(name="D-Fielder1", age=random.randint(20, 38), meet=70, power=65, run=75, defense=80, throwing=70, contract_years=random.randint(1, 5)))
        dragons.add_player(Fielder(name="D-Fielder2", age=random.randint(20, 38), meet=65, power=75, run=60, defense=70, throwing=85, contract_years=random.randint(1, 5)))
        dragons.add_player(Fielder(name="D-Fielder3", age=random.randint(20, 38), meet=80, power=50, run=85, defense=65, throwing=60, contract_years=random.randint(1, 5)))
        dragons.add_player(Pitcher(name="D-Pitcher1", age=random.randint(20, 38), speed=150, control=80, stamina=85, breaking_balls={'slider': 4, 'curve': 3}, contract_years=random.randint(1, 5)))
        dragons.add_player(Pitcher(name="D-Pitcher2", age=random.randint(20, 38), speed=145, control=85, stamina=70, breaking_balls={'fork': 5}, contract_years=random.randint(1, 5)))

        # --- Create Tigers ---
        tigers = Team("Tigers")
        tigers.add_player(Fielder(name="T-Fielder1", age=random.randint(20, 38), meet=85, power=80, run=65, defense=60, throwing=65, contract_years=random.randint(1, 5)))
        tigers.add_player(Fielder(name="T-Fielder2", age=random.randint(20, 38), meet=75, power=70, run=70, defense=75, throwing=70, contract_years=random.randint(1, 5)))
        tigers.add_player(Fielder(name="T-Fielder3", age=random.randint(20, 38), meet=60, power=90, run=55, defense=50, throwing=60, contract_years=random.randint(1, 5)))
        tigers.add_player(Pitcher(name="T-Pitcher1", age=random.randint(20, 38), speed=155, control=70, stamina=90, breaking_balls={'cutter': 3, 'changeup': 4}, contract_years=random.randint(1, 5)))
        tigers.add_player(Pitcher(name="T-Pitcher2", age=random.randint(20, 38), speed=140, control=90, stamina=65, breaking_balls={'screwball': 4}, contract_years=random.randint(1, 5)))

        # --- Create Lions ---
        lions = Team("Lions")
        lions.add_player(Fielder(name="L-Fielder1", age=random.randint(20, 38), meet=75, power=88, run=70, defense=65, throwing=70, contract_years=random.randint(1, 5)))
        lions.add_player(Fielder(name="L-Fielder2", age=random.randint(20, 38), meet=82, power=75, run=75, defense=70, throwing=75, contract_years=random.randint(1, 5)))
        lions.add_player(Fielder(name="L-Fielder3", age=random.randint(20, 38), meet=68, power=80, run=80, defense=80, throwing=80, contract_years=random.randint(1, 5)))
        lions.add_player(Pitcher(name="L-Pitcher1", age=random.randint(20, 38), speed=152, control=75, stamina=88, breaking_balls={'sinker': 5, 'slider': 2}, contract_years=random.randint(1, 5)))
        lions.add_player(Pitcher(name="L-Pitcher2", age=random.randint(20, 38), speed=148, control=82, stamina=72, breaking_balls={'circlechange': 4}, contract_years=random.randint(1, 5)))

        # --- Create Hawks ---
        hawks = Team("Hawks")
        hawks.add_player(Fielder(name="H-Fielder1", age=random.randint(20, 38), meet=88, power=78, run=82, defense=85, throwing=80, contract_years=random.randint(1, 5)))
        hawks.add_player(Fielder(name="H-Fielder2", age=random.randint(20, 38), meet=79, power=82, run=78, defense=75, throwing=88, contract_years=random.randint(1, 5)))
        hawks.add_player(Fielder(name="H-Fielder3", age=random.randint(20, 38), meet=72, power=75, run=90, defense=90, throwing=75, contract_years=random.randint(1, 5)))
        hawks.add_player(Pitcher(name="H-Pitcher1", age=random.randint(20, 38), speed=160, control=85, stamina=92, breaking_balls={'splitter': 6, 'curve': 3}, contract_years=random.randint(1, 5)))
        hawks.add_player(Pitcher(name="H-Pitcher2", age=random.randint(20, 38), speed=142, control=88, stamina=75, breaking_balls={'shuuto': 4}, contract_years=random.randint(1, 5)))

        persistent.teams.extend([dragons, tigers, lions, hawks])

    if not hasattr(persistent, 'game_history'):
        persistent.game_history = []

    if not hasattr(persistent, 'current_year'):
        persistent.current_year = 2024

    # MVP: Add difficulty settings
    if not hasattr(persistent, 'hit_level'):
        persistent.hit_level = 0.25 # 打低/打高
    if not hasattr(persistent, 'stat_influence'):
        persistent.stat_influence = 1.0 # 乱数振れ幅
