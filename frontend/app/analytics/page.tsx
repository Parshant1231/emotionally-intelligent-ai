// frontend/app/analytics/page.tsx
// Research dashboard — shows live thesis data

"use client";

import { useState, useEffect } from "react";
import { getAnalyticsSummary, AnalyticsSummary } from "@/lib/api";

export default function AnalyticsPage() {
  const [data,    setData]    = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalyticsSummary()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-gray-500 text-sm">Loading research data...</p>
    </main>
  );

  if (!data) return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-red-500 text-sm">Failed to load data. Is the backend running?</p>
    </main>
  );

  const Card = ({ label, value }: { label: string; value: string | number }) => (
    <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
      <p className="text-xs text-gray-500 font-medium uppercase tracking-wide mb-1">
        {label}
      </p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto">

        <h1 className="text-xl font-bold text-gray-900 mb-1">
          Research Dashboard
        </h1>
        <p className="text-sm text-gray-500 mb-6">
          Live data from all chat sessions — OBJ 3 &amp; 4 evidence
        </p>

        {/* Summary cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card label="Total Sessions" value={data.total_sessions} />
          <Card label="Total Messages" value={data.total_messages} />
          <Card label="EI Satisfaction"   value={data.avg_satisfaction.ei_bot || "—"} />
          <Card label="Trad Satisfaction" value={data.avg_satisfaction.traditional_bot || "—"} />
        </div>

        {/* Emotion distribution */}
        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-800 mb-3">
            Emotion Distribution
          </h2>
          {Object.entries(data.emotion_distribution).length === 0 ? (
            <p className="text-sm text-gray-400">No emotion data yet.</p>
          ) : (
            <div className="space-y-2">
              {Object.entries(data.emotion_distribution)
                .sort(([, a], [, b]) => b - a)
                .map(([emotion, count]) => {
                  const total = Object.values(data.emotion_distribution)
                    .reduce((a, b) => a + b, 0);
                  const pct = Math.round((count / total) * 100);
                  return (
                    <div key={emotion} className="flex items-center gap-3">
                      <span className="w-20 text-xs text-gray-600 capitalize">
                        {emotion}
                      </span>
                      <div className="flex-1 bg-gray-100 rounded-full h-2">
                        <div
                          className="bg-indigo-500 h-2 rounded-full transition-all"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 w-8 text-right">
                        {pct}%
                      </span>
                    </div>
                  );
                })}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}