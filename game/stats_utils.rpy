init python:
    import collections
    import random

    def get_all_players(teams):
        """Extracts all players from all teams."""
        all_players = []
        for team in teams:
            all_players.extend(team.players)
        return all_players

    def get_standings(teams):
        """
        Calculates team standings, including win percentage and games behind.
        """
        # Sort teams by win percentage (wins / (wins + losses))
        # Handle division by zero if a team has not played any games.
        def win_pct(team):
            if team.wins + team.losses == 0:
                return 0.0
            return float(team.wins) / (team.wins + team.losses)

        sorted_teams = sorted(teams, key=win_pct, reverse=True)

        standings = []
        if not sorted_teams:
            return standings

        leader_wins = sorted_teams[0].wins
        leader_losses = sorted_teams[0].losses

        for team in sorted_teams:
            # Games behind formula: ((leader_wins - team_wins) + (team_losses - leader_losses)) / 2
            games_behind = ((leader_wins - team.wins) + (team.losses - leader_losses)) / 2.0
            standings.append({
                "name": team.name,
                "wins": team.wins,
                "losses": team.losses,
                "draws": team.draws,
                "win_pct": win_pct(team),
                "games_behind": games_behind
            })
        return standings

    def get_league_leaders(teams, stat, num_leaders=3):
        """
        Gets the top players in a specific statistical category.
        """
        all_players = get_all_players(teams)

        # Filter for players who are eligible for the stat
        if stat in ["era", "wins", "losses", "strikeouts"]: # Pitching stats
            eligible_players = [p for p in all_players if isinstance(p, Pitcher)]
            # For ERA, require a minimum number of innings pitched
            if stat == "era":
                eligible_players = [p for p in eligible_players if p.innings_pitched >= 1.0]

        else: # Batting stats
            eligible_players = [p for p in all_players if isinstance(p, Fielder)]
            # For batting average, require a minimum number of at-bats
            if stat == "batting_avg":
                eligible_players = [p for p in eligible_players if p.at_bats >= 10]


        # Sort players by the stat.
        # For ERA, lower is better. For all others, higher is better.
        reverse_order = stat != "era"
        sorted_players = sorted(eligible_players, key=lambda p: getattr(p, stat), reverse=reverse_order)

        leaders = []
        for player in sorted_players[:num_leaders]:
            leaders.append({
                "name": player.name,
                "team": next((t.name for t in teams if player in t.players), ""),
                "stat_value": getattr(player, stat),
                "age": player.age
            })
        return leaders

    def process_offseason_changes(teams):
        """
        Simulates the off-season: ages up players, handles contracts and retirements,
        applies stat changes, and increments the game year.
        """
        retired_players = collections.defaultdict(list)

        for team in teams:
            players_to_keep = []
            for player in team.players:
                # 1. Age the player
                player.age += 1
                player.contract_years -= 1

                # 2. Retirement Logic
                # Players over 38 with 0 contract years have a high chance of retiring.
                if player.age > 38 and player.contract_years <= 0:
                    if random.random() < 0.75: # 75% chance to retire
                        retired_players[team.name].append(player.name)
                        continue # Player retires, skip to next player

                # 3. Contract Renewal for players with expired contracts
                if player.contract_years <= 0:
                    player.contract_years = random.randint(1, 4) # Assign new contract
                    # Adjust salary based on performance/age
                    player.salary = max(500, player.salary + random.randint(-1000, 2000))


                # 4. Stat changes based on age
                change = 0
                if player.age <= 27: # Growth phase
                    change = random.randint(1, 3)
                elif player.age >= 34: # Decline phase
                    change = random.randint(-3, -1)

                if change != 0:
                    MIN_STAT = 10
                    MAX_STAT = 99
                    if isinstance(player, Fielder):
                        player.meet = max(MIN_STAT, min(MAX_STAT, player.meet + change))
                        player.power = max(MIN_STAT, min(MAX_STAT, player.power + change))
                        player.run = max(MIN_STAT, min(MAX_STAT, player.run + change))
                        player.defense = max(MIN_STAT, min(MAX_STAT, player.defense + change))
                        player.throwing = max(MIN_STAT, min(MAX_STAT, player.throwing + change))
                    elif isinstance(player, Pitcher):
                        player.speed = max(MIN_STAT, min(MAX_STAT, player.speed + change))
                        player.control = max(MIN_STAT, min(MAX_STAT, player.control + change))
                        player.stamina = max(MIN_STAT, min(MAX_STAT, player.stamina + change))

                players_to_keep.append(player)

            # Update the team's player list
            team.players = players_to_keep


        # 5. Increment the year
        persistent.current_year += 1

        # Store retired players list for potential display later
        persistent.retired_players_log = retired_players
