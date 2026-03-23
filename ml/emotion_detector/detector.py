# ml/emotion_detector/detector.py

from transformers import pipeline
import json

# These are the 7 emotions this model detects
SUPPORTED_EMOTIONS = ["joy", "sadness", "anger", "fear", "disgust", "surprise", "neutral"]

class EmotionDetector:
    """
    Detects emotions in text using a pre-trained HuggingFace model.
    Model: j-hartmann/emotion-english-distilroberta-base
    
    This is the core of Objective 1 & 3 in your thesis.
    """

    def __init__(self):
        print("🔄 Loading emotion detection model...")
        
        # pipeline() is HuggingFace's easy interface
        # It handles: downloading model, tokenizing text, running inference
        # top_k=None means return scores for ALL emotions, not just the top 1
        self.model = pipeline(
            task="text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,
            device=-1  # -1 = use CPU (free). Change to 0 if you have a GPU
        )
        
        print("✅ Emotion model loaded successfully!")

    def detect(self, text: str) -> dict:
        """
        Analyze emotion in a single text string.

        Args:
            text: Any string — user message, sentence, etc.

        Returns:
            {
                "text": original text,
                "dominant_emotion": "anger",
                "confidence": 0.91,
                "all_scores": { "anger": 0.91, "joy": 0.02, ... }
            }
        
        Raises:
            ValueError: if text is empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Truncate very long texts — model has a 512 token limit
        text = text.strip()[:512]

        # Run the model — this is the actual inference call
        raw_results = self.model(text)[0]

        # raw_results looks like:
        # [{"label": "anger", "score": 0.91}, {"label": "joy", "score": 0.02}, ...]
        # We convert it to a clean dict
        all_scores = {
            item["label"]: round(item["score"], 4)
            for item in raw_results
        }

        # Find the emotion with the highest score
        dominant_emotion = max(all_scores, key=all_scores.get)
        confidence = all_scores[dominant_emotion]

        return {
            "text": text,
            "dominant_emotion": dominant_emotion,
            "confidence": confidence,
            "all_scores": all_scores
        }

    def detect_batch(self, texts: list[str]) -> list[dict]:
        """
        Analyze emotions for a list of texts at once.
        More efficient than calling detect() in a loop.
        
        Used for: analyzing your GoEmotions dataset in bulk
        """
        if not texts:
            raise ValueError("Text list cannot be empty")

        # Filter out empty strings
        cleaned = [t.strip()[:512] for t in texts if t and t.strip()]

        results = []
        for text in cleaned:
            results.append(self.detect(text))

        return results

    def detect_conversation(self, messages: list[dict]) -> list[dict]:
        """
        Analyze emotions across a full conversation.
        Used for Objective 3 — tracking emotional shift during a session.

        Args:
            messages: [{"role": "user", "content": "..."}, ...]

        Returns:
            list of emotion results for each user message only
        """
        user_messages = [
            msg["content"]
            for msg in messages
            if msg.get("role") == "user"
        ]

        results = self.detect_batch(user_messages)

        # Calculate sentiment shift — did emotion improve over conversation?
        # We define "positive" emotions as joy, and track if user moved toward it
        POSITIVE_EMOTIONS = {"joy", "surprise"}
        NEGATIVE_EMOTIONS = {"sadness", "anger", "fear", "disgust"}

        if len(results) >= 2:
            first_emotion = results[0]["dominant_emotion"]
            last_emotion = results[-1]["dominant_emotion"]

            if first_emotion in NEGATIVE_EMOTIONS and last_emotion in POSITIVE_EMOTIONS:
                shift = "improved"
            elif first_emotion in POSITIVE_EMOTIONS and last_emotion in NEGATIVE_EMOTIONS:
                shift = "worsened"
            else:
                shift = "stable"
        else:
            shift = "insufficient_data"

        return {
            "per_message": results,
            "sentiment_shift": shift,
            "total_messages_analyzed": len(results)
        }