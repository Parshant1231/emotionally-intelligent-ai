// frontend/lib/api.ts
// Central API client — all backend calls go through here

import axios from "axios";

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: { "Content-Type": "application/json" },
});

// ── Types ─────────────────────────────────────────────────────────

export type BotType = "ei" | "traditional";

export interface StartSessionPayload {
  bot_type:     BotType;
  age_group:    string;
  gender:       string;
  tech_comfort: string;
}

export interface StartSessionResponse {
  session_id: string;
  bot_type:   BotType;
  message:    string;
}

export interface ChatMessage {
  role:               "user" | "bot";
  content:            string;
  detected_emotion?:  string;
  emotion_confidence?: number;
  style_applied?:     string;
}

export interface ChatResponse {
  response:            string;
  turn:                number;
  bot_type:            BotType;
  detected_emotion?:   string;
  emotion_confidence?: number;
  style_applied?:      string;
}

export interface AnalyticsSummary {
  total_sessions:       number;
  total_messages:       number;
  avg_satisfaction:     { ei_bot: number; traditional_bot: number };
  emotion_distribution: Record<string, number>;
}

// ── API Functions ─────────────────────────────────────────────────

export const startSession = async (
  payload: StartSessionPayload
): Promise<StartSessionResponse> => {
  const { data } = await API.post("/api/chat/start", payload);
  return data;
};

export const sendMessage = async (
  session_id: string,
  message:    string,
  bot_type:   BotType
): Promise<ChatResponse> => {
  const { data } = await API.post("/api/chat/message", {
    session_id,
    message,
    bot_type,
  });
  return data;
};

export const endSession = async (
  session_id:   string,
  bot_type:     BotType,
  satisfaction: number
): Promise<void> => {
  await API.post("/api/chat/end", { session_id, bot_type, satisfaction });
};

export const getAnalyticsSummary = async (): Promise<AnalyticsSummary> => {
  const { data } = await API.get("/api/analytics/summary");
  return data;
};