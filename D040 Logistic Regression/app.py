import streamlit as st
import json
import os
from datetime import date, datetime

st.set_page_config(page_title="Shiva's Transformation", page_icon="💪", layout="wide")

# ── Persistent storage (JSON file) ──────────────────────────────────────────
DATA_FILE = "shiva_progress.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"daily": {}, "weight_log": {}, "notes": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Plan data ────────────────────────────────────────────────────────────────
PLAN = {
    "Mon": {
        "workout_type": "Push Day 💪",
        "deficit": 380,
        "schedule": [
            ("5:00 AM", "Wake up", "Drink 500ml water immediately"),
            ("5:05 AM", "Pre-workout fuel", "Eat banana, then start workout"),
            ("5:10–6:10 AM", "WORKOUT", "Push day — 45 min"),
            ("6:10–7:00 AM", "Morning routine", "Freshen up, get ready, pack dabba"),
            ("7:00 AM", "Breakfast", "Oats with milk"),
            ("8:00 AM", "Leave for office", "Carry dabba + 1L water bottle"),
            ("10:30 AM", "Office snack", "Boiled egg + roasted chana at desk"),
            ("1:00–2:00 PM", "Lunch + study", "Eat dabba in 20 min, study rest of break"),
            ("4:00 PM", "Evening snack", "Curd + fruit"),
            ("7:00 PM", "Reach home", "Freshen up + 15 min walk"),
            ("7:30 PM", "Dinner", "Egg bhurji + rice + sabzi (you cook)"),
            ("8:00–11:00 PM", "Study block", "AI/ML prep — 3 hrs deep focus"),
            ("11:15 PM", "Wind down", "No screens, prep for tomorrow"),
            ("11:30 PM", "Sleep 😴", "5.5 hrs — screens off by 11:15"),
        ],
        "meals": [
            {"time": "5:05 AM", "name": "Banana (pre-workout)", "items": [("Banana (medium)", "1 whole", "~120g")], "protein": 1, "kcal": 90},
            {"time": "7:00 AM", "name": "Oats with milk", "items": [("Oats (dry)", "60g", "weigh dry before cooking"), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "on top"), ("Salt", "1 pinch", "")], "protein": 18, "kcal": 380},
            {"time": "10:30 AM", "name": "Boiled egg + roasted chana", "items": [("Boiled egg (whole)", "1 egg", "~60g — boil night before"), ("Roasted chana", "30g", "carry in small box")], "protein": 15, "kcal": 180},
            {"time": "1:00 PM", "name": "Egg curry + rice + sabzi (dabba)", "items": [("Eggs in curry", "2 eggs", "~120g"), ("Rice (dry, before cooking)", "80g", "= ~220g cooked"), ("Sabzi (any family curry)", "100g", ""), ("Cucumber + tomato", "100g", "EAT THESE FIRST always")], "protein": 26, "kcal": 550},
            {"time": "4:00 PM", "name": "Curd + fruit", "items": [("Curd / dahi", "150g", "carry in small dabba"), ("Guava or apple", "1 whole", "~150g")], "protein": 7, "kcal": 130},
            {"time": "7:30 PM", "name": "Egg bhurji + rice + sabzi (dinner)", "items": [("Eggs (for bhurji)", "2 eggs", "~120g"), ("Rice (dry)", "80g", "weigh before cooking"), ("Onion", "50g", ""), ("Tomato", "50g", ""), ("Oil", "3ml", "½ tsp only"), ("Sabzi (family curry)", "100g", ""), ("Cucumber", "80g", "eat first")], "protein": 24, "kcal": 560},
        ],
        "exercises": [
            {"name": "Warmup — jumping jacks", "sets": "5 min", "reps": "", "rest": "", "kcal": 30, "note": "Get heart rate up"},
            {"name": "Push-ups (standard)", "sets": "4 sets", "reps": "15 reps", "rest": "90 sec", "kcal": 40, "note": "Full range, chest to floor"},
            {"name": "Wide push-ups", "sets": "3 sets", "reps": "12 reps", "rest": "90 sec", "kcal": 30, "note": "Hands wider than shoulder-width"},
            {"name": "Pike push-ups", "sets": "3 sets", "reps": "10 reps", "rest": "60 sec", "kcal": 30, "note": "Hips high, nose to floor"},
            {"name": "Diamond push-ups", "sets": "3 sets", "reps": "8–10 reps", "rest": "60 sec", "kcal": 25, "note": "Hands form diamond shape"},
            {"name": "Chair dips", "sets": "3 sets", "reps": "12 reps", "rest": "60 sec", "kcal": 25, "note": "Elbows back, not flared"},
            {"name": "Cooldown stretch", "sets": "5 min", "reps": "", "rest": "", "kcal": 10, "note": "Chest, shoulders, triceps"},
        ],
    },
    "Tue": {
        "workout_type": "Pull Day 🏋",
        "deficit": 300,
        "schedule": [
            ("5:00 AM", "Wake up", "500ml water"),
            ("5:05 AM", "Pre-workout fuel", "Banana"),
            ("5:10–6:10 AM", "WORKOUT", "Pull day — 45 min"),
            ("6:10–7:00 AM", "Morning routine", "Get ready, pack chicken dabba"),
            ("7:00 AM", "Breakfast", "Oats with milk"),
            ("8:00 AM", "Leave for office", "Carry dabba + water"),
            ("10:30 AM", "Office snack", "Boiled egg + groundnuts"),
            ("1:00–2:00 PM", "Lunch + study", "Chicken dabba + study"),
            ("4:00 PM", "Evening snack", "Curd"),
            ("7:00 PM", "Reach home", "Freshen up + short walk"),
            ("7:30 PM", "Dinner", "Chicken + rice + sabzi"),
            ("8:00–11:00 PM", "Study block", "3 hrs"),
            ("11:30 PM", "Sleep 😴", ""),
        ],
        "meals": [
            {"time": "5:05 AM", "name": "Banana (pre-workout)", "items": [("Banana (medium)", "1 whole", "~120g")], "protein": 1, "kcal": 90},
            {"time": "7:00 AM", "name": "Oats with milk", "items": [("Oats (dry)", "60g", ""), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "")], "protein": 18, "kcal": 380},
            {"time": "10:30 AM", "name": "Boiled egg + groundnuts", "items": [("Boiled egg", "1 egg", "~60g"), ("Roasted groundnuts", "25g", "alternate with chana")], "protein": 14, "kcal": 215},
            {"time": "1:00 PM", "name": "Chicken + rice + sabzi (dabba) 🍗", "items": [("Chicken (raw weight)", "150g raw", "→ ~110g cooked, always weigh raw"), ("Rice (dry)", "80g", "= ~220g cooked"), ("Sabzi", "100g", ""), ("Cucumber + tomato", "100g", "EAT FIRST")], "protein": 32, "kcal": 580},
            {"time": "4:00 PM", "name": "Curd", "items": [("Curd / dahi", "150g", "")], "protein": 7, "kcal": 120},
            {"time": "7:30 PM", "name": "Chicken + rice + sabzi (dinner) 🍗", "items": [("Chicken (raw weight)", "150g raw", "→ ~110g cooked"), ("Rice (dry)", "80g", ""), ("Sabzi", "100g", ""), ("Dal / pappu (if available)", "80g cooked", ""), ("Cucumber", "80g", "eat first")], "protein": 32, "kcal": 600},
        ],
        "exercises": [
            {"name": "Warmup — arm circles + light jog", "sets": "5 min", "reps": "", "rest": "", "kcal": 30, "note": "Loosen shoulders"},
            {"name": "Australian rows (use table)", "sets": "4 sets", "reps": "10–12 reps", "rest": "90 sec", "kcal": 40, "note": "Lie under table, pull chest to edge"},
            {"name": "Superman holds", "sets": "3 sets", "reps": "12 reps", "rest": "60 sec", "kcal": 25, "note": "Hold 2 sec at top, squeeze glutes"},
            {"name": "Reverse snow angels (prone)", "sets": "3 sets", "reps": "15 reps", "rest": "60 sec", "kcal": 25, "note": "Face down, arms sweep overhead"},
            {"name": "Bicep curls (water bottles)", "sets": "3 sets", "reps": "15 reps", "rest": "60 sec", "kcal": 20, "note": "Full extension at bottom"},
            {"name": "Cooldown stretch", "sets": "5 min", "reps": "", "rest": "", "kcal": 10, "note": "Back, biceps, lats"},
        ],
    },
    "Wed": {
        "workout_type": "Legs + Core 🦵 (Hardest day!)",
        "deficit": 370,
        "schedule": [
            ("5:00 AM", "Wake up", "500ml water — legs day, you need hydration"),
            ("5:05 AM", "Pre-workout fuel", "Banana — don't skip on legs day"),
            ("5:10–6:10 AM", "WORKOUT", "Legs + core — hardest session of the week"),
            ("6:10–7:00 AM", "Morning routine", "Pack egg curry dabba"),
            ("7:00 AM", "Breakfast", "Oats with milk"),
            ("8:00 AM", "Leave for office", ""),
            ("10:30 AM", "Office snack", "Boiled egg + chana"),
            ("1:00–2:00 PM", "Lunch + study", ""),
            ("4:00 PM", "Evening snack", "Curd + groundnuts (bigger — legs day)"),
            ("7:00 PM", "Reach home", ""),
            ("7:30 PM", "Dinner", "Egg bhurji + rice + dal + sabzi — eat full dinner"),
            ("8:00–11:00 PM", "Study block", "3 hrs"),
            ("11:30 PM", "Sleep 😴", "Recovery starts now"),
        ],
        "meals": [
            {"time": "5:05 AM", "name": "Banana (pre-workout)", "items": [("Banana (medium)", "1 whole", "~120g")], "protein": 1, "kcal": 90},
            {"time": "7:00 AM", "name": "Oats with milk", "items": [("Oats (dry)", "60g", ""), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "")], "protein": 18, "kcal": 380},
            {"time": "10:30 AM", "name": "Boiled egg + roasted chana", "items": [("Boiled egg", "1 egg", "~60g"), ("Roasted chana", "30g", "")], "protein": 15, "kcal": 180},
            {"time": "1:00 PM", "name": "Egg curry + rice + sabzi (dabba)", "items": [("Eggs in curry", "2 eggs", "~120g"), ("Rice (dry)", "80g", ""), ("Sabzi", "100g", ""), ("Cucumber + carrot", "100g", "EAT FIRST")], "protein": 26, "kcal": 550},
            {"time": "4:00 PM", "name": "Curd + groundnuts (bigger — legs day)", "items": [("Curd / dahi", "150g", ""), ("Roasted groundnuts", "25g", "extra snack for hard day")], "protein": 12, "kcal": 265},
            {"time": "7:30 PM", "name": "Egg bhurji + rice + dal + sabzi", "items": [("Eggs (bhurji)", "2 eggs", "~120g"), ("Rice (dry)", "80g", ""), ("Onion", "50g", ""), ("Tomato", "50g", ""), ("Oil", "3ml", "½ tsp"), ("Dal / pappu (cooked)", "100g", "extra protein"), ("Sabzi", "100g", "")], "protein": 24, "kcal": 580},
        ],
        "exercises": [
            {"name": "Warmup — high knees", "sets": "5 min", "reps": "", "rest": "", "kcal": 35, "note": "Full warm up, legs need it"},
            {"name": "Bodyweight squats", "sets": "4 sets", "reps": "20 reps", "rest": "90 sec", "kcal": 50, "note": "Knee over toes, sit back into it"},
            {"name": "Bulgarian split squats", "sets": "3 sets", "reps": "10 reps each leg", "rest": "90 sec", "kcal": 45, "note": "Back foot on chair, go deep"},
            {"name": "Glute bridges", "sets": "4 sets", "reps": "15 reps", "rest": "60 sec", "kcal": 30, "note": "2 second hold at top, squeeze"},
            {"name": "Plank", "sets": "3 sets", "reps": "45 sec hold", "rest": "45 sec", "kcal": 20, "note": "Straight line head to heels"},
            {"name": "Bicycle crunches", "sets": "3 sets", "reps": "20 reps", "rest": "45 sec", "kcal": 20, "note": "Slow and controlled"},
            {"name": "Cooldown stretch", "sets": "5 min", "reps": "", "rest": "", "kcal": 10, "note": "Quads, hamstrings, hip flexors"},
        ],
    },
    "Thu": {
        "workout_type": "Push Day 2 💪",
        "deficit": 300,
        "schedule": [
            ("5:00 AM", "Wake up", "500ml water"),
            ("5:05 AM", "Pre-workout fuel", "Banana"),
            ("5:10–6:10 AM", "WORKOUT", "Push day 2 — variations"),
            ("6:10–7:00 AM", "Morning routine", "Pack chicken dabba"),
            ("7:00 AM", "Breakfast", "Oats with milk"),
            ("8:00 AM", "Leave for office", ""),
            ("10:30 AM", "Office snack", "Boiled egg + groundnuts"),
            ("1:00–2:00 PM", "Lunch + study", "Chicken dabba"),
            ("4:00 PM", "Evening snack", "Curd"),
            ("7:00 PM", "Reach home", ""),
            ("7:30 PM", "Dinner", "Chicken + rice + sabzi"),
            ("8:00–11:00 PM", "Study block", "3 hrs AI/ML prep"),
            ("11:30 PM", "Sleep 😴", ""),
        ],
        "meals": [
            {"time": "5:05 AM", "name": "Banana (pre-workout)", "items": [("Banana (medium)", "1 whole", "~120g")], "protein": 1, "kcal": 90},
            {"time": "7:00 AM", "name": "Oats with milk", "items": [("Oats (dry)", "60g", ""), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "")], "protein": 18, "kcal": 380},
            {"time": "10:30 AM", "name": "Boiled egg + groundnuts", "items": [("Boiled egg", "1 egg", "~60g"), ("Roasted groundnuts", "25g", "")], "protein": 14, "kcal": 215},
            {"time": "1:00 PM", "name": "Chicken + rice + sabzi (dabba) 🍗", "items": [("Chicken (raw weight)", "150g raw", "→ ~110g cooked"), ("Rice (dry)", "80g", ""), ("Sabzi", "100g", ""), ("Cucumber + tomato", "100g", "EAT FIRST")], "protein": 32, "kcal": 580},
            {"time": "4:00 PM", "name": "Curd", "items": [("Curd / dahi", "150g", "")], "protein": 7, "kcal": 120},
            {"time": "7:30 PM", "name": "Chicken + rice + sabzi (dinner) 🍗", "items": [("Chicken (raw weight)", "150g raw", ""), ("Rice (dry)", "80g", ""), ("Sabzi", "100g", ""), ("Dal / pappu (cooked)", "80g", ""), ("Cucumber", "80g", "eat first")], "protein": 32, "kcal": 600},
        ],
        "exercises": [
            {"name": "Warmup — jumping jacks", "sets": "5 min", "reps": "", "rest": "", "kcal": 30, "note": ""},
            {"name": "Decline push-ups (feet elevated on chair)", "sets": "4 sets", "reps": "12 reps", "rest": "90 sec", "kcal": 40, "note": "Targets upper chest"},
            {"name": "Incline push-ups (hands elevated)", "sets": "3 sets", "reps": "15 reps", "rest": "90 sec", "kcal": 35, "note": "Targets lower chest"},
            {"name": "Pike push-ups slow (3 sec down)", "sets": "3 sets", "reps": "10 reps", "rest": "60 sec", "kcal": 30, "note": "Slow eccentric = more muscle"},
            {"name": "Tricep overhead extension (water bottle)", "sets": "3 sets", "reps": "15 reps", "rest": "60 sec", "kcal": 20, "note": "Full extension overhead"},
            {"name": "Cooldown stretch", "sets": "5 min", "reps": "", "rest": "", "kcal": 10, "note": ""},
        ],
    },
    "Fri": {
        "workout_type": "HIIT 🔥 (Biggest calorie burn!)",
        "deficit": 400,
        "schedule": [
            ("5:00 AM", "Wake up", "500ml water — HIIT day"),
            ("5:05 AM", "Pre-workout fuel", "Banana — critical for HIIT"),
            ("5:10–6:10 AM", "WORKOUT", "HIIT — highest calorie burn of week"),
            ("6:10–7:00 AM", "Morning routine", "Pack egg curry dabba"),
            ("7:00 AM", "Breakfast", "Oats with milk"),
            ("8:00 AM", "Leave for office", ""),
            ("10:30 AM", "Office snack", "Boiled egg + chana"),
            ("1:00–2:00 PM", "Lunch + study", "Egg curry dabba"),
            ("4:00 PM", "Evening snack", "Curd + groundnuts (bigger — HIIT hunger)"),
            ("7:00 PM", "Reach home", ""),
            ("7:30 PM", "Dinner", "Dal + rice + sabzi (light dinner — max deficit)"),
            ("8:00–11:00 PM", "Study block", "3 hrs"),
            ("11:30 PM", "Sleep 😴", "Biggest deficit day done!"),
        ],
        "meals": [
            {"time": "5:05 AM", "name": "Banana (pre-workout) — don't skip!", "items": [("Banana (medium)", "1 whole", "~120g — HIIT needs this")], "protein": 1, "kcal": 90},
            {"time": "7:00 AM", "name": "Oats with milk", "items": [("Oats (dry)", "60g", ""), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "")], "protein": 18, "kcal": 380},
            {"time": "10:30 AM", "name": "Boiled egg + roasted chana", "items": [("Boiled egg", "1 egg", "~60g"), ("Roasted chana", "30g", "")], "protein": 15, "kcal": 180},
            {"time": "1:00 PM", "name": "Egg curry + rice + sabzi (dabba)", "items": [("Eggs in curry", "2 eggs", "~120g"), ("Rice (dry)", "80g", ""), ("Sabzi", "100g", ""), ("Cucumber + tomato", "100g", "EAT FIRST")], "protein": 26, "kcal": 550},
            {"time": "4:00 PM", "name": "Curd + groundnuts (bigger — HIIT hunger)", "items": [("Curd / dahi", "150g", ""), ("Roasted groundnuts", "25g", "")], "protein": 12, "kcal": 265},
            {"time": "7:30 PM", "name": "Dal + rice + sabzi (light dinner — max deficit)", "items": [("Dal / pappu (cooked)", "150g", "extra thick — more protein"), ("Rice (dry)", "80g", ""), ("Sabzi", "100g", ""), ("Cucumber", "80g", "eat first")], "protein": 15, "kcal": 450},
        ],
        "exercises": [
            {"name": "Jumping jacks", "sets": "4 rounds", "reps": "45 sec on / 15 sec off", "rest": "15 sec", "kcal": 60, "note": "Full arm extension"},
            {"name": "Burpees", "sets": "4 rounds", "reps": "30 sec on / 30 sec off", "rest": "30 sec", "kcal": 70, "note": "Hardest exercise — biggest burn"},
            {"name": "Mountain climbers", "sets": "3 rounds", "reps": "40 sec on", "rest": "20 sec", "kcal": 50, "note": "Drive knees to chest fast"},
            {"name": "Jump squats", "sets": "3 rounds", "reps": "30 sec on", "rest": "30 sec", "kcal": 55, "note": "Land softly, absorb with knees"},
            {"name": "High knees", "sets": "3 rounds", "reps": "40 sec on", "rest": "20 sec", "kcal": 45, "note": "Arms pump, knees to waist height"},
            {"name": "Cooldown stretch", "sets": "5 min", "reps": "", "rest": "", "kcal": 10, "note": "Full body — you earned it"},
        ],
    },
    "Sat": {
        "workout_type": "Active Rest + Meal Prep 🚶",
        "deficit": 200,
        "schedule": [
            ("6:30 AM", "Wake up (slight buffer)", "No alarm stress today"),
            ("6:45 AM", "Breakfast", "Oats with milk — no banana, rest day"),
            ("7:30–8:30 AM", "Brisk walk (outdoor)", "30–45 min Zone 2 cardio"),
            ("9:00 AM–12:00 PM", "Study block 1", "3 hrs — morning brain = best retention"),
            ("12:00–1:00 PM", "Break + lunch prep", ""),
            ("1:00 PM", "Lunch", "Chicken + rice + dal (slightly more — rest day)"),
            ("2:00–5:00 PM", "Study block 2", "3 hrs — revision, mock interviews"),
            ("4:00 PM", "Snack + MEAL PREP", "Boil 6 eggs + cook 500g chicken for week"),
            ("5:00–7:00 PM", "Personal time", "Relax, family time"),
            ("7:30 PM", "Dinner", "Egg bhurji + rice + sabzi"),
            ("11:00 PM", "Sleep 😴", "7.5 hrs — weekend recovery"),
        ],
        "meals": [
            {"time": "6:45 AM", "name": "Oats with milk (no banana today)", "items": [("Oats (dry)", "60g", ""), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "")], "protein": 18, "kcal": 380},
            {"time": "10:30 AM", "name": "Curd + groundnuts", "items": [("Curd / dahi", "150g", ""), ("Roasted groundnuts", "25g", "")], "protein": 12, "kcal": 265},
            {"time": "1:00 PM", "name": "Chicken + rice + dal + sabzi (relaxed lunch) 🍗", "items": [("Chicken (raw)", "180g raw", "→ ~135g cooked (more — rest day)"), ("Rice (dry)", "100g", "slightly more on rest day"), ("Dal / pappu (cooked)", "100g", ""), ("Sabzi", "100g", ""), ("Salad (cucumber+tomato+carrot)", "150g", "eat first — big salad today")], "protein": 38, "kcal": 680},
            {"time": "4:00 PM", "name": "Roasted chana (while meal prepping)", "items": [("Roasted chana", "30g", "snack while you cook for the week")], "protein": 8, "kcal": 110},
            {"time": "7:30 PM", "name": "Egg bhurji + rice + sabzi", "items": [("Eggs (bhurji)", "2 eggs", "~120g"), ("Rice (dry)", "80g", ""), ("Onion", "50g", ""), ("Tomato", "50g", ""), ("Oil", "3ml", "½ tsp"), ("Sabzi", "100g", "")], "protein": 24, "kcal": 560},
        ],
        "exercises": [
            {"name": "Brisk outdoor walk", "sets": "1 session", "reps": "30–45 min", "rest": "", "kcal": 120, "note": "Zone 2 — can talk but slightly breathless"},
            {"name": "Full body stretch", "sets": "15–20 min", "reps": "", "rest": "", "kcal": 20, "note": "Focus on sore muscles from the week"},
            {"name": "MEAL PREP — Boil 6 eggs", "sets": "One time", "reps": "Store in fridge", "rest": "", "kcal": 0, "note": "Saves every morning this week"},
            {"name": "MEAL PREP — Cook 500g chicken", "sets": "One time", "reps": "Store in airtight box", "rest": "", "kcal": 0, "note": "For Tue + Thu dabba — done in advance"},
        ],
    },
    "Sun": {
        "workout_type": "Full Rest 😴 + Cheat Meal",
        "deficit": 0,
        "schedule": [
            ("Morning", "Weigh yourself FASTED", "Before eating, after bathroom — write number below"),
            ("7:00 AM", "Breakfast", "Oats with milk — keep clean even on Sunday"),
            ("9:00 AM–12:00 PM", "Study block 1", "3 hrs"),
            ("1:00 PM", "CHEAT MEAL 🎉", "Biryani, outside food — anything. ONE MEAL only."),
            ("2:00–5:00 PM", "Study block 2", "3 hrs"),
            ("4:00 PM", "Snack", "Curd — reset after cheat meal"),
            ("5:00–7:00 PM", "Rest / family time", ""),
            ("7:30 PM", "Dinner", "Back to plan — egg bhurji + rice + sabzi"),
            ("11:00 PM", "Sleep 😴", "7.5 hrs — most important sleep of the week"),
        ],
        "meals": [
            {"time": "7:00 AM", "name": "Oats with milk (keep clean)", "items": [("Oats (dry)", "60g", ""), ("Full-fat milk", "200ml", ""), ("Roasted groundnuts", "15g", "")], "protein": 18, "kcal": 380},
            {"time": "1:00 PM", "name": "CHEAT MEAL 🎉 — Anything you want!", "items": [("Biryani / outside food / family special", "No weighing", "You earned this. Enjoy fully."), ("ONE MEAL ONLY", "", "Dinner is back to plan")], "protein": 20, "kcal": 800},
            {"time": "4:00 PM", "name": "Curd (reset)", "items": [("Curd / dahi", "150g", "back on track")], "protein": 7, "kcal": 120},
            {"time": "7:30 PM", "name": "Egg bhurji + rice + sabzi (back to plan)", "items": [("Eggs (bhurji)", "2 eggs", "~120g"), ("Rice (dry)", "80g", ""), ("Onion", "50g", ""), ("Tomato", "50g", ""), ("Oil", "3ml", ""), ("Sabzi", "100g", "")], "protein": 24, "kcal": 560},
        ],
        "exercises": [
            {"name": "No structured workout — FULL REST", "sets": "", "reps": "", "rest": "", "kcal": 0, "note": "Muscles grow on rest days, not workout days"},
            {"name": "Light walk (optional only)", "sets": "If you feel like it", "reps": "20–30 min", "rest": "", "kcal": 40, "note": "Don't force it"},
            {"name": "Sleep 7.5 hrs tonight", "sets": "Sleep by 11 PM", "reps": "", "rest": "", "kcal": 0, "note": "Most important recovery of the week"},
        ],
    },
}

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAY_COLORS = {"Mon": "🔵", "Tue": "🔴", "Wed": "🟢", "Thu": "🔵", "Fri": "🔥", "Sat": "🟡", "Sun": "🎉"}

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main > div { padding-top: 1rem; }
.metric-card { background: #f8f9fa; border-radius: 12px; padding: 14px; text-align: center; border: 1px solid #e9ecef; }
.metric-val { font-size: 1.8rem; font-weight: 600; color: #1a1a1a; }
.metric-label { font-size: 0.75rem; color: #666; margin-top: 2px; }
.fat-card { background: linear-gradient(135deg, #d4edda, #c3e6cb); border-radius: 14px; padding: 18px; border: 1px solid #b8dacc; margin: 12px 0; }
.meal-card { background: white; border: 1px solid #e9ecef; border-radius: 10px; padding: 14px; margin: 8px 0; }
.weight-item { display: flex; justify-content: space-between; align-items: center; background: #e8f4fd; border-radius: 8px; padding: 6px 10px; margin: 3px 0; font-size: 0.85rem; }
.weight-badge { background: #1976d2; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.schedule-row { display: flex; gap: 12px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.time-badge { background: #f0f0f0; padding: 3px 8px; border-radius: 8px; font-size: 0.75rem; color: #555; min-width: 90px; text-align: center; flex-shrink: 0; }
.ex-card { background: white; border: 1px solid #e9ecef; border-left: 4px solid #1976d2; border-radius: 8px; padding: 12px; margin: 6px 0; }
.rule-card { background: #fff8e1; border-left: 4px solid #f9a825; border-radius: 8px; padding: 10px 14px; margin: 6px 0; }
.progress-done { color: #2e7d32; font-weight: 600; }
.stProgress > div > div > div > div { background: #1976d2; }
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
data = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💪 Shiva's Tracker")
    st.markdown("**5'5\" · 76 kg start · Goal: 68 kg**")
    st.divider()

    today_name = date.today().strftime("%A")[:3]
    default_day = today_name if today_name in DAYS else "Mon"
    selected_day = st.radio("Select day", DAYS, index=DAYS.index(default_day), format_func=lambda d: f"{DAY_COLORS[d]} {d} — {PLAN[d]['workout_type']}")

    st.divider()
    st.markdown("### 📅 Today's date")
    st.markdown(f"**{date.today().strftime('%d %b %Y')}**")

    st.divider()
    st.markdown("### ⚖️ Weekly weigh-in")
    weigh_date = str(date.today())
    current_weight = st.number_input("Today's weight (kg)", min_value=50.0, max_value=120.0, value=76.0, step=0.1)
    if st.button("Log weight"):
        data["weight_log"][weigh_date] = current_weight
        save_data(data)
        st.success(f"Logged {current_weight} kg ✓")

    if data["weight_log"]:
        st.markdown("**Weight history:**")
        sorted_weights = sorted(data["weight_log"].items(), reverse=True)[:8]
        for d, w in sorted_weights:
            st.markdown(f"`{d}` → **{w} kg**")

# ── Main content ─────────────────────────────────────────────────────────────
plan = PLAN[selected_day]
date_key = f"{selected_day}_{date.today().isoformat()}"

if date_key not in data["daily"]:
    data["daily"][date_key] = {"meals": {}, "exercises": {}, "steps": 0}

day_data = data["daily"][date_key]

st.title(f"{DAY_COLORS[selected_day]} {selected_day}day — {plan['workout_type']}")

# ── Fat loss calculation ─────────────────────────────────────────────────────
meals_done = sum(1 for v in day_data["meals"].values() if v)
ex_done = sum(1 for v in day_data["exercises"].values() if v)
total_meals = len(plan["meals"])
total_ex = len(plan["exercises"])
steps = day_data.get("steps", 0)

meal_ratio = meals_done / total_meals if total_meals > 0 else 0
ex_kcal = sum(plan["exercises"][i]["kcal"] for i in range(total_ex) if day_data["exercises"].get(str(i)))
steps_kcal = int(steps * 0.04)
diet_deficit = int(plan["deficit"] * meal_ratio)
total_deficit = diet_deficit + ex_kcal + steps_kcal
fat_burned_g = round(total_deficit / 7.7, 1)
fat_week_g = round(fat_burned_g * 5.5, 1)
fat_month_g = round(fat_burned_g * 24, 1)
fat_month_kg = round(fat_month_g / 1000, 2)

# ── Fat card ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🔥 Fat burned today", f"{fat_burned_g}g", help="1g fat = 7.7 kcal deficit")
with col2:
    st.metric("📅 Est. this week", f"{fat_week_g}g")
with col3:
    st.metric("📆 Est. this month", f"{fat_month_kg} kg")
with col4:
    st.metric("⚡ Kcal deficit", f"{total_deficit}")

# Progress bars
st.markdown("---")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f"**🍽 Meals: {meals_done}/{total_meals}**")
    st.progress(meal_ratio)
with col_b:
    st.markdown(f"**🏋 Workout: {ex_done}/{total_ex}**")
    st.progress(ex_done / total_ex if total_ex > 0 else 0)
with col_c:
    st.markdown(f"**👟 Steps: {steps:,} / 10,000**")
    st.progress(min(1.0, steps / 10000))

# Steps input
st.markdown("**Update steps:**")
sc1, sc2, sc3, sc4, sc5 = st.columns(5)
with sc1:
    if st.button("➕ 1K"):
        day_data["steps"] = min(20000, day_data.get("steps", 0) + 1000)
        save_data(data); st.rerun()
with sc2:
    if st.button("➕ 2K"):
        day_data["steps"] = min(20000, day_data.get("steps", 0) + 2000)
        save_data(data); st.rerun()
with sc3:
    if st.button("➕ 5K"):
        day_data["steps"] = min(20000, day_data.get("steps", 0) + 5000)
        save_data(data); st.rerun()
with sc4:
    if st.button("✅ Done 10K"):
        day_data["steps"] = 10000
        save_data(data); st.rerun()
with sc5:
    if st.button("🔄 Reset steps"):
        day_data["steps"] = 0
        save_data(data); st.rerun()

if steps >= 10000:
    st.success("🎉 10,000 steps goal achieved today!")

# ── Tabs ─────────────────────────────────────────────────────────────────────
st.markdown("---")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗓 Schedule", "🍽 Meals", "🏋 Workout", "📊 Progress", "📋 Rules"])

# ── Tab 1: Schedule ──────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Today's full timeline")
    for time_str, activity, note in plan["schedule"]:
        cols = st.columns([1.2, 2, 3])
        with cols[0]:
            st.markdown(f"<span style='background:#f0f0f0;padding:3px 8px;border-radius:8px;font-size:0.78rem;color:#555'>{time_str}</span>", unsafe_allow_html=True)
        with cols[1]:
            weight = 600 if "WORKOUT" in activity or "Study" in activity or "Sleep" in activity or "CHEAT" in activity or "Weigh" in activity else 400
            st.markdown(f"<span style='font-weight:{weight}'>{activity}</span>", unsafe_allow_html=True)
        with cols[2]:
            if note:
                st.markdown(f"<span style='color:#666;font-size:0.85rem'>{note}</span>", unsafe_allow_html=True)

# ── Tab 2: Meals ─────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Today's meal plan with exact weights")
    st.info("⚖️ **Weigh rule:** Rice + oats = dry weight before cooking. Chicken = raw weight before cooking. Eggs/curd = as is.")

    total_protein = sum(m["protein"] for m in plan["meals"])
    total_kcal_plan = sum(m["kcal"] for m in plan["meals"])
    mc1, mc2 = st.columns(2)
    mc1.metric("Total protein today", f"{total_protein}g")
    mc2.metric("Total calories planned", f"{total_kcal_plan} kcal")

    st.markdown("---")
    for i, meal in enumerate(plan["meals"]):
        done = day_data["meals"].get(str(i), False)
        col_check, col_content = st.columns([0.08, 0.92])
        with col_check:
            checked = st.checkbox("", value=done, key=f"meal_{selected_day}_{i}")
            if checked != done:
                day_data["meals"][str(i)] = checked
                save_data(data)
                st.rerun()
        with col_content:
            status = "~~" if done else ""
            st.markdown(f"**{status}{meal['time']} — {meal['name']}{status}** &nbsp; `{meal['kcal']} kcal` &nbsp; `{meal['protein']}g protein`")
            for item_name, weight, note in meal["items"]:
                badge = f"<span style='background:#1976d2;color:white;padding:1px 7px;border-radius:10px;font-size:0.75rem;font-weight:600'>{weight}</span>"
                note_text = f" <span style='color:#888;font-size:0.8rem'>— {note}</span>" if note else ""
                st.markdown(f"&nbsp;&nbsp;&nbsp;{badge} &nbsp; {item_name}{note_text}", unsafe_allow_html=True)
        st.markdown("---")

    meals_completed = sum(1 for v in day_data["meals"].values() if v)
    if meals_completed == len(plan["meals"]):
        st.success("✅ All meals done today! Great discipline Shiva!")

# ── Tab 3: Workout ───────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"### {plan['workout_type']}")
    st.markdown("**Time: 5:10 AM – 6:10 AM &nbsp;|&nbsp; Duration: 45–60 min**")

    ex_total_kcal = sum(e["kcal"] for e in plan["exercises"])
    ec1, ec2 = st.columns(2)
    ec1.metric("Workout calorie burn", f"~{ex_total_kcal} kcal")
    ec2.metric("Exercises", f"{len(plan['exercises'])}")

    st.markdown("---")
    for i, ex in enumerate(plan["exercises"]):
        done = day_data["exercises"].get(str(i), False)
        col_chk, col_body = st.columns([0.08, 0.92])
        with col_chk:
            chk = st.checkbox("", value=done, key=f"ex_{selected_day}_{i}")
            if chk != done:
                day_data["exercises"][str(i)] = chk
                save_data(data)
                st.rerun()
        with col_body:
            border_color = "#4caf50" if done else "#1976d2"
            opacity = "0.5" if done else "1"
            sets_info = ""
            if ex["sets"]:
                sets_info += f"**{ex['sets']}**"
            if ex["reps"]:
                sets_info += f" × {ex['reps']}"
            if ex["rest"]:
                sets_info += f" &nbsp;|&nbsp; Rest: {ex['rest']}"
            if ex["kcal"] > 0:
                sets_info += f" &nbsp;|&nbsp; ~{ex['kcal']} kcal"

            st.markdown(f"""
            <div style='border-left:4px solid {border_color};padding:8px 12px;border-radius:6px;background:white;border:1px solid #e9ecef;opacity:{opacity};margin-bottom:4px'>
                <div style='font-weight:600;font-size:0.95rem'>{"✅ " if done else ""}{ex["name"]}</div>
                <div style='font-size:0.82rem;color:#555;margin-top:3px'>{sets_info}</div>
                {"<div style='font-size:0.8rem;color:#1976d2;margin-top:2px'>💡 " + ex["note"] + "</div>" if ex["note"] else ""}
            </div>""", unsafe_allow_html=True)

    ex_done_count = sum(1 for v in day_data["exercises"].values() if v)
    if ex_done_count == len(plan["exercises"]):
        st.success("🏆 Full workout complete! Beast mode activated!")
    elif ex_done_count > 0:
        st.info(f"💪 {ex_done_count}/{len(plan['exercises'])} exercises done — keep going!")

# ── Tab 4: Progress ──────────────────────────────────────────────────────────
with tab4:
    st.markdown("### 📊 Your transformation progress")

    if data["weight_log"]:
        import json
        weights = sorted(data["weight_log"].items())
        dates_list = [w[0] for w in weights]
        vals_list = [w[1] for w in weights]

        st.markdown("#### Weight log")
        for d, w in reversed(weights):
            diff = ""
            idx = dates_list.index(d)
            if idx > 0:
                change = w - vals_list[idx-1]
                diff = f" &nbsp; {'🔻' if change < 0 else '🔺'} {abs(change):.1f} kg"
            st.markdown(f"`{d}` &nbsp; **{w} kg**{diff}", unsafe_allow_html=True)

        start = vals_list[0]
        current = vals_list[-1]
        lost = start - current
        goal = 68.0
        remaining = current - goal
        pct = min(100, (lost / (start - goal)) * 100) if start != goal else 100

        st.markdown("---")
        p1, p2, p3 = st.columns(3)
        p1.metric("Starting weight", f"{start} kg")
        p2.metric("Current weight", f"{current} kg", delta=f"{-lost:.1f} kg" if lost > 0 else None)
        p3.metric("Goal (68 kg)", f"{remaining:.1f} kg to go")
        st.markdown(f"**Journey to goal: {pct:.0f}% complete**")
        st.progress(pct / 100)
    else:
        st.info("Log your weight in the sidebar to track progress here.")

    st.markdown("---")
    st.markdown("#### Fat loss calculator")
    st.markdown("""
    | Scenario | Daily deficit | Fat/week | Fat/month |
    |---|---|---|---|
    | Plan only (no steps) | ~350 kcal | ~320g | ~1.3 kg |
    | Plan + 10K steps | ~750 kcal | ~680g | ~2.7 kg |
    | Plan + 10K + full workout | ~1,050 kcal | ~950g | ~3.8 kg |

    > 1g of body fat = 7.7 kcal. These are estimates — actual results depend on metabolism.
    """)

    st.markdown("#### 90-day roadmap")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""**Month 1**
        - Lose 2–4 kg
        - Build the habit
        - Show up every day
        - Hardest mentally""")
    with r2:
        st.markdown("""**Month 2**
        - Lose 2–3 more kg
        - Visible change begins
        - Clothes fit differently
        - Strength goes up""")
    with r3:
        st.markdown("""**Month 3**
        - Target 68–70 kg
        - Muscle definition shows
        - Body recomp kicks in
        - Fully built routine""")

    st.markdown("---")
    st.markdown("#### Notes")
    note_key = str(date.today())
    note_val = data["notes"].get(note_key, "")
    new_note = st.text_area("Today's notes (how you felt, what was hard, wins)", value=note_val, height=100)
    if st.button("Save note"):
        data["notes"][note_key] = new_note
        save_data(data)
        st.success("Saved ✓")

# ── Tab 5: Rules ─────────────────────────────────────────────────────────────
with tab5:
    st.markdown("### 📋 The non-negotiables")

    rules = [
        ("🥚 Protein at every single meal", "Eggs, chicken, dal, curd — one must be on every plate. Without protein you lose muscle with fat."),
        ("🍚 Rice stays — 80g dry per meal max", "Don't cut rice. Just add protein alongside it. Rice is not your enemy."),
        ("🥗 Start every meal with salad / cucumber", "Eat 80–100g cucumber or salad FIRST. You'll eat less rice naturally."),
        ("💧 3.5+ litres of water daily", "Hyderabad heat is real. Carry a 1L bottle always. Dehydration fakes hunger."),
        ("🛌 Weekend sleep is sacred — 7.5 hrs min", "You're on 5.5 hrs weekdays. Weekend must compensate or you'll burn out."),
        ("🍱 Pack lunch dabba every single day", "Canteen food = unknown oil + calories. One dabba = diet on autopilot."),
        ("📈 Progressive overload weekly", "Add 1–2 reps per set every week. Same effort = no progress after 4 weeks."),
        ("⚖️ Weigh every Sunday morning fasted", "Before eating, after bathroom. Target: lose 0.5–1 kg/week. Faster = muscle loss."),
        ("🎉 One cheat MEAL per week max", "Sunday lunch — anything you want. Not cheat day. One meal. Dinner back to plan."),
        ("🚶 10,000 steps daily", "Walk to office, take stairs, walk after dinner. Steps are free fat burning."),
    ]
    for title, desc in rules:
        st.markdown(f"""
        <div style='background:#fff8e1;border-left:4px solid #f9a825;border-radius:8px;padding:10px 14px;margin:8px 0'>
            <div style='font-weight:600;font-size:0.95rem'>{title}</div>
            <div style='font-size:0.85rem;color:#555;margin-top:3px'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛒 Weekly shopping list")
    shopping = [
        ("Eggs", "1 tray (30)", "~₹200"),
        ("Oats", "500g", "~₹80"),
        ("Full-fat milk", "2L/week", "~₹90"),
        ("Roasted chana", "500g", "~₹60"),
        ("Roasted groundnuts", "500g", "~₹70"),
        ("Curd / dahi", "1kg", "~₹70"),
        ("Bananas", "7 (one/workout day)", "~₹35"),
        ("Chicken", "1kg raw/week", "~₹220"),
        ("Cucumber, tomato, carrot", "fresh weekly", "~₹50"),
        ("Rice, dal, sabzi", "family buys", "—"),
    ]
    for item, qty, cost in shopping:
        st.markdown(f"- **{item}** — {qty} &nbsp; `{cost}`")
    st.markdown("**Total food cost: ~₹875–1,000/week**")

    st.markdown("---")
    st.markdown("### ⚠️ Common mistakes to avoid")
    mistakes = [
        "Eating heaped cups of rice — measure 80g dry",
        "Skipping breakfast — muscle loss starts within hours",
        "Eating canteen food even once — breaks the calorie count",
        "Not drinking water — dehydration = fake hunger = overeating",
        "Sleeping less than 5.5 hrs — cortisol rises, fat storage increases",
        "Missing weekend meal prep — creates chaos all week",
        "Weighing chicken after cooking — always weigh raw",
    ]
    for m in mistakes:
        st.markdown(f"❌ {m}")
