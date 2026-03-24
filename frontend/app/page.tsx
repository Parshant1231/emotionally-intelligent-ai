// frontend/app/page.tsx
// Landing page — collects user characteristics (OBJ 2 data)

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { startSession, BotType } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();

  const [form, setForm] = useState({
    age_group:    "",
    gender:       "",
    tech_comfort: "",
    bot_type:     "" as BotType | "",
  });
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState("");

  const handleStart = async () => {
    if (!form.age_group || !form.gender || !form.tech_comfort || !form.bot_type) {
      setError("Please fill in all fields before starting.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const session = await startSession({
        bot_type:     form.bot_type as BotType,
        age_group:    form.age_group,
        gender:       form.gender,
        tech_comfort: form.tech_comfort,
      });

      // Store session in localStorage for chat page
      localStorage.setItem("session_id", session.session_id);
      localStorage.setItem("bot_type",   session.bot_type);

      router.push("/chat");
    } catch {
      setError("Failed to start session. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const Field = ({ label, name, options }: {
    label:   string;
    name:    keyof typeof form;
    options: { value: string; label: string }[];
  }) => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1.5">
        {label}
      </label>
      <select
        value={form[name]}
        onChange={(e) => setForm({ ...form, [name]: e.target.value })}
        className="w-full px-3 py-2.5 border border-gray-300 rounded-xl text-sm
                   focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
      >
        <option value="">Select...</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  );

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 to-white
                     flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200
                      w-full max-w-md p-8">

        {/* Header */}
        <div className="mb-6">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center
                          justify-center text-white text-lg mb-3">🧠</div>
          <h1 className="text-xl font-bold text-gray-900">
            EI-AI Research Study
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Please complete this short profile before starting the chat session.
          </p>
        </div>

        {/* Form */}
        <div className="space-y-4">
          <Field
            label="Age Group"
            name="age_group"
            options={[
              { value: "under-18", label: "Under 18" },
              { value: "18-24",    label: "18 – 24"  },
              { value: "25-34",    label: "25 – 34"  },
              { value: "35-44",    label: "35 – 44"  },
              { value: "45+",      label: "45+"       },
            ]}
          />
          <Field
            label="Gender"
            name="gender"
            options={[
              { value: "male",           label: "Male"            },
              { value: "female",         label: "Female"          },
              { value: "non-binary",     label: "Non-binary"      },
              { value: "prefer-not-say", label: "Prefer not to say" },
            ]}
          />
          <Field
            label="Tech Comfort Level"
            name="tech_comfort"
            options={[
              { value: "low",    label: "Low — I rarely use technology" },
              { value: "medium", label: "Medium — I use it regularly"   },
              { value: "high",   label: "High — I'm very tech-savvy"    },
            ]}
          />
          <Field
            label="Chat Session Type"
            name="bot_type"
            options={[
              { value: "ei",          label: "Session A" },
              { value: "traditional", label: "Session B" },
            ]}
          />

          <p className="text-xs text-gray-400">
            * Session type is randomly assigned as part of the study design.
          </p>
        </div>

        {error && (
          <p className="mt-4 text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">
            {error}
          </p>
        )}

        <button
          onClick={handleStart}
          disabled={loading}
          className="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 text-white
                     font-medium py-2.5 rounded-xl transition-colors
                     disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? "Starting session..." : "Start Chat Session →"}
        </button>
      </div>
    </main>
  );
}