screen game_log_screen():
    tag menu

    use game_menu("試合ログ", scroll="viewport", spacing=10):
        style_prefix "log"

        vbox:
            spacing 15

            # --- Highlights Section ---
            frame:
                style "log_frame"
                vbox:
                    spacing 5
                    label _("今日のハイライト")
                    if persistent.last_game_highlights:
                        for highlight in persistent.last_game_highlights:
                            text highlight
                    else:
                        text "ハイライトはありません。"

            # --- Full Game Log Section ---
            frame:
                style "log_frame"
                vbox:
                    spacing 5
                    label _("全プレイ記録")
                    if persistent.last_game_log:
                        for event in persistent.last_game_log:
                            text event
                    else:
                        text "試合ログはありません。"

# --- Styling for the new screen ---
style log_frame is gui_frame
style log_label is gui_label
style log_label_text is gui_label_text
style log_text is gui_text

style log_frame:
    padding (15, 10)
    xfill True

style log_label_text:
    size gui.label_text_size - 4

style log_text:
    size gui.text_size - 2
