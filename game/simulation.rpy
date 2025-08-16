init python:
    import random

    def _get_pitcher_rating(pitcher):
        """
        Calculates an overall rating for a single pitcher based on their detailed stats.
        This helper function is not intended to be called from outside this file.
        """
        if not pitcher:
            # Return a low rating if for some reason a team has no pitcher.
            return 20

        # The pitcher's overall effectiveness is a weighted average of their key stats.
        # The value of breaking balls is estimated by summing their effectiveness levels and multiplying by a factor.
        breaking_ball_rating = sum(pitcher.breaking_balls.values()) * 4

        # A weighted formula to combine the different pitching attributes.
        # Control is weighted most heavily, as it's crucial for preventing runs.
        pitcher_rating = (pitcher.speed * 0.15) + (pitcher.control * 0.4) + (pitcher.stamina * 0.2) + breaking_ball_rating
        return pitcher_rating

    def simulate_game(home_team, away_team):
        """
        Simulates a single game between two teams using the new detailed player stats.
        This function replaces the older, simpler simulation.
        """
        # === 1. Pre-game Setup: Get team and player ratings ===

        # Each team selects its starting pitcher for the game.
        home_pitcher = home_team.get_starting_pitcher()
        away_pitcher = away_team.get_starting_pitcher()

        # Get the overall offensive and defensive ratings for each team.
        home_offense = home_team.get_offense_rating()
        home_defense = home_team.get_defense_rating()

        away_offense = away_team.get_offense_rating()
        away_defense = away_team.get_defense_rating()

        # Calculate the overall rating for the starting pitchers.
        home_pitcher_rating = _get_pitcher_rating(home_pitcher)
        away_pitcher_rating = _get_pitcher_rating(away_pitcher)

        # === 2. Scoring Simulation ===

        # The core idea is that a team's run potential is their offense vs. the opponent's pitching and defense.
        # A higher value means more runs are likely to be scored.
        home_score_potential = (home_offense * 1.1) - (away_pitcher_rating * 0.9 + away_defense * 0.3)
        away_score_potential = (away_offense * 1.1) - (home_pitcher_rating * 0.9 + home_defense * 0.3)

        # Convert the "potential" into a final score.
        # We divide by a scaling factor to get a realistic run count and add randomness.
        home_score = int(max(0, (home_score_potential / 8.0) + random.uniform(-2.5, 3.5)))
        away_score = int(max(0, (away_score_potential / 8.0) + random.uniform(-2.5, 3.5)))

        # === 3. Post-game Updates ===

        # Update the win/loss/draw records for both teams based on the final score.
        if home_score > away_score:
            home_team.wins += 1
            away_team.losses += 1
        elif away_score > home_score:
            away_team.wins += 1
            home_team.losses += 1
        else:
            home_team.draws += 1
            away_team.draws += 1

        # Return a formatted string with the game's result for display.
        result_str = "{} {} - {} {}".format(home_team.name, home_score, away_score, away_team.name)
        return result_str
