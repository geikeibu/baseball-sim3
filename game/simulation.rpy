init python:
    import random

    def _get_pitcher_rating(pitcher):
        """
        Calculates an overall rating for a single pitcher based on their detailed stats.
        This helper function is not intended to be called from outside this file.
        """
        if not pitcher:
            return 20
        breaking_ball_rating = sum(pitcher.breaking_balls.values()) * 4
        pitcher_rating = (pitcher.speed * 0.15) + (pitcher.control * 0.4) + (pitcher.stamina * 0.2) + breaking_ball_rating
        return pitcher_rating

    def _simulate_at_bat(batter, pitcher):
        """
        Simulates a single at-bat between a batter and a pitcher.
        Returns the outcome of the at-bat as a string.
        """
        # --- Base Probabilities ---
        # These are the foundational chances for different events to occur in an at-bat.
        strikeout_prob = 0.20
        walk_prob = 0.08
        hit_prob = 0.25

        # --- Adjust Probabilities based on Player Stats ---

        # Pitcher's influence:
        # Higher control reduces walks and hits, increases strikeouts.
        strikeout_prob += (pitcher.control - 75) * 0.003
        walk_prob -= (pitcher.control - 75) * 0.002
        hit_prob -= (pitcher.control - 75) * 0.002
        # Higher speed increases strikeouts.
        strikeout_prob += (pitcher.speed - 150) * 0.002

        # Batter's influence:
        # Higher meet skill reduces strikeouts and increases hits.
        strikeout_prob -= (batter.meet - 75) * 0.004
        hit_prob += (batter.meet - 75) * 0.003

        # --- Determine the At-Bat Outcome ---
        rand_num = random.random()

        if rand_num < strikeout_prob:
            return "三振"
        elif rand_num < strikeout_prob + walk_prob:
            return "四球"
        elif rand_num < strikeout_prob + walk_prob + hit_prob:
            # It's a hit! Now determine the type of hit based on power.
            power_rating = (batter.power + pitcher.speed / 10.0) / 100.0
            hit_rand = random.random()
            if hit_rand < (0.05 * power_rating):
                return "本塁打"
            elif hit_rand < (0.05 * power_rating) + (0.20 * power_rating):
                return "三塁打"
            elif hit_rand < (0.05 * power_rating) + (0.20 * power_rating) + (0.35 * power_rating):
                return "二塁打"
            else:
                return "安打"
        else:
            # If it's not a strikeout, walk, or hit, it's an out from a ball in play.
            return "アウト"

    def simulate_game(home_team, away_team):
        """
        Simulates a detailed, inning-by-inning game between two teams.
        """
        # === 1. Pre-game Setup ===
        game_log = []
        highlights = []
        home_score, away_score = 0, 0
        inning = 1
        home_batting_order_index, away_batting_order_index = 0, 0

        home_pitcher = home_team.get_starting_pitcher()
        away_pitcher = away_team.get_starting_pitcher()
        home_batters = home_team.get_fielders()
        away_batters = away_team.get_fielders()

        game_log.append("試合開始！ {} vs {}".format(away_team.name, home_team.name))
        game_log.append("先発投手: {} ({}). {} ({})".format(away_team.name, away_pitcher.name, home_team.name, home_pitcher.name))

        # === 2. Main Game Loop ===
        while inning <= 9 or home_score == away_score:
            game_log.append("--- {}回 ---".format(inning))

            # --- Away Team's At-Bat (Top of the inning) ---
            game_log.append("▼ {}の攻撃".format(away_team.name))
            outs = 0
            bases = [None, None, None] # 1st, 2nd, 3rd base

            while outs < 3:
                batter = away_batters[away_batting_order_index]
                result = _simulate_at_bat(batter, home_pitcher)
                log_entry = "{}、{}の打席: {}".format(batter.name, away_team.name, result)
                game_log.append(log_entry)

                runs_this_play = 0
                if result == "安打":
                    if bases[2]: runs_this_play += 1; bases[2] = None
                    if bases[1]: bases[2] = bases[1]; bases[1] = None
                    if bases[0]: bases[1] = bases[0]
                    bases[0] = batter
                elif result == "二塁打":
                    if bases[2]: runs_this_play += 1; bases[2] = None
                    if bases[1]: runs_this_play += 1; bases[1] = None
                    if bases[0]: bases[2] = bases[0]; bases[0] = None
                    bases[1] = batter
                elif result == "三塁打":
                    runs_this_play += sum(1 for b in bases if b)
                    bases = [None, None, batter]
                elif result == "本塁打":
                    runs_this_play += sum(1 for b in bases if b) + 1
                    bases = [None, None, None]
                    highlight_msg = "{}回表、{}が{}から{}ランホームラン！".format(inning, batter.name, home_pitcher.name, runs_this_play)
                    highlights.append(highlight_msg)
                    game_log.append(highlight_msg)
                elif result == "四球":
                    if bases[0] and bases[1] and bases[2]: runs_this_play += 1
                    elif bases[0] and bases[1]: bases[2] = bases[1]
                    elif bases[0]: bases[1] = bases[0]
                    bases[0] = batter
                elif result == "三振":
                    outs += 1
                elif result == "アウト":
                    outs += 1

                if runs_this_play > 0:
                    away_score += runs_this_play
                    score_msg = "{}が{}点獲得！ 現在のスコア: {} {} - {} {}".format(away_team.name, runs_this_play, home_team.name, home_score, away_score, away_team.name)
                    game_log.append(score_msg)
                    if runs_this_play > 1:
                        highlights.append(score_msg)


                away_batting_order_index = (away_batting_order_index + 1) % len(away_batters)
                if outs == 3:
                    game_log.append("チェンジ")

            # --- Home Team's At-Bat (Bottom of the inning) ---
            if inning >= 9 and home_score > away_score:
                break # Walk-off win, no need to play bottom of the 9th.

            game_log.append("▲ {}の攻撃".format(home_team.name))
            outs = 0
            bases = [None, None, None]

            while outs < 3:
                batter = home_batters[home_batting_order_index]
                result = _simulate_at_bat(batter, away_pitcher)
                log_entry = "{}、{}の打席: {}".format(batter.name, home_team.name, result)
                game_log.append(log_entry)

                runs_this_play = 0
                if result == "安打":
                    if bases[2]: runs_this_play += 1; bases[2] = None
                    if bases[1]: bases[2] = bases[1]; bases[1] = None
                    if bases[0]: bases[1] = bases[0]
                    bases[0] = batter
                elif result == "二塁打":
                    if bases[2]: runs_this_play += 1; bases[2] = None
                    if bases[1]: runs_this_play += 1; bases[1] = None
                    if bases[0]: bases[2] = bases[0]; bases[0] = None
                    bases[1] = batter
                elif result == "三塁打":
                    runs_this_play += sum(1 for b in bases if b)
                    bases = [None, None, batter]
                elif result == "本塁打":
                    runs_this_play += sum(1 for b in bases if b) + 1
                    bases = [None, None, None]
                    highlight_msg = "{}回裏、{}が{}から{}ランホームラン！".format(inning, batter.name, away_pitcher.name, runs_this_play)
                    highlights.append(highlight_msg)
                    game_log.append(highlight_msg)
                elif result == "四球":
                    if bases[0] and bases[1] and bases[2]: runs_this_play += 1
                    elif bases[0] and bases[1]: bases[2] = bases[1]
                    elif bases[0]: bases[1] = bases[0]
                    bases[0] = batter
                elif result == "三振":
                    outs += 1
                elif result == "アウト":
                    outs += 1

                if runs_this_play > 0:
                    home_score += runs_this_play
                    score_msg = "{}が{}点獲得！ 現在のスコア: {} {} - {} {}".format(home_team.name, runs_this_play, home_team.name, home_score, away_score, away_team.name)
                    game_log.append(score_msg)
                    if runs_this_play > 1:
                        highlights.append(score_msg)

                home_batting_order_index = (home_batting_order_index + 1) % len(home_batters)
                if outs == 3:
                    game_log.append("チェンジ")

                if inning >= 9 and home_score > away_score:
                    break # Walk-off win

            inning += 1

        # === 3. Post-game Updates ===
        game_log.append("試合終了！")
        if home_score > away_score:
            home_team.wins += 1
            away_team.losses += 1
        elif away_score > home_score:
            away_team.wins += 1
            home_team.losses += 1
        else:
            home_team.draws += 1
            away_team.draws += 1

        if home_pitcher:
            fatigue_gain = 80 - (home_pitcher.stamina / 4.0)
            home_pitcher.fatigue = min(100, home_pitcher.fatigue + fatigue_gain)
        if away_pitcher:
            fatigue_gain = 80 - (away_pitcher.stamina / 4.0)
            away_pitcher.fatigue = min(100, away_pitcher.fatigue + fatigue_gain)

        # === 4. Return Game Data ===
        result_str = "{} {} - {} {}".format(home_team.name, home_score, away_score, away_team.name)

        # Select top 3 highlights
        top_highlights = highlights[:3]

        return {
            "result_str": result_str,
            "home_score": home_score,
            "away_score": away_score,
            "game_log": game_log,
            "highlights": top_highlights
        }
