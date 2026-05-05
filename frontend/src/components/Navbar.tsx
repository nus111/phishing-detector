"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useAuthStore, useLangStore } from "@/lib/store";
import { t } from "@/lib/i18n";

const LANGUAGES = [
  { code: "en", label: "English", flag: "🇬🇧" },
  { code: "zh", label: "中文", flag: "🇨🇳" },
  { code: "ms", label: "Melayu", flag: "🇲🇾" },
  { code: "ta", label: "தமிழ்", flag: "🇮🇳" },
];

const NAV_ITEMS = [
  { href: "/analyze", icon: "🔍", labelKey: "common.analyze" },
  { href: "/dashboard", icon: "📊", labelKey: "common.dashboard" },
  { href: "/education", icon: "📚", labelKey: "common.education" },
];

export default function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();
  const { language, setLanguage } = useLangStore();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-bold text-lg">
            🛡️ <span className="hidden sm:inline">Phishing Detector</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                  pathname === item.href
                    ? "bg-blue-50 text-blue-700"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                {item.icon} {t(item.labelKey, language)}
              </Link>
            ))}
            {user?.role === "admin" && (
              <Link
                href="/admin"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                  pathname === "/admin"
                    ? "bg-blue-50 text-blue-700"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                ⚙️ {t("common.admin", language)}
              </Link>
            )}
          </div>

          {/* Right side: language + auth */}
          <div className="flex items-center gap-3">
            {/* Language switcher */}
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="text-sm border rounded-lg px-2 py-1.5 bg-white"
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code}>
                  {l.flag} {l.label}
                </option>
              ))}
            </select>

            {/* Auth */}
            {user ? (
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600 hidden sm:inline">
                  {user.name}
                </span>
                <button
                  onClick={logout}
                  className="text-sm text-red-600 hover:text-red-700 px-2 py-1"
                >
                  {t("common.signOut", language)}
                </button>
              </div>
            ) : (
              <div className="flex gap-2">
                <Link
                  href="/login"
                  className="text-sm text-blue-600 hover:text-blue-700 px-3 py-1.5"
                >
                  {t("common.signIn", language)}
                </Link>
                <Link
                  href="/register"
                  className="text-sm bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700"
                >
                  {t("common.signUp", language)}
                </Link>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              className="md:hidden p-2"
              onClick={() => setMobileOpen(!mobileOpen)}
            >
              {mobileOpen ? "✕" : "☰"}
            </button>
          </div>
        </div>

        {/* Mobile Nav */}
        {mobileOpen && (
          <div className="md:hidden pb-4 space-y-1">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className={`block px-3 py-2 rounded-lg text-sm ${
                  pathname === item.href
                    ? "bg-blue-50 text-blue-700"
                    : "text-gray-600"
                }`}
              >
                {item.icon} {t(item.labelKey, language)}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
