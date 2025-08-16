# Define the screens for our game UI
screen pennant_screen():
    tag menu # This ensures the main menu is hidden when this screen is shown.

    # A vertical box layout to arrange our UI elements.
    vbox:
        xalign 0.5 # Center horizontally on the screen
        yalign 0.5 # Center vertically on the screen
        spacing 15 # Space between elements

        # Game Title
        text "Pennant Race" size 40

        # Display the result of the last simulated game.
        if game_result:
            text "Result: [game_result]"

        # A frame to neatly contain the league standings.
        frame:
            padding (15, 15)
            vbox:
                spacing 5
                text "League Standings"
                # Standings Table Header
                hbox:
                    spacing 10
                    text "Team" xsize 250
                    text "Wins" xsize 60
                    text "Losses" xsize 60
                    text "Draws" xsize 60
                # We sort the teams by wins in descending order for the standings.
                $ sorted_teams = sorted(persistent.teams, key=lambda t: t.wins, reverse=True)
                for team in sorted_teams:
                    hbox:
                        spacing 10
                        text team.name xsize 250
                        text str(team.wins) xsize 60
                        text str(team.losses) xsize 60
                        text str(team.draws) xsize 60

        # Game action buttons
        hbox:
            spacing 20
            # Show the "Next Game" button only if there are games left in the schedule.
            if schedule:
                textbutton "1試合進める" action Call("play_next_game")
                textbutton "5試合進める" action Call("play_multiple_games", game_count=5)
                textbutton "シーズン終了まで" action Call("play_multiple_games", game_count=len(schedule))

            # Show the "View Log" button if a log exists for the previous game.
            if persistent.last_game_log:
                textbutton "試合ログを見る" action Show("game_log_screen")

        # When the season is over, show end-of-season options.
        if not schedule:
            vbox:
                spacing 15
                text "Season Finished!" size 28
                textbutton "Restart Season" action Call("reset_and_start")
                textbutton "Main Menu" action MainMenu()


# --- Game Logic ---

init python:
    def rest_all_pitchers():
        """
        Reduces fatigue for every pitcher on every team to simulate a day of rest.
        """
        if persistent.teams:
            for team in persistent.teams:
                for pitcher in team.get_pitchers():
                    # Each day of rest reduces fatigue by a set amount.
                    # We use max() to ensure fatigue doesn't drop below 0.
                    pitcher.fatigue = max(0, pitcher.fatigue - 30)

    def _play_one_game():
        """
        Helper function to simulate a single game.
        This contains the logic previously in the play_next_game label.
        """
        if not schedule:
            return

        # First, process a day of rest for all pitchers in the league.
        rest_all_pitchers()

        # Then, get the next matchup from the front of the schedule list.
        home_team, away_team = schedule.pop(0)
        # Simulate the game and store the outcome.
        sim_result = simulate_game(home_team, away_team)

        # Store the results for display on the screen.
        # These are global variables, so we need to declare that.
        global game_result
        game_result = sim_result["result_str"]
        persistent.last_game_log = sim_result["game_log"]
        persistent.last_game_highlights = sim_result["highlights"]

# Default variables that will hold the game's state.
default game_result = ""
default schedule = []
default persistent.last_game_log = []
default persistent.last_game_highlights = []


# The game's entry point.
label start:
    # We immediately jump to the season setup.
    jump start_season

label start_season:
    # This block runs at the beginning of each season.
    python:
        # Reset wins, losses, rotation, and fatigue for all teams.
        for t in persistent.teams:
            t.wins = 0
            t.losses = 0
            t.draws = 0
            t.rotation_index = 0
            for p in t.get_pitchers():
                p.fatigue = 0

        # Generate the season schedule.
        schedule = []
        teams = list(persistent.teams)
        # Create a double round-robin schedule (each team plays every other team home and away).
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                schedule.append((teams[i], teams[j]))
                schedule.append((teams[j], teams[i]))

        # Shuffle the schedule for variety each season.
        renpy.random.shuffle(schedule)

        # Set an initial message for the result display and clear previous game logs.
        game_result = "The season is about to begin!"
        persistent.last_game_log = []
        persistent.last_game_highlights = []


    # Show the main pennant screen to the player.
    call screen pennant_screen
    return

label play_next_game:
    # This block is called when the player clicks "Simulate Next Game".
    python:
        _play_one_game()

    # Re-display the screen to show the updated results and standings.
    call screen pennant_screen
    return

label play_multiple_games(game_count):
    # This block is called to simulate multiple games at once.
    python:
        # Loop for the given number of games.
        for _ in range(game_count):
            # If the schedule is empty, stop simulating.
            if not schedule:
                break
            _play_one_game()

    # After simulating, update the screen.
    call screen pennant_screen
    return

label reset_and_start:
    # This allows the player to restart the season from the end screen.
    jump start_season
