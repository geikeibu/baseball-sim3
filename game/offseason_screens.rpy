init python:
    # --- Trade Screen State Variables ---
    default trade_player_team = None
    default trade_other_team = None
    default trade_player_selected = None
    default trade_other_player_selected = None
    default trade_feedback_message = ""

    def get_player_team():
        # The player's team is assumed to be the first team in the list.
        return persistent.teams[0]

    def get_cpu_teams():
        return persistent.teams[1:]

    def execute_trade():
        global trade_feedback_message
        player_team = get_player_team()

        if not trade_player_selected or not trade_other_player_selected or not trade_other_team:
            trade_feedback_message = "選手を選択してください。"
            return

        player_value = calculate_trade_value(trade_player_selected)
        other_player_value = calculate_trade_value(trade_other_player_selected)

        # AI Logic: Accept if the offered player's value is at least 95% of their player's value
        if player_value >= other_player_value * 0.95:
            # Execute the trade
            player_team.players.remove(trade_player_selected)
            trade_other_team.players.remove(trade_other_player_selected)

            player_team.add_player(trade_other_player_selected)
            trade_other_team.add_player(trade_player_selected)

            trade_feedback_message = "トレード成立！"
            # Reset selections
            renpy.store.trade_player_selected = None
            renpy.store.trade_other_player_selected = None
        else:
            trade_feedback_message = "トレード拒否。相手が納得しませんでした。"


screen trade_screen():
    tag menu
    use game_menu(_("トレード"), scroll="viewport"):
        style_prefix "trade"

        hbox:
            spacing 20
            # --- Player's Team Column ---
            vbox:
                frame:
                    style "trade_frame"
                    label _("[get_player_team().name] (自チーム)")
                    null height 5

                    # Scrollable list of players
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            for p in get_player_team().players:
                                textbutton "[p.name] ([p.position[0]], [p.age]歳, 総[p.overall])" action SetField(renpy.store, "trade_player_selected", p)

            # --- Other Teams Column ---
            vbox:
                label _("交渉相手")
                $ cpu_teams = get_cpu_teams()
                for team in cpu_teams:
                    textbutton team.name action SetField(renpy.store, "trade_other_team", team)

                if trade_other_team:
                    frame:
                        style "trade_frame"
                        label _("[trade_other_team.name]")
                        null height 5
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            vbox:
                                for p in trade_other_team.players:
                                    textbutton "[p.name] ([p.position[0]], [p.age]歳, 総[p.overall])" action SetField(renpy.store, "trade_other_player_selected", p)

        # --- Trade Proposal Area ---
        frame:
            style "trade_frame"
            xalign 0.5
            vbox:
                label _("トレード提案")
                null height 10
                hbox:
                    spacing 30
                    # Player giving
                    vbox:
                        text _("放出する選手:")
                        if trade_player_selected:
                            text "[trade_player_selected.name] ([trade_player_selected.age]歳)"
                            text "総合力: [trade_player_selected.overall]"
                            text "トレード価値: [calculate_trade_value(trade_player_selected)]"
                        else:
                            text "未選択"

                    # Player receiving
                    vbox:
                        text _("獲得する選手:")
                        if trade_other_player_selected:
                            text "[trade_other_player_selected.name] ([trade_other_player_selected.age]歳)"
                            text "総合力: [trade_other_player_selected.overall]"
                            text "トレード価値: [calculate_trade_value(trade_other_player_selected)]"
                        else:
                            text "未選択"

                null height 10
                textbutton _("トレードを申し込む") action Function(execute_trade)

                if trade_feedback_message:
                    null height 5
                    text trade_feedback_message

# --- Styling ---
style trade_frame is gui_frame
style trade_frame:
    padding (10, 10)

