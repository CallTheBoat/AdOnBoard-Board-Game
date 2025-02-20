import streamlit as st
import random

def start_game():
    st.title("🚀 AdOnBoard: Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🎲")

    players = st.number_input("Πόσοι παίκτες θα παίξουν; (1-4):", min_value=1, max_value=4, step=1)
    if st.button("Ξεκίνα το παιχνίδι!"):
        st.session_state["players"] = players
        st.session_state["game_started"] = True
        st.experimental_rerun()

if "game_started" not in st.session_state:
    st.session_state["game_started"] = False

if st.session_state["game_started"]:
    def play_game():
        routes = ["Πολικός Αστέρας", "Φεγγάρι", "Ναυτίλος", "Φάρος", "Άνεμος"]
        event_cards = [
            "Κακοκαιρία! Χάνεις έναν γύρο.",
            "Χορηγία από τη Vodafone! Κερδίζεις 200.000€.",
            "Βλάβη στο GPS! Πληρώνεις 50.000€.",
            "Καλός καιρός! Προχωράς 2 θέσεις μπροστά.",
            "Ναύλωση VIP! Κερδίζεις 300.000€."
        ]

        if "player_data" not in st.session_state:
            st.session_state["player_data"] = {f"Παίκτης {i+1}": {"money": 1000000, "position": 0} for i in range(st.session_state["players"])}

        for player in st.session_state["player_data"]:
            st.write(f"### {player}, ρίξε το ζάρι... 🎲")
            if st.button(f"Ρίξε ζάρι ({player})"):
                roll = random.randint(1, 6)
                st.session_state["player_data"][player]["position"] = (st.session_state["player_data"][player]["position"] + roll) % len(routes)
                st.write(f"{player} μετακινήθηκε στη διαδρομή: {routes[st.session_state['player_data'][player]['position']]}!")

                event = random.choice(event_cards)
                st.write(f"🃏 Κάρτα συμβάντος: {event}")

                if "Κερδίζεις" in event:
                    amount = int(event.split()[2].replace("€.", ""))
                    st.session_state["player_data"][player]["money"] += amount
                elif "Πληρώνεις" in event:
                    amount = int(event.split()[2].replace("€.", ""))
                    st.session_state["player_data"][player]["money"] -= amount

                st.write(f"{player} τώρα έχει **{st.session_state['player_data'][player]['money']}€**.")
                st.experimental_rerun()

        if st.button("Τέλος παιχνιδιού"):
            st.session_state["game_started"] = False
            st.experimental_rerun()

    play_game()
else:
    start_game()
