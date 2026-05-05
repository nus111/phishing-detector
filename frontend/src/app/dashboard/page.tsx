"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { analyze } from "@/lib/api";
import { useAuthStore, useLangStore } from "@/lib/store";
import { t } from "@/lib/i18n";

interface HistoryItem {
  id: string;
  input_text: string;
  detected_language: string;
  risk_score: number;
  risk_level: string;
  created_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { token } = useAuthStore();
  const { language } = useLangStore();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [stats, setStats] = useState({ total: 0, high: 0, medium: 0, low: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { router.push("/login"); return; }
    loadData();
  }, [token]);

  const loadData = async () => {
    try {
      const { data } = await analyze.history(1, 50);
      const items = data.items || [];
      setHistory(items);
      setStats({
        total: data.total,
        high: items.filter((i: HistoryItem) => i.risk_level === "high").length,
        medium: items.filter((i: HistoryItem) => i.risk_level === "medium").length,
        low: items.filter((i: HistoryItem) => i.risk_level === "low").length,
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const riskColors: Record<string, string> = {
    high: "bg-red-100 text-red-700",
    medium: "bg-yellow-100 text-yellow-700",
    low: "bg-green-100 text-green-700",
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gray-50 p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">{t("dashboard.title", language)}</h1>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: t("dashboard.totalAnalyses", language), value: stats.total, color: "border-gray-300" },
            { label: t("dashboard.highRisk", language), value: stats.high, color: "border-red-500" },
            { label: t("dashboard.mediumRisk", language), value: stats.medium, color: "border-yellow-500" },
            { label: t("dashboard.lowRisk", language), value: stats.low, color: "border-green-500" },
          ].map((s) => (
            <div key={s.label} className={`bg-white rounded-xl shadow-sm p-5 border-l-4 ${s.color}`}>
              <p className="text-sm text-gray-500">{s.label}</p>
              <p className="text-3xl font-bold mt-1">{loading ? "..." : s.value}</p>
            </div>
          ))}
        </div>

        {/* History */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{t("dashboard.recentAnalyses", language)}</h2>
            <Link href="/analyze" className="text-sm text-blue-600 hover:underline">
              + New Analysis
            </Link>
          </div>

          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading...</div>
          ) : history.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-400 mb-4">No analyses yet.</p>
              <Link href="/analyze" className="text-blue-600 hover:underline">
                Start by analyzing a message →
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-500 border-b">
                    <th className="pb-2 pr-4">Message</th>
                    <th className="pb-2 pr-4">Lang</th>
                    <th className="pb-2 pr-4">Risk</th>
                    <th className="pb-2 pr-4">Score</th>
                    <th className="pb-2">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((item) => (
                    <tr key={item.id} className="border-b last:border-0 hover:bg-gray-50">
                      <td className="py-3 pr-4 max-w-xs truncate">
                        <Link href={`/analyze`} className="hover:text-blue-600">
                          {item.input_text.slice(0, 80)}{item.input_text.length > 80 ? "..." : ""}
                        </Link>
                      </td>
                      <td className="py-3 pr-4">
                        <span className="bg-gray-100 px-2 py-0.5 rounded text-xs uppercase">
                          {item.detected_language}
                        </span>
                      </td>
                      <td className="py-3 pr-4">
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskColors[item.risk_level] || ""}`}>
                          {item.risk_level}
                        </span>
                      </td>
                      <td className="py-3 pr-4 font-mono">{item.risk_score}</td>
                      <td className="py-3 text-gray-400 text-xs">
                        {new Date(item.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
