screen dashboard_screen():
    tag menu

    # Use the game_menu screen for a consistent look and feel.
    # The content of this screen will be transcluded into the game_menu.
    use game_menu(_("順位・個人成績"), scroll="viewport", spacing=15):
        style_prefix "dash"

        # --- Data Loading ---
        $ standings = get_standings(persistent.teams)
        $ batting_avg_leaders = get_league_leaders(persistent.teams, "batting_avg")
        $ hr_leaders = get_league_leaders(persistent.teams, "home_runs")
        $ era_leaders = get_league_leaders(persistent.teams, "era")
        # Assuming the player's team is the first one in the list for "recent games"
        $ player_team_name = persistent.teams[0].name
        $ recent_games = [g for g in reversed(persistent.game_history) if g['home_team'] == player_team_name or g['away_team'] == player_team_name]


        # --- Main VBox container ---
        vbox:
            xfill True

            # --- Standings Section ---
            frame:
                style "dash_frame"
                vbox:
                    label _("リーグ順位表")
                    null height 5
                    grid 6 1: # 6 columns, 1 row for header
                        xfill True
                        text _("順位")
                        text _("チーム")
                        text _("勝")
                        text _("敗")
                        text _("分")
                        text _("首位差")

                    $ rank = 1
                    for team in standings:
                        grid 6 1:
                            xfill True
                            text "[rank]"
                            text "[team.name]"
                            text "[team.wins]"
                            text "[team.losses]"
                            text "[team.draws]"
                            text "[team.games_behind:.1f]"
                        $ rank += 1

            # --- League Leaders Section ---
            frame:
                style "dash_frame"
                vbox:
                    label _("個人成績")
                    null height 5
                    hbox:
                        spacing 20
                        # Batting Average
                        vbox:
                            label _("打率")
                            for p in batting_avg_leaders:
                                text "[p.name] ([p.team]): [p.stat_value:.3f]"
                            if not batting_avg_leaders:
                                text "規定打席未到達"
                        # Home Runs
                        vbox:
                            label _("本塁打")
                            for p in hr_leaders:
                                text "[p.name] ([p.team]): [p.stat_value]"
                            if not hr_leaders:
                                text "-"
                        # ERA
                        vbox:
                            label _("防御率")
                            for p in era_leaders:
                                text "[p.name] ([p.team]): [p.stat_value:.2f]"
                            if not era_leaders:
                                text "規定投球回未到達"

            # --- Recent Games Section ---
            frame:
                style "dash_frame"
                vbox:
                    label _("直近の試合結果 ([player_team_name])")
                    null height 5
                    if recent_games:
                        for game in recent_games:
                            text game.result_str
                    else:
                        text "試合記録がありません。"


# --- Styling for the new screen ---
style dash_frame is gui_frame
style dash_label is gui_label
style dash_label_text is gui_label_text
style dash_text is gui_text

style dash_frame:
    padding (15, 10)
    xfill True

style dash_label_text:
    size gui.label_text_size - 4

style dash_text:
    size gui.text_size - 2
