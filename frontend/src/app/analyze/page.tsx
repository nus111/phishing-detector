'use client';

import { useState } from 'react';

interface AnalysisResult {
  id: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high';
  detected_language: string;
  detected_patterns: {
    type: string;
    confidence: number;
    evidence: string;
    explanation: string;
  }[];
  recommendation: string;
}

export default function AnalyzePage() {
  const [text, setText] = useState('');
  const [language, setLanguage] = useState('auto');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      // TODO: Call POST /api/v1/analyze
      // Mock result for now
      await new Promise((r) => setTimeout(r, 1500));
      setResult({
        id: 'mock-001',
        risk_score: 85,
        risk_level: 'high',
        detected_language: 'zh',
        detected_patterns: [
          {
            type: 'Visa Threat',
            confidence: 0.92,
            evidence: '签证已被取消',
            explanation: 'Uses visa cancellation threat to create panic',
          },
          {
            type: 'Urgency Pressure',
            confidence: 0.87,
            evidence: '立即点击',
            explanation: 'Uses urgency language to force quick action',
          },
        ],
        recommendation: 'This message has a high probability of being a phishing attempt. Do not click any links or provide personal information.',
      });
    } finally {
      setLoading(false);
    }
  };

  const riskColors = {
    low: 'bg-green-100 text-green-800 border-green-300',
    medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    high: 'bg-red-100 text-red-800 border-red-300',
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">🔍 Message Analyzer</h1>

        {/* Input Area */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <label className="block text-sm font-medium mb-2">
            Paste or type a message to analyze
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full border rounded-lg px-4 py-3 h-40 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter suspicious message here..."
          />
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Language:</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="border rounded-lg px-3 py-1.5 text-sm"
              >
                <option value="auto">Auto-detect</option>
                <option value="en">English</option>
                <option value="zh">中文</option>
                <option value="ms">Bahasa Melayu</option>
                <option value="ta">தமிழ்</option>
              </select>
            </div>
            <button
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>

        {/* Result Area */}
        {result && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className={`inline-block px-4 py-2 rounded-lg border mb-4 ${riskColors[result.risk_level]}`}>
              <span className="font-bold uppercase">{result.risk_level}</span>
              <span className="ml-2">Risk — Score: {result.risk_score}/100</span>
            </div>

            <p className="text-sm text-gray-500 mb-4">
              Detected language: <strong>{result.detected_language.toUpperCase()}</strong>
            </p>

            <h3 className="font-semibold mb-2">Detected Threats:</h3>
            <ul className="space-y-2 mb-4">
              {result.detected_patterns.map((p, i) => (
                <li key={i} className="flex items-start gap-2 p-3 bg-gray-50 rounded-lg">
                  <span className="text-red-500">⚠️</span>
                  <div>
                    <p className="font-medium">{p.type} <span className="text-sm text-gray-400">({Math.round(p.confidence * 100)}%)</span></p>
                    <p className="text-sm text-gray-600">&ldquo;{p.evidence}&rdquo; — {p.explanation}</p>
                  </div>
                </li>
              ))}
            </ul>

            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold mb-1">💡 Recommendation</h3>
              <p className="text-sm text-gray-700">{result.recommendation}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
