// frontend/app/chat/page.tsx
"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { sendMessage, endSession, BotType, ChatMessage } from "@/lib/api";
import MessageBubble from "@/components/MessageBubble";
import SatisfactionRating from "@/components/SatisfactionRating";

export default function ChatPage() {
  const router = useRouter();

  const [sessionId, setSessionId] = useState<string>("");
  const [botType,   setBotType]   = useState<BotType>("ei");
  const [messages,  setMessages]  = useState<ChatMessage[]>([]);
  const [input,     setInput]     = useState("");
  const [loading,   setLoading]   = useState(false);
  const [showRating, setShowRating] = useState(false);
  const [rated,      setRated]      = useState(false);
  const [turnCount,  setTurnCount]  = useState(0);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const sid = localStorage.getItem("session_id");
    const bt  = localStorage.getItem("bot_type") as BotType;

    if (!sid || !bt) { router.push("/"); return; }

    setSessionId(sid);
    setBotType(bt);

    // Welcome message
    setMessages([{
      role:    "bot",
      content: bt === "ei"
        ? "Hello! I'm here to chat and help. How are you feeling today?"
        : "Hello! How can I help you today?",
    }]);
  }, [router]);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg: ChatMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendMessage(sessionId, userMsg.content, botType);

      const botMsg: ChatMessage = {
        role:               "bot",
        content:            res.response,
        detected_emotion:   res.detected_emotion,
        emotion_confidence: res.emotion_confidence,
        style_applied:      res.style_applied,
      };

      // Attach emotion data to the user message for badge display
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...userMsg,
          detected_emotion:   res.detected_emotion,
          emotion_confidence: res.emotion_confidence,
        };
        return [...updated, botMsg];
      });

      setTurnCount(res.turn);

      // Show rating after 5 turns
      if (res.turn >= 5) setShowRating(true);

    } catch {
      setMessages((prev) => [...prev, {
        role:    "bot",
        content: "Sorry, something went wrong. Please try again.",
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleRating = async (rating: number) => {
    setLoading(true);
    try {
      await endSession(sessionId, botType, rating);
      setRated(true);
      localStorage.removeItem("session_id");
      localStorage.removeItem("bot_type");
    } catch {
      console.error("Failed to save rating");
    } finally {
      setLoading(false);
    }
  };

  // ── Rated / Thank you screen ──────────────────────────────────
  if (rated) {
    return (
      <main className="min-h-screen bg-indigo-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200
                        max-w-md w-full p-8 text-center">
          <div className="text-4xl mb-4">🎉</div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            Thank you!
          </h2>
          <p className="text-sm text-gray-500 mb-6">
            Your responses have been recorded for the research study.
          </p>
          <button
            onClick={() => router.push("/")}
            className="bg-indigo-600 text-white px-6 py-2.5 rounded-xl
                       text-sm font-medium hover:bg-indigo-700 transition-colors"
          >
            Start New Session
          </button>
        </div>
      </main>
    );
  }

  // ── Main Chat UI ──────────────────────────────────────────────
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">

      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3
                         flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center
                          justify-center text-white text-sm">🧠</div>
          <div>
            <p className="text-sm font-semibold text-gray-900">
              {botType === "ei" ? "Session A" : "Session B"}
            </p>
            <p className="text-xs text-gray-400">
              {turnCount} turn{turnCount !== 1 ? "s" : ""}
            </p>
          </div>
        </div>

        {/* EI badge — shows this is emotionally aware */}
        {botType === "ei" && (
          <span className="text-xs bg-indigo-50 text-indigo-700 px-2.5 py-1
                           rounded-full font-medium border border-indigo-100">
            ✨ Active
          </span>
        )}
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3 max-w-2xl
                      w-full mx-auto">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} botType={botType} />
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="flex items-start gap-2">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm
                            px-4 py-2.5 shadow-sm">
              <div className="flex gap-1 items-center h-4">
                {[0, 1, 2].map((i) => (
                  <div key={i}
                    className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Satisfaction rating — appears after 5 turns */}
      {showRating && !rated && (
        <div className="px-4 py-4 max-w-2xl w-full mx-auto">
          <SatisfactionRating onSubmit={handleRating} loading={loading} />
        </div>
      )}

      {/* Input bar */}
      <div className="bg-white border-t border-gray-200 px-4 py-3 sticky bottom-0">
        <div className="max-w-2xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
            placeholder="Type a message..."
            disabled={loading || rated}
            className="flex-1 px-4 py-2.5 border border-gray-300 rounded-xl text-sm
                       focus:outline-none focus:ring-2 focus:ring-indigo-500
                       disabled:bg-gray-50 disabled:text-gray-400"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim() || rated}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5
                       rounded-xl text-sm font-medium transition-colors
                       disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}