# --- Draft Screen ---
init python:
    default draft_rookies = []
    default draft_order = []
    default draft_current_pick = 0
    default draft_player_selected = None
    default draft_log = []

    def generate_rookies(num_rookies=20):
        rookies = []
        for i in range(num_rookies):
            age = random.randint(18, 22)
            if random.random() > 0.3: # 70% chance of being a Fielder
                player = Fielder(
                    name="Rookie-F{}".format(i+1),
                    age=age,
                    meet=random.randint(40, 75),
                    power=random.randint(40, 75),
                    run=random.randint(40, 75),
                    defense=random.randint(40, 75),
                    throwing=random.randint(40, 75),
                    contract_years=4,
                    salary=500
                )
            else: # 30% chance of being a Pitcher
                player = Pitcher(
                    name="Rookie-P{}".format(i+1),
                    age=age,
                    speed=random.randint(130, 155),
                    control=random.randint(40, 75),
                    stamina=random.randint(40, 75),
                    breaking_balls={'slider': random.randint(1, 4)},
                    contract_years=4,
                    salary=500
                )
            rookies.append(player)
        # Sort rookies by overall so the best are at the top
        rookies.sort(key=lambda p: p.overall, reverse=True)
        return rookies

    def start_draft():
        # This function is called to set up the draft
        renpy.store.draft_rookies = generate_rookies()
        # Draft order is reverse standings of the previous year
        sorted_teams = sorted(persistent.teams, key=lambda t: t.wins)
        renpy.store.draft_order = sorted_teams
        renpy.store.draft_current_pick = 0
        renpy.store.draft_log = ["ドラフトを開始します。"]

    def draft_ai_pick():
        if not draft_rookies: return

        team = draft_order[draft_current_pick]
        best_rookie = draft_rookies[0] # Rookies are pre-sorted by overall

        team.add_player(best_rookie)
        draft_rookies.remove(best_rookie)

        draft_log.append("{}位 {}、{} を指名".format(draft_current_pick + 1, team.name, best_rookie.name))
        renpy.store.draft_current_pick += 1

        # Check if next pick is also AI
        if draft_current_pick < len(draft_order):
            next_team = draft_order[draft_current_pick]
            if next_team != get_player_team():
                renpy.call("draft_ai_pick_label")


    def player_draft_pick():
        if not draft_player_selected: return

        team = get_player_team()
        team.add_player(draft_player_selected)
        draft_rookies.remove(draft_player_selected)

        draft_log.append("{}位 {}、{} を指名".format(draft_current_pick + 1, team.name, draft_player_selected.name))
        renpy.store.draft_player_selected = None
        renpy.store.draft_current_pick += 1

        # Trigger next AI pick if there is one
        if draft_current_pick < len(draft_order):
            next_team = draft_order[draft_current_pick]
            if next_team != get_player_team():
                renpy.call("draft_ai_pick_label")


screen draft_screen():
    tag menu
    use game_menu(_("ドラフト会議"), scroll="viewport"):

        hbox:
            spacing 20
            # --- Rookie List ---
            vbox:
                label _("新人選手リスト")
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        for p in draft_rookies:
                            textbutton "[p.name] ([p.position[0]], [p.age]歳, 総[p.overall])" action SetField(renpy.store, "draft_player_selected", p)

            # --- Draft Log and Controls ---
            vbox:
                label _("指名ログ")
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        for entry in draft_log:
                            text entry

                null height 15

                # --- Player selection display and pick button ---
                if draft_current_pick < len(draft_order) and draft_order[draft_current_pick] == get_player_team():
                    label _("あなたの番です")
                    if draft_player_selected:
                        text "選択中の選手: [draft_player_selected.name]"
                        textbutton _("この選手を指名する") action Function(player_draft_pick)
                    else:
                        text "リストから選手を選択してください。"
                elif draft_current_pick >= len(draft_order):
                    label _("ドラフト終了")
                    textbutton _("ダッシュボードに戻る") action Show("dashboard_screen")
                else:
                    label _("AIが指名中...")

# Ren'Py labels to handle AI picks in the background
label draft_ai_pick_label:
    python:
        draft_ai_pick()
    return

label start_draft_label:
    python:
        start_draft()
    call screen draft_screen
    return

screen philosophy_screen():
    tag menu
    use game_menu(_("チーム方針設定"), scroll="viewport"):
        style_prefix "trade" # Reuse styles from trade screen for consistency

        $ player_team = get_player_team()

        vbox:
            spacing 15
            xalign 0.5
            yalign 0.5

            frame:
                style "trade_frame"
                padding (20, 20)
                vbox:
                    spacing 15
                    label _("来シーズンの方針を選択してください")

                    $ current_philosophy_text = {
                        "balanced": "バランス",
                        "power": "長打重視",
                        "speed": "機動力重視",
                        "defense": "守備重視"
                    }[player_team.philosophy]
                    text "現在の方針: [current_philosophy_text]"

                    null height 10

                    hbox:
                        spacing 20
                        xalign 0.5
                        textbutton _("長打重視") action [SetField(player_team, "philosophy", "power"), Hide("philosophy_screen"), Show("philosophy_screen")]
                        textbutton _("機動力重視") action [SetField(player_team, "philosophy", "speed"), Hide("philosophy_screen"), Show("philosophy_screen")]
                        textbutton _("守備重視") action [SetField(player_team, "philosophy", "defense"), Hide("philosophy_screen"), Show("philosophy_screen")]
                        textbutton _("バランス") action [SetField(player_team, "philosophy", "balanced"), Hide("philosophy_screen"), Show("philosophy_screen")]
