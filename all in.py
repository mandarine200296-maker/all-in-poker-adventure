import tkinter as tk
from tkinter import messagebox
import random


# -----------------------------
# Global Game Data
# -----------------------------

player = {
    "name": "",
    "chips": 100,
    "confidence": 50,
    "reputation": 50
}

current_scene_index = 0


scenes = [
    {
        "title": "Scene 1: First Hand",
        "story": (
            "You sit down at your first Poker Night.\n\n"
            "You are holding A♣ Q♣. A confident player raises before the flop.\n"
            "Everyone at the table is watching your reaction.\n\n"
            "What will you do?"
        ),
        "choices": [
            {
                "text": "Fold safely",
                "result": "You fold and avoid early risk. It is a safe but quiet start.",
                "effects": {"chips": -5, "confidence": -2, "reputation": 0}
            },
            {
                "text": "Call",
                "result": "You call and stay in the hand. You feel more involved in the game.",
                "effects": {"chips": -10, "confidence": 5, "reputation": 2}
            },
            {
                "text": "Re-raise",
                "result": "You re-raise boldly. The table starts to notice your confidence.",
                "effects": {"chips": -20, "confidence": 10, "reputation": 8}
            }
        ]
    },
    {
        "title": "Scene 2: Bluff Chance",
        "story": (
            "The flop is revealed: 7♠ 9♦ K♣.\n\n"
            "Your hand is not very strong, but your opponent looks unsure.\n"
            "This might be a chance to bluff.\n\n"
            "What will you do?"
        ),
        "choices": [
            {
                "text": "Check",
                "result": "You check and wait. It is cautious, but you do not gain control.",
                "effects": {"chips": 0, "confidence": -2, "reputation": -1}
            },
            {
                "text": "Small bet",
                "result": "You make a small bet. It shows confidence without risking too much.",
                "effects": {"chips": -10, "confidence": 5, "reputation": 4}
            },
            {
                "text": "Big bluff",
                "result": "You make a big bluff. It is risky, but it creates pressure.",
                "effects": {"chips": -25, "confidence": 10, "reputation": 10}
            }
        ]
    },
    {
        "title": "Scene 3: Strong Hand",
        "story": (
            "You look down and see K♥ K♦.\n\n"
            "This is one of the strongest starting hands in Texas Hold'em.\n"
            "However, playing too aggressively may scare everyone away.\n\n"
            "How will you play this strong hand?"
        ),
        "choices": [
            {
                "text": "Slow play",
                "result": "You hide your strength and let others stay in the hand.",
                "effects": {"chips": 15, "confidence": 5, "reputation": 3}
            },
            {
                "text": "Standard raise",
                "result": "You make a clean raise. It is balanced and controlled.",
                "effects": {"chips": 25, "confidence": 8, "reputation": 6}
            },
            {
                "text": "Go all in",
                "result": "You go all in. The whole table reacts to your fearless move.",
                "effects": {"chips": -30, "confidence": 15, "reputation": 15}
            }
        ]
    },
    {
        "title": "Scene 4: Pressure Moment",
        "story": (
            "After several rounds, your chip stack is under pressure.\n\n"
            "Another player keeps raising and trying to push you out.\n"
            "You need to decide whether to protect your chips or fight back.\n\n"
            "What is your decision?"
        ),
        "choices": [
            {
                "text": "Protect chips",
                "result": "You protect your chips and wait for a better chance.",
                "effects": {"chips": -5, "confidence": -3, "reputation": -2}
            },
            {
                "text": "Call carefully",
                "result": "You call carefully and keep yourself in the game.",
                "effects": {"chips": -15, "confidence": 4, "reputation": 3}
            },
            {
                "text": "Fight back",
                "result": "You fight back with a strong raise. The table respects your courage.",
                "effects": {"chips": 20, "confidence": 8, "reputation": 8}
            }
        ]
    },
    {
        "title": "Scene 5: Final Table",
        "story": (
            "This is the final hand of the night.\n\n"
            "You are close to the top of the table, but one wrong decision could ruin everything.\n"
            "The final pot is large, and everyone is waiting for your move.\n\n"
            "How will you finish the night?"
        ),
        "choices": [
            {
                "text": "Play safe",
                "result": "You play safely and protect your final position.",
                "effects": {"chips": 10, "confidence": 2, "reputation": 1}
            },
            {
                "text": "Make a smart call",
                "result": "You make a smart call and win a solid pot.",
                "effects": {"chips": 30, "confidence": 8, "reputation": 8}
            },
            {
                "text": "Final all in",
                "result": "You push all in for the final hand. It is a dramatic ending.",
                "effects": {"chips": -40, "confidence": 20, "reputation": 20}
            }
        ]
    }
]


# -----------------------------
# Helper Functions
# -----------------------------

