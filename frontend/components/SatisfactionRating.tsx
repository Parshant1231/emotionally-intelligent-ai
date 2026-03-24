// frontend/components/SatisfactionRating.tsx
// Post-session survey — feeds OBJ 3 & 4 thesis data

interface Props {
  onSubmit: (rating: number) => void;
  loading:  boolean;
}

export default function SatisfactionRating({ onSubmit, loading }: Props) {
  const ratings = [1, 2, 3, 4, 5];
  const labels  = ["Very Poor", "Poor", "Neutral", "Good", "Excellent"];

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm max-w-md mx-auto">
      <h3 className="text-base font-semibold text-gray-800 mb-1">
        Rate your experience
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        How satisfied were you with this conversation?
      </p>

      <div className="flex justify-between gap-2 mb-4">
        {ratings.map((r) => (
          <button
            key={r}
            onClick={() => !loading && onSubmit(r)}
            disabled={loading}
            className="flex-1 flex flex-col items-center gap-1 p-3 rounded-xl border
                       border-gray-200 hover:border-indigo-400 hover:bg-indigo-50
                       transition-all disabled:opacity-50 cursor-pointer group"
          >
            <span className="text-xl">
              {["😞", "😕", "😐", "🙂", "😄"][r - 1]}
            </span>
            <span className="text-xs text-gray-500 group-hover:text-indigo-600">
              {r}
            </span>
          </button>
        ))}
      </div>

      <div className="flex justify-between text-xs text-gray-400 px-1">
        <span>{labels[0]}</span>
        <span>{labels[4]}</span>
      </div>
    </div>
  );
}