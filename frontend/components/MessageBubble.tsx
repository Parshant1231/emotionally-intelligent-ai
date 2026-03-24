// frontend/components/MessageBubble.tsx

import EmotionBadge from "./EmotionBadge";
import { ChatMessage } from "@/lib/api";

interface Props {
  message:  ChatMessage;
  botType:  "ei" | "traditional";
}

export default function MessageBubble({ message, botType }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex flex-col ${isUser ? "items-end" : "items-start"} gap-1`}>

      {/* Bubble */}
      <div className={`max-w-[75%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed
        ${isUser
          ? "bg-indigo-600 text-white rounded-br-sm"
          : "bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm"
        }`}
      >
        {message.content}
      </div>

      {/* Emotion badge — only on user messages in EI bot mode */}
      {isUser && botType === "ei" && message.detected_emotion && (
        <EmotionBadge
          emotion={message.detected_emotion}
          confidence={message.emotion_confidence ?? 0}
        />
      )}

      {/* Style applied — shows EI bot's response strategy */}
      {!isUser && botType === "ei" && message.style_applied && (
        <span className="text-xs text-gray-400 px-1">
          💡 {message.style_applied}
        </span>
      )}
    </div>
  );
}