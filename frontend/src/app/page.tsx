import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold mb-4">
          🛡️ Phishing Detector
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          AI-powered multilingual phishing and fraud detection system.
          Protect yourself from scams in any language.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/analyze"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            Analyze Message
          </Link>
          <Link
            href="/login"
            className="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition"
          >
            Sign In
          </Link>
        </div>
      </div>
    </main>
  );
}