def reset_player(name):
    """Reset player data for a new game."""
    global player
    player = {
        "name": name,
        "chips": 100,
        "confidence": 50,
        "reputation": 50
    }


def update_status_label():
    """Update the status label on the screen."""
    status_text = (
        f"Player: {player['name']}    "
        f"Chips: {player['chips']}    "
        f"Confidence: {player['confidence']}    "
        f"Reputation: {player['reputation']}"
    )
    status_label.config(text=status_text)


def clear_window():
    """Remove all widgets from the main window."""
    for widget in root.winfo_children():
        widget.destroy()


def apply_effects(effects):
    """Apply choice effects to the player dictionary."""
    player["chips"] += effects["chips"]
    player["confidence"] += effects["confidence"]
    player["reputation"] += effects["reputation"]

    if player["confidence"] < 0:
        player["confidence"] = 0

    if player["reputation"] < 0:
        player["reputation"] = 0


def random_event():
    """Randomly return a special event."""
    events = [
        {
            "text": "Lucky moment! Your opponent misreads your move. You gain 15 chips.",
            "effects": {"chips": 15, "confidence": 3, "reputation": 2}
        },
        {
            "text": "Bad luck! The river card helps your opponent. You lose 15 chips.",
            "effects": {"chips": -15, "confidence": -3, "reputation": 0}
        },
        {
            "text": "The table respects your calm attitude. Your reputation increases.",
            "effects": {"chips": 0, "confidence": 2, "reputation": 5}
        },
        {
            "text": "You hesitate for too long. Your confidence drops slightly.",
            "effects": {"chips": 0, "confidence": -4, "reputation": -1}
        },
        None,
        None
    ]

    return random.choice(events)


def get_ending():
    """Decide the final ending based on player status."""
    chips = player["chips"]
    confidence = player["confidence"]
    reputation = player["reputation"]

    if chips >= 150 and reputation >= 70:
        return (
            "Poker Night Champion",
            "You played with confidence, earned respect, and finished with a strong chip stack. "
            "Tonight, you are the champion of Poker Night!"
        )
    elif chips >= 120:
        return (
            "Smart Strategist",
            "You made balanced decisions and protected your chips well. "
            "You may not be the loudest player, but your strategy worked."
        )
    elif reputation >= 80:
        return (
            "Table Legend",
            "Even though your chip stack was not perfect, everyone remembers your bold moves. "
            "You became the most exciting player at the table."
        )
    elif chips <= 30 and confidence >= 80:
        return (
            "Brave but Broke",
            "You played fearlessly and made dramatic choices, but your chips could not survive the night. "
            "At least nobody can say you were boring."
        )
    elif chips <= 0:
        return (
            "Early Exit",
            "You lost all your chips before the end of the night. "
            "It was a tough lesson, but every poker player starts somewhere."
        )
    else:
        return (
            "Learning Beginner",
            "You survived your first Poker Night and learned from every decision. "
            "With more practice, you could become a much stronger player."
        )


# -----------------------------
# Screen Functions
# -----------------------------

def show_main_menu():
    """Display the main menu."""
    clear_window()

    title = tk.Label(
        root,
        text="All In: A Poker Night Adventure",
        font=("Arial", 22, "bold"),
        fg="#1b4332"
    )
    title.pack(pady=30)

    subtitle = tk.Label(
        root,
        text="A poker-themed interactive story game",
        font=("Arial", 13)
    )
    subtitle.pack(pady=10)

    start_button = tk.Button(
        root,
        text="Start New Game",
        width=25,
        height=2,
        command=show_name_screen
    )
    start_button.pack(pady=12)

    rules_button = tk.Button(
        root,
        text="How to Play",
        width=25,
        height=2,
        command=show_rules
    )
    rules_button.pack(pady=12)

    exit_button = tk.Button(
        root,
        text="Exit",
        width=25,
        height=2,
        command=root.destroy
    )
    exit_button.pack(pady=12)


def show_name_screen():
    """Ask the player to enter a name."""
    clear_window()

    title = tk.Label(
        root,
        text="Create Your Player",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=25)

    instruction = tk.Label(
        root,
        text="Enter your player name:",
        font=("Arial", 13)
    )
    instruction.pack(pady=10)

    name_entry = tk.Entry(root, font=("Arial", 13), width=30)
    name_entry.pack(pady=10)

    def start_game_with_name():
        name = name_entry.get().strip()

        if name == "":
            messagebox.showwarning("Invalid Name", "Please enter a player name.")
            return

        reset_player(name)
        start_game()

    start_button = tk.Button(
        root,
        text="Start Adventure",
        width=20,
        height=2,
        command=start_game_with_name
    )
    start_button.pack(pady=15)

    back_button = tk.Button(
        root,
        text="Back to Menu",
        width=20,
        command=show_main_menu
    )
    back_button.pack(pady=5)


