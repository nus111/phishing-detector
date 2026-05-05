import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col">
      {/* Hero */}
      <section className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="max-w-3xl text-center">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            🛡️ Phishing Detector
          </h1>
          <p className="text-xl text-gray-600 mb-4">
            AI-powered multilingual phishing and fraud detection system.
          </p>
          <p className="text-gray-500 mb-8">
            Protecting vulnerable populations from scams in{" "}
            <strong>English</strong>, <strong>中文</strong>,{" "}
            <strong>Bahasa Melayu</strong>, and <strong>தமிழ்</strong>.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link
              href="/analyze"
              className="bg-blue-600 text-white px-8 py-3 rounded-xl text-lg font-medium hover:bg-blue-700 transition shadow-lg shadow-blue-200"
            >
              🔍 Analyze a Message
            </Link>
            <Link
              href="/register"
              className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-xl text-lg font-medium hover:bg-blue-50 transition"
            >
              Create Account
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white py-16 px-4">
        <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: "🌍",
              title: "Multilingual",
              desc: "Supports English, Chinese, Malay, and Tamil with automatic language detection.",
            },
            {
              icon: "🤖",
              title: "AI-Powered",
              desc: "Deep learning model (XLM-RoBERTa) trained on real phishing data for accurate detection.",
            },
            {
              icon: "📚",
              title: "Educational",
              desc: "Built-in security education with tips, articles, and quizzes to improve awareness.",
            },
          ].map((f) => (
            <div key={f.title} className="text-center p-6">
              <span className="text-4xl">{f.icon}</span>
              <h3 className="text-xl font-semibold mt-4 mb-2">{f.title}</h3>
              <p className="text-gray-600">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
