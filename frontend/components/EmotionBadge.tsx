// frontend/components/EmotionBadge.tsx
// Shows detected emotion on EI bot messages — visual thesis evidence

interface Props {
  emotion:    string;
  confidence: number;
}

// Each emotion gets a color + emoji
const EMOTION_STYLES: Record<string, { bg: string; emoji: string }> = {
  joy:      { bg: "bg-yellow-100 text-yellow-800", emoji: "😊" },
  sadness:  { bg: "bg-blue-100 text-blue-800",     emoji: "😢" },
  anger:    { bg: "bg-red-100 text-red-800",        emoji: "😠" },
  fear:     { bg: "bg-purple-100 text-purple-800",  emoji: "😰" },
  disgust:  { bg: "bg-green-100 text-green-800",    emoji: "😒" },
  surprise: { bg: "bg-orange-100 text-orange-800",  emoji: "😲" },
  neutral:  { bg: "bg-gray-100 text-gray-700",      emoji: "😐" },
};

export default function EmotionBadge({ emotion, confidence }: Props) {
  const style = EMOTION_STYLES[emotion] ?? EMOTION_STYLES["neutral"];

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${style.bg}`}>
      {style.emoji} {emotion} · {(confidence * 100).toFixed(0)}%
    </span>
  );
}