"use client";

import { useState, useEffect } from "react";
import { education } from "@/lib/api";
import { useLangStore, useAuthStore } from "@/lib/store";
import { t } from "@/lib/i18n";

interface Content {
  id: string;
  title: string;
  content_type: string;
  language: string;
  difficulty_level: string;
  content: any;
}

const TYPE_ICONS: Record<string, string> = {
  tip: "💡",
  article: "📄",
  quiz: "📋",
};

const LANG_FLAGS: Record<string, string> = {
  en: "🇬🇧",
  zh: "🇨🇳",
  ms: "🇲🇾",
  ta: "🇮🇳",
};

export default function EducationPage() {
  const { language } = useLangStore();
  const { token } = useAuthStore();
  const [items, setItems] = useState<Content[]>([]);
  const [selected, setSelected] = useState<Content | null>(null);
  const [filterLang, setFilterLang] = useState("all");
  const [loading, setLoading] = useState(true);
  // Quiz state
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [quizResult, setQuizResult] = useState<{ score: number; total: number } | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => { loadContent(); }, [filterLang]);

  const loadContent = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (filterLang !== "all") params.language = filterLang;
      const { data } = await education.list(filterLang !== "all" ? filterLang : undefined);
      setItems(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSubmit = async (contentId: string) => {
    if (!token) return;
    setSubmitting(true);
    try {
      const { data } = await education.submitQuiz(contentId, answers);
      setQuizResult({ score: data.score, total: data.total });
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gray-50 p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">{t("education.title", language)}</h1>
        <p className="text-gray-500 mb-6">{t("education.subtitle", language)}</p>

        {/* Language filter */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {[{ code: "all", label: "All" }, ...LANGUAGES].map((l) => (
            <button
              key={l.code}
              onClick={() => { setFilterLang(l.code); setSelected(null); }}
              className={`px-3 py-1.5 rounded-lg text-sm transition ${
                filterLang === l.code
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-100 border"
              }`}
            >
              {"flag" in l ? l.flag + " " : ""}{l.label}
            </button>
          ))}
        </div>

        {/* Content grid */}
        {loading ? (
          <div className="text-center py-12 text-gray-400">Loading...</div>
        ) : selected ? (
          <div className="bg-white rounded-2xl shadow-md p-6">
            <button onClick={() => { setSelected(null); setQuizResult(null); setAnswers({}); }}
              className="text-sm text-blue-600 hover:underline mb-4">
              ← Back to list
            </button>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">{TYPE_ICONS[selected.content_type] || "📄"}</span>
              <span className="text-xs uppercase bg-gray-100 px-2 py-0.5 rounded">{selected.content_type}</span>
              <span className="text-xs text-gray-400">{LANG_FLAGS[selected.language]} {selected.language.toUpperCase()}</span>
            </div>
            <h2 className="text-2xl font-bold mb-4">{selected.title}</h2>

            {selected.content_type === "quiz" ? (
              <div>
                {selected.content.questions?.map((q: any, i: number) => (
                  <div key={q.id} className="mb-6 p-4 bg-gray-50 rounded-lg">
                    <p className="font-medium mb-3">{i + 1}. {q.question}</p>
                    <div className="space-y-2">
                      {Object.entries(q.options).map(([key, val]) => (
                        <label key={key} className={`flex items-center gap-3 p-2 rounded cursor-pointer transition ${
                          answers[q.id] === key ? "bg-blue-50 border border-blue-300" : "hover:bg-gray-100"
                        }`}>
                          <input
                            type="radio"
                            name={q.id}
                            value={key}
                            checked={answers[q.id] === key}
                            onChange={() => setAnswers({ ...answers, [q.id]: key })}
                            disabled={!!quizResult}
                          />
                          <span className="text-sm"><strong>{key.toUpperCase()}.</strong> {val as string}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
                {quizResult ? (
                  <div className={`p-4 rounded-lg ${quizResult.score === quizResult.total ? "bg-green-50 text-green-700" : "bg-yellow-50 text-yellow-700"}`}>
                    <p className="font-bold text-lg">Score: {quizResult.score}/{quizResult.total}</p>
                    <p className="text-sm mt-1">
                      {quizResult.score === quizResult.total
                        ? "🎉 Perfect! You have excellent phishing awareness!"
                        : "Keep learning to improve your detection skills."}
                    </p>
                  </div>
                ) : (
                  <button
                    onClick={() => handleQuizSubmit(selected.id)}
                    disabled={submitting || Object.keys(answers).length === 0}
                    className="bg-blue-600 text-white px-6 py-2.5 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                  >
                    {submitting ? "Submitting..." : "Submit Answers"}
                  </button>
                )}
              </div>
            ) : (
              <div className="prose prose-sm max-w-none">
                {selected.content.body?.split("\n").map((line: string, i: number) => (
                  <p key={i} className="mb-2 text-gray-700">{line}</p>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {items.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelected(item)}
                className="bg-white rounded-xl shadow-sm p-5 hover:shadow-md transition cursor-pointer border"
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-2xl">{TYPE_ICONS[item.content_type] || "📄"}</span>
                  <span className="text-xs uppercase bg-gray-100 px-2 py-0.5 rounded">{item.content_type}</span>
                  <span className="text-xs text-gray-400">{LANG_FLAGS[item.language]}</span>
                </div>
                <h3 className="font-semibold mb-1">{item.title}</h3>
                <p className="text-xs text-gray-400 capitalize">{item.difficulty_level}</p>
              </div>
            ))}
            {items.length === 0 && (
              <div className="col-span-full text-center py-12 text-gray-400">
                No education content found for this filter.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

const LANGUAGES = [
  { code: "en", label: "English", flag: "🇬🇧" },
  { code: "zh", label: "中文", flag: "🇨🇳" },
  { code: "ms", label: "Melayu", flag: "🇲🇾" },
  { code: "ta", label: "தமிழ்", flag: "🇮🇳" },
];
