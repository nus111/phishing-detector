"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { admin } from "@/lib/api";
import { useAuthStore, useLangStore } from "@/lib/store";
import { t } from "@/lib/i18n";

interface DashboardData {
  total_analyses: number;
  total_users: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  analyses_by_language: Record<string, number>;
  analyses_by_day: { date: string; count: number }[];
  recent_threats: any[];
}

export default function AdminPage() {
  const router = useRouter();
  const { user, token } = useAuthStore();
  const { language } = useLangStore();
  const [data, setData] = useState<DashboardData | null>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [feedback, setFeedback] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<"dashboard" | "users" | "feedback">("dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) { router.push("/login"); return; }
    if (user && user.role !== "admin") { router.push("/dashboard"); return; }
    loadDashboard();
  }, [token, user]);

  const loadDashboard = async () => {
    try {
      const [dashRes, usersRes, fbRes] = await Promise.all([
        admin.dashboard(),
        admin.users(),
        admin.feedback(),
      ]);
      setData(dashRes.data);
      setUsers(usersRes.data);
      setFeedback(fbRes.data);
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError("Admin access required. Please login with an admin account.");
      } else {
        setError("Failed to load admin data.");
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-gray-400">Loading...</div>;
  if (error) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-red-50 text-red-700 p-6 rounded-xl max-w-md text-center">
        <p className="text-lg font-semibold mb-2">⚠️ Access Denied</p>
        <p>{error}</p>
        <p className="text-sm mt-2 text-gray-500">Login: admin@phishing-detector.com / admin123</p>
      </div>
    </div>
  );

  const langData = data ? Object.entries(data.analyses_by_language) : [];
  const langColors: Record<string, string> = { en: "bg-blue-500", zh: "bg-red-500", ms: "bg-green-500", ta: "bg-purple-500", unknown: "bg-gray-400" };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gray-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">⚙️ {t("common.admin", language)}</h1>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          {(["dashboard", "users", "feedback"] as const).map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === tab ? "bg-blue-600 text-white" : "bg-white text-gray-600 hover:bg-gray-100 border"
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {activeTab === "dashboard" && data && (
          <>
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
              {[
                { label: "Total Analyses", value: data.total_analyses, color: "border-gray-300" },
                { label: "Total Users", value: data.total_users, color: "border-blue-500" },
                { label: "High Risk", value: data.high_risk_count, color: "border-red-500" },
                { label: "Medium Risk", value: data.medium_risk_count, color: "border-yellow-500" },
                { label: "Low Risk", value: data.low_risk_count, color: "border-green-500" },
              ].map((s) => (
                <div key={s.label} className={`bg-white rounded-xl shadow-sm p-4 border-l-4 ${s.color}`}>
                  <p className="text-xs text-gray-500">{s.label}</p>
                  <p className="text-2xl font-bold">{s.value}</p>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Language distribution */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="font-semibold mb-4">Language Distribution</h2>
                {langData.length > 0 ? (
                  <div className="space-y-3">
                    {langData.map(([lang, count]) => {
                      const total = langData.reduce((s, [, c]) => s + c, 0);
                      const pct = total > 0 ? Math.round((count / total) * 100) : 0;
                      return (
                        <div key={lang}>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="uppercase font-medium">{lang}</span>
                            <span className="text-gray-500">{count} ({pct}%)</span>
                          </div>
                          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div className={`h-full rounded-full ${langColors[lang] || "bg-gray-400"}`} style={{ width: `${pct}%` }} />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-gray-400 text-center py-8">No data yet</p>
                )}
              </div>

              {/* Daily trend */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="font-semibold mb-4">Daily Analysis Trend (30 days)</h2>
                {data.analyses_by_day.length > 0 ? (
                  <div className="flex items-end gap-1 h-40">
                    {data.analyses_by_day.map((d) => {
                      const max = Math.max(...data.analyses_by_day.map((x) => x.count), 1);
                      const h = Math.max((d.count / max) * 100, 4);
                      return (
                        <div key={d.date} className="flex-1 flex flex-col items-center group">
                          <div className="text-xs text-gray-400 opacity-0 group-hover:opacity-100 mb-1">{d.count}</div>
                          <div className="w-full bg-blue-500 rounded-t" style={{ height: `${h}%` }} />
                          <div className="text-[8px] text-gray-400 mt-1 truncate w-full text-center">
                            {d.date.slice(5)}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-gray-400 text-center py-8">No data yet</p>
                )}
              </div>

              {/* Recent threats */}
              <div className="bg-white rounded-xl shadow-sm p-6 lg:col-span-2">
                <h2 className="font-semibold mb-4">Recent High-Risk Threats</h2>
                {data.recent_threats.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead><tr className="text-left text-gray-500 border-b">
                        <th className="pb-2">ID</th><th className="pb-2">Language</th>
                        <th className="pb-2">Score</th><th className="pb-2">Patterns</th>
                        <th className="pb-2">Date</th>
                      </tr></thead>
                      <tbody>
                        {data.recent_threats.map((t) => (
                          <tr key={t.id} className="border-b last:border-0">
                            <td className="py-2 font-mono text-xs">{t.id.slice(0, 8)}</td>
                            <td className="py-2"><span className="bg-gray-100 px-2 py-0.5 rounded text-xs uppercase">{t.language}</span></td>
                            <td className="py-2 text-red-600 font-medium">{t.risk_score}</td>
                            <td className="py-2 text-xs text-gray-500">{t.patterns?.join(", ") || "—"}</td>
                            <td className="py-2 text-xs text-gray-400">{t.created_at ? new Date(t.created_at).toLocaleDateString() : "—"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-gray-400 text-center py-8">No high-risk threats detected yet</p>
                )}
              </div>
            </div>
          </>
        )}

        {activeTab === "users" && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="font-semibold mb-4">Users ({users.length})</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="text-left text-gray-500 border-b">
                  <th className="pb-2">Name</th><th className="pb-2">Email</th>
                  <th className="pb-2">Role</th><th className="pb-2">Language</th>
                  <th className="pb-2">Analyses</th><th className="pb-2">Joined</th>
                </tr></thead>
                <tbody>
                  {users.map((u: any) => (
                    <tr key={u.id} className="border-b last:border-0">
                      <td className="py-2 font-medium">{u.name}</td>
                      <td className="py-2 text-gray-500">{u.email}</td>
                      <td className="py-2"><span className={`px-2 py-0.5 rounded text-xs ${u.role === "admin" ? "bg-purple-100 text-purple-700" : "bg-gray-100"}`}>{u.role}</span></td>
                      <td className="py-2 text-xs uppercase">{u.preferred_language}</td>
                      <td className="py-2">{u.analysis_count}</td>
                      <td className="py-2 text-xs text-gray-400">{new Date(u.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "feedback" && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="font-semibold mb-4">User Feedback ({feedback.length})</h2>
            {feedback.length > 0 ? (
              <div className="space-y-3">
                {feedback.map((f: any) => (
                  <div key={f.id} className="p-3 bg-gray-50 rounded-lg flex items-start justify-between">
                    <div>
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${f.feedback_type === "false_positive" ? "bg-yellow-100 text-yellow-700" : "bg-red-100 text-red-700"}`}>
                        {f.feedback_type}
                      </span>
                      {f.description && <p className="text-sm mt-1 text-gray-600">{f.description}</p>}
                    </div>
                    <span className="text-xs text-gray-400">{new Date(f.created_at).toLocaleDateString()}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-400 text-center py-8">No feedback yet</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
