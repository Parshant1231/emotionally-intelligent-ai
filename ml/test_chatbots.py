# ml/test_chatbots.py
# Runs both bots side by side — core of your OBJ 4 comparison

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from traditional_chatbot.bot import TraditionalChatbot
from ei_chatbot.bot import EIChatbot
import json

def run_comparison():
    print("="*65)
    print("🤖 CHATBOT COMPARISON TEST — Traditional vs EI")
    print("="*65)

    # Load both bots
    trad_bot = TraditionalChatbot()
    ei_bot   = EIChatbot()

    # These test messages cover different emotional states
    # Directly tied to your thesis OBJ 4
    test_messages = [
        "I'm so frustrated, nothing is working and I want to give up.",
        "I just got promoted at work, I'm so happy!",
        "I'm really scared about my exam results tomorrow.",
        "Can you help me understand how this works?",
        "I feel so alone, nobody understands me.",
    ]

    print("\n📊 Running same messages through BOTH bots...\n")

    for i, message in enumerate(test_messages, 1):
        print(f"{'='*65}")
        print(f"Turn {i} | User: {message}")
        print(f"{'-'*65}")

        # Traditional bot response
        trad_result = trad_bot.respond(message)
        print(f"🔵 TRADITIONAL : {trad_result['response']}")

        # EI bot response
        ei_result = ei_bot.respond(message)
        print(f"🟢 EI BOT      : {ei_result['response']}")
        print(f"   └─ Detected : {ei_result['detected_emotion'].upper()} "
              f"({ei_result['emotion_confidence']*100:.1f}% confidence)")
        print(f"   └─ Style    : {ei_result['style_applied']}")

    # Print EI session summary — this is thesis data
    print(f"\n{'='*65}")
    print("📋 EI BOT SESSION SUMMARY (Thesis Data — OBJ 3 & 4)")
    print(f"{'='*65}")
    summary = ei_bot.get_session_summary()
    print(f"Total turns         : {summary['total_turns']}")
    print(f"Emotions detected   : {summary['emotions_detected']}")
    print(f"Overall dominant    : {summary['dominant_emotion_overall'].upper()}")

    # Save session log to JSON — use this in your thesis analysis
    os.makedirs("../research", exist_ok=True)
    with open("../research/sample_session_log.json", "w") as f:
        json.dump(summary["full_log"], f, indent=2)
    print(f"\n✅ Full session log saved → research/sample_session_log.json")
    print("   Use this JSON data in your thesis Chapter 4 (Results)")


if __name__ == "__main__":
    run_comparison()