def show_rules():
    """Display game rules."""
    clear_window()

    title = tk.Label(
        root,
        text="How to Play",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=20)

    rules_text = (
        "In this game, you play as a beginner poker player at a casual Poker Night.\n\n"
        "You will go through five poker-themed story scenes. In each scene, you need to "
        "choose one action by clicking a button.\n\n"
        "Your choices will affect three status values:\n\n"
        "• Chips: your score and resources\n"
        "• Confidence: how brave and steady you are\n"
        "• Reputation: how other players see you\n\n"
        "Random events may also happen during the game.\n\n"
        "At the end, your final chips, confidence, and reputation will decide your ending."
    )

    rules_label = tk.Label(
        root,
        text=rules_text,
        font=("Arial", 12),
        wraplength=650,
        justify="left"
    )
    rules_label.pack(pady=10)

    back_button = tk.Button(
        root,
        text="Back to Menu",
        width=20,
        height=2,
        command=show_main_menu
    )
    back_button.pack(pady=20)


def start_game():
    """Start the game from the first scene."""
    global current_scene_index
    current_scene_index = 0
    show_scene()


def show_scene():
    """Display the current scene."""
    clear_window()

    global status_label

    if current_scene_index >= len(scenes):
        show_final_result()
        return

    scene = scenes[current_scene_index]

    title_label = tk.Label(
        root,
        text=scene["title"],
        font=("Arial", 20, "bold"),
        fg="#081c15"
    )
    title_label.pack(pady=15)

    story_label = tk.Label(
        root,
        text=scene["story"],
        font=("Arial", 12),
        wraplength=680,
        justify="left"
    )
    story_label.pack(pady=15)

    status_label = tk.Label(
        root,
        text="",
        font=("Arial", 12, "bold"),
        fg="#2d6a4f"
    )
    status_label.pack(pady=10)

    update_status_label()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    for i in range(3):
        choice = scene["choices"][i]
        choice_button = tk.Button(
            button_frame,
            text=choice["text"],
            width=20,
            height=2,
            command=lambda index=i: handle_choice(index)
        )
        choice_button.grid(row=0, column=i, padx=10)


def handle_choice(choice_index):
    """Handle the player's choice."""
    scene = scenes[current_scene_index]
    choice = scene["choices"][choice_index]

    apply_effects(choice["effects"])

    result_message = choice["result"]

    event = random_event()

    if event is not None:
        apply_effects(event["effects"])
        result_message += "\n\nRandom Event:\n" + event["text"]

    show_result_screen(result_message)


def show_result_screen(result_message):
    """Show the result after a choice before moving to the next scene."""
    clear_window()

    global status_label

    title_label = tk.Label(
        root,
        text="Result",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=20)

    result_label = tk.Label(
        root,
        text=result_message,
        font=("Arial", 12),
        wraplength=680,
        justify="left"
    )
    result_label.pack(pady=20)

    status_label = tk.Label(
        root,
        text="",
        font=("Arial", 12, "bold"),
        fg="#2d6a4f"
    )
    status_label.pack(pady=10)

    update_status_label()

    next_button = tk.Button(
        root,
        text="Continue",
        width=20,
        height=2,
        command=go_to_next_scene
    )
    next_button.pack(pady=20)


def go_to_next_scene():
    """Move to the next scene."""
    global current_scene_index
    current_scene_index += 1
    show_scene()


def show_final_result():
    """Display final ending."""
    clear_window()

    ending_title, ending_description = get_ending()

    title_label = tk.Label(
        root,
        text="Final Result",
        font=("Arial", 22, "bold"),
        fg="#1b4332"
    )
    title_label.pack(pady=20)

    ending_label = tk.Label(
        root,
        text=ending_title,
        font=("Arial", 18, "bold"),
        fg="#b85c00"
    )
    ending_label.pack(pady=10)

    description_label = tk.Label(
        root,
        text=ending_description,
        font=("Arial", 12),
        wraplength=680,
        justify="center"
    )
    description_label.pack(pady=15)

    final_status = (
        f"Final Status\n\n"
        f"Player: {player['name']}\n"
        f"Chips: {player['chips']}\n"
        f"Confidence: {player['confidence']}\n"
        f"Reputation: {player['reputation']}"
    )

    status_result_label = tk.Label(
        root,
        text=final_status,
        font=("Arial", 12, "bold"),
        fg="#2d6a4f"
    )
    status_result_label.pack(pady=15)

    menu_button = tk.Button(
        root,
        text="Back to Menu",
        width=20,
        height=2,
        command=show_main_menu
    )
    menu_button.pack(pady=15)


# -----------------------------
# Main Program
# -----------------------------

root = tk.Tk()
root.title("All In: A Poker Night Adventure")
root.geometry("760x560")
root.resizable(False, False)

show_main_menu()

root.mainloop()