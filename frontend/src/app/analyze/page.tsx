"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { analyze } from "@/lib/api";
import { useAuthStore, useLangStore } from "@/lib/store";
import { t } from "@/lib/i18n";

interface Pattern {
  type: string;
  confidence: number;
  evidence: string;
  explanation: string;
}

interface Result {
  id: string;
  risk_score: number;
  risk_level: "low" | "medium" | "high";
  detected_language: string;
  detected_patterns: Pattern[];
  recommendation: string;
  model_version: string;
}

const RISK_STYLES = {
  low: { bg: "bg-green-50", border: "border-green-300", text: "text-green-700", emoji: "🟢" },
  medium: { bg: "bg-yellow-50", border: "border-yellow-300", text: "text-yellow-700", emoji: "🟡" },
  high: { bg: "bg-red-50", border: "border-red-300", text: "text-red-700", emoji: "🔴" },
};

export default function AnalyzePage() {
  const router = useRouter();
  const { token } = useAuthStore();
  const { language } = useLangStore();
  const [text, setText] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) router.push("/login");
  }, [token, router]);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const { data } = await analyze.submit(text);
      setResult(data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        router.push("/login");
      } else {
        setError(err.response?.data?.detail || "Analysis failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const risk = result ? RISK_STYLES[result.risk_level] : null;

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gray-50 p-4 md:p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">{t("analyze.title", language)}</h1>
        <p className="text-gray-500 mb-6">{t("analyze.subtitle", language)}</p>

        {/* Input */}
        <div className="bg-white rounded-2xl shadow-md p-6 mb-6">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full border rounded-xl px-4 py-3 h-40 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm"
            placeholder={t("analyze.placeholder", language)}
          />
          <div className="flex items-center justify-between mt-4">
            <span className="text-xs text-gray-400">
              {text.length} characters
            </span>
            <button
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
              className="bg-blue-600 text-white px-6 py-2.5 rounded-xl hover:bg-blue-700 transition disabled:opacity-50 font-medium"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  {t("analyze.analyzing", language)}
                </span>
              ) : (
                t("analyze.analyzeButton", language)
              )}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-xl text-sm">
            {error}
          </div>
        )}

        {/* Result */}
        {result && risk && (
          <div className={`bg-white rounded-2xl shadow-md p-6 border-l-4 ${risk.border}`}>
            {/* Risk badge */}
            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg ${risk.bg} ${risk.text} mb-4`}>
              <span>{risk.emoji}</span>
              <span className="font-bold uppercase text-sm">
                {t(`risk.${result.risk_level}`, language)} RISK
              </span>
              <span className="text-sm opacity-75">
                — {result.risk_score}/100
              </span>
            </div>

            {/* Score bar */}
            <div className="mb-4">
              <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    result.risk_level === "high"
                      ? "bg-red-500"
                      : result.risk_level === "medium"
                      ? "bg-yellow-500"
                      : "bg-green-500"
                  }`}
                  style={{ width: `${result.risk_score}%` }}
                />
              </div>
            </div>

            <p className="text-xs text-gray-400 mb-4">
              {t("analyze.detectedLanguage", language)}:{" "}
              <strong>{result.detected_language.toUpperCase()}</strong>
              <span className="ml-3">Model: {result.model_version}</span>
            </p>

            {/* Detected patterns */}
            {result.detected_patterns.length > 0 && (
              <>
                <h3 className="font-semibold mb-2">{t("analyze.detectedThreats", language)}</h3>
                <ul className="space-y-2 mb-4">
                  {result.detected_patterns.map((p, i) => (
                    <li key={i} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                      <span className="text-red-500 mt-0.5">⚠️</span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-sm">{p.type.replace(/_/g, " ")}</span>
                          <span className="text-xs bg-gray-200 px-1.5 py-0.5 rounded">
                            {Math.round(p.confidence * 100)}%
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-0.5">
                          &ldquo;{p.evidence}&rdquo; — {p.explanation}
                        </p>
                      </div>
                    </li>
                  ))}
                </ul>
              </>
            )}

            {/* Recommendation */}
            <div className={`p-4 rounded-lg ${risk.bg}`}>
              <h3 className="font-semibold mb-1">💡 {t("analyze.recommendation", language)}</h3>
              <p className="text-sm text-gray-700">{result.recommendation}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
