import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

# ----------------- ΡΥΘΜΙΣΕΙΣ ΕΦΑΡΜΟΓΗΣ -----------------
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Παιχνίδι", layout="wide")
st.title("🚢 AdOnBoard - Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🏴‍☠️")

# ----------------- ΔΕΔΟΜΕΝΑ ΣΚΑΦΩΝ & ΧΟΡΗΓΩΝ -----------------
sponsors = ["Nike", "Red Bull", "Vodafone", "Adidas", "North Face", "Coca-Cola"]
boats = ["BlueWave", "SailVenture", "Golden Horizon", "Sunset Cruiser", "Ocean Explorer"]
boat_capacity = {"BlueWave": 10, "SailVenture": 8, "Golden Horizon": 9, "Sunset Cruiser": 10, "Ocean Explorer": 8}

# ----------------- ΔΗΜΙΟΥΡΓΙΑ ΠΑΙΚΤΩΝ -----------------
st.sidebar.header("📌 Επιλογές Παικτών")
num_players = st.sidebar.slider("Πόσοι παίκτες θα παίξουν; (1-10):", 2, 10, 4)
selected_boat = st.sidebar.selectbox("🚤 Επιλέξτε Σκάφος:", boats)
selected_sponsor = st.sidebar.selectbox("💰 Επιλέξτε Χορηγό:", sponsors)

players = {f"Παίκτης {i+1}": {"θέση": 0, "χρήματα": 100000, "likes": 0, "sponsor": selected_sponsor} for i in range(num_players)}

# ----------------- HOTSPOTS & VIP EVENTS -----------------
hotspots = ["Mykonos Paradise Beach", "Santorini Red Beach", "Rhodes Faliraki", "Zakynthos Navagio", "Corfu Old Town"]
quiet_areas = ["Kythnos Kolona", "Andros Golden Sand", "Lefkada Porto Katsiki", "Alonissos Marine Park"]

# ----------------- LEADERBOARD -----------------
def show_leaderboard():
    leaderboard = pd.DataFrame.from_dict(players, orient='index')[['χρήματα', 'likes']]
    leaderboard = leaderboard.sort_values(by=['χρήματα', 'likes'], ascending=False)
    st.sidebar.subheader("🏆 Leaderboard")
    st.sidebar.dataframe(leaderboard)

# ----------------- ΔΗΜΙΟΥΡΓΙΑ ΧΑΡΤΗ & ΔΙΑΔΡΟΜΩΝ -----------------
def draw_board():
    fig, ax = plt.subplots(figsize=(8, 8))
    locations = hotspots + quiet_areas
    np.random.shuffle(locations)
    angles = np.linspace(0, 2*np.pi, len(locations), endpoint=False)
    positions = np.array([np.cos(angles), np.sin(angles)]).T * 10
    
    for i, (x, y) in enumerate(positions):
        color = "red" if locations[i] in hotspots else "blue"
        ax.add_patch(plt.Circle((x, y), 1, fill=True, color=color))
        ax.text(x, y, locations[i], ha='center', fontsize=10, fontweight='bold')
    
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    st.pyplot(fig)

def roll_dice():
    return random.randint(1, 6)

# ----------------- ΚΙΝΗΣΗ ΠΑΙΚΤΩΝ & CHALLENGES -----------------
def move_player(player):
    roll = roll_dice()
    st.write(f"🎲 {player} έριξε **{roll}**!")
    time.sleep(1)
    new_position = (players[player]["θέση"] + roll) % len(hotspots + quiet_areas)
    players[player]["θέση"] = new_position
    current_location = (hotspots + quiet_areas)[new_position]
    
    if current_location in hotspots:
        players[player]["χρήματα"] += 5000
        players[player]["likes"] += 2000
        st.success(f"🔥 Το {player} βρέθηκε σε hotspot! +5000€ και +2000 likes!")
    else:
        players[player]["χρήματα"] += 2000
        st.info(f"🌊 {player} έφτασε σε μια ήσυχη περιοχή. +2000€.")
    
    challenge = random.choice(["Διαφημιστική Καμπάνια!", "Συναυλία Beach Party!", "Χορηγία VIP Event!", "Extreme Sailing Challenge!"])
    st.write(f"📢 {challenge}")

# ----------------- ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ -----------------
if st.button("🎲 Ρίξε το Ζάρι!"):
    for player in players:
        move_player(player)
    draw_board()
    show_leaderboard()

draw_board()
show_leaderboard()
