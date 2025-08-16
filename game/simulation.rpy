init python:
    import random

    def simulate_game(team1, team2):
        """
        Simulates a single game between two teams based on their stats.
        Updates their win/loss records and returns a result string.
        """
        # Get the average stats for both teams from our definitions.
        team1_offense = team1.get_avg_offense()
        team1_pitching = team1.get_avg_pitching()

        team2_offense = team2.get_avg_offense()
        team2_pitching = team2.get_avg_pitching()

        # The core of the simulation.
        # We calculate a "base score potential" based on the difference between
        # one team's offense and the other's pitching.
        # A higher difference means a higher chance of scoring.
        team1_score_potential = (team1_offense - team2_pitching) / 7.0
        team2_score_potential = (team2_offense - team1_pitching) / 7.0

        # We add a random factor to make the games unpredictable.
        # random.uniform gives us a floating point number.
        # max(0, ...) ensures we don't end up with negative scores.
        team1_score = int(max(0, team1_score_potential + random.uniform(-3, 4)))
        team2_score = int(max(0, team2_score_potential + random.uniform(-3, 4)))

        # Update the persistent team objects with the new stats.
        if team1_score > team2_score:
            team1.wins += 1
            team2.losses += 1
        elif team2_score > team1_score:
            team2.wins += 1
            team1.losses += 1
        else:
            team1.draws += 1
            team2.draws += 1

        # Return a formatted string for easy display in Ren'Py.
        result_str = "{} {} - {} {}".format(team1.name, team1_score, team2_score, team2.name)
        return result_str
