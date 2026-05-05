'use client';

export default function EducationPage() {
  // TODO: Fetch from GET /api/v1/education
  const tips = [
    {
      id: 1,
      title: 'How to spot a phishing email',
      type: 'tip',
      language: 'en',
    },
    {
      id: 2,
      title: 'Visa scam warning signs',
      type: 'article',
      language: 'en',
    },
    {
      id: 3,
      title: 'Quiz: Can you identify the scam?',
      type: 'quiz',
      language: 'en',
    },
  ];

  const typeIcons: Record<string, string> = {
    tip: '💡',
    article: '📄',
    quiz: '📋',
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">📚 Cybersecurity Education</h1>
        <p className="text-gray-600 mb-6">
          Learn how to identify and protect yourself from phishing and fraud.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tips.map((tip) => (
            <div
              key={tip.id}
              className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition cursor-pointer"
            >
              <span className="text-3xl">{typeIcons[tip.type] || '📄'}</span>
              <h3 className="font-semibold mt-3 mb-1">{tip.title}</h3>
              <span className="text-xs uppercase text-gray-400 bg-gray-100 px-2 py-1 rounded">
                {tip.type}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
