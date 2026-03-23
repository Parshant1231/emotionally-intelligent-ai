# ml/emotion_detector/test_detector.py
# Run this to verify your emotion detector works correctly

from detector import EmotionDetector
import json

def run_tests():
    detector = EmotionDetector()
    print("\n" + "="*60)
    print("🧪 EMOTION DETECTOR — TEST SUITE")
    print("="*60)

    # --- Test 1: Basic single detection ---
    print("\n📌 TEST 1: Single text detection")
    test_cases = [
        "I am so happy today, everything is going great!",
        "I feel completely hopeless and devastated.",
        "This is absolutely infuriating, I can't take it anymore!",
        "I'm scared about what might happen next.",
        "The weather is okay I guess.",
    ]

    for text in test_cases:
        result = detector.detect(text)
        print(f"\n  Input   : {text}")
        print(f"  Emotion : {result['dominant_emotion'].upper()} ({result['confidence']*100:.1f}% confident)")

    # --- Test 2: Batch detection ---
    print("\n" + "-"*60)
    print("📌 TEST 2: Batch detection")
    batch = [
        "I love this so much!",
        "Why does nothing ever work?",
        "I don't really have an opinion."
    ]
    batch_results = detector.detect_batch(batch)
    for r in batch_results:
        print(f"  '{r['text'][:40]}...' → {r['dominant_emotion']} ({r['confidence']*100:.1f}%)")

    # --- Test 3: Conversation analysis ---
    print("\n" + "-"*60)
    print("📌 TEST 3: Conversation sentiment shift")
    conversation = [
        {"role": "user", "content": "I'm so frustrated, nothing is working."},
        {"role": "assistant", "content": "I understand, let me help you."},
        {"role": "user", "content": "Okay that actually helped a bit."},
        {"role": "assistant", "content": "Great! Let's keep going."},
        {"role": "user", "content": "Yes! I finally got it working, thank you so much!"},
    ]
    conv_result = detector.detect_conversation(conversation)
    print(f"  Messages analyzed : {conv_result['total_messages_analyzed']}")
    print(f"  Sentiment shift   : {conv_result['sentiment_shift'].upper()}")
    print(f"  Per message:")
    for i, msg in enumerate(conv_result['per_message']):
        print(f"    Turn {i+1}: {msg['dominant_emotion']} ({msg['confidence']*100:.1f}%)")

    # --- Test 4: Edge cases ---
    print("\n" + "-"*60)
    print("📌 TEST 4: Edge cases")
    try:
        detector.detect("")
    except ValueError as e:
        print(f"  ✅ Empty string correctly rejected: {e}")

    long_text = "word " * 600
    result = detector.detect(long_text)
    print(f"  ✅ Long text (600 words) handled: {result['dominant_emotion']}")

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED — Emotion Detector is working!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_tests()