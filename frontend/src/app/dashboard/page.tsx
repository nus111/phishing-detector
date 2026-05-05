'use client';

export default function DashboardPage() {
  // TODO: Fetch real data from GET /api/v1/analyze/history
  const stats = {
    totalAnalyses: 0,
    highRiskCount: 0,
    mediumRiskCount: 0,
    lowRiskCount: 0,
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">📊 Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow-md p-6">
            <p className="text-sm text-gray-500">Total Analyses</p>
            <p className="text-3xl font-bold">{stats.totalAnalyses}</p>
          </div>
          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-red-500">
            <p className="text-sm text-gray-500">High Risk</p>
            <p className="text-3xl font-bold text-red-600">{stats.highRiskCount}</p>
          </div>
          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-yellow-500">
            <p className="text-sm text-gray-500">Medium Risk</p>
            <p className="text-3xl font-bold text-yellow-600">{stats.mediumRiskCount}</p>
          </div>
          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
            <p className="text-sm text-gray-500">Low Risk</p>
            <p className="text-3xl font-bold text-green-600">{stats.lowRiskCount}</p>
          </div>
        </div>

        {/* Recent Analyses */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Analyses</h2>
          <p className="text-gray-400 text-center py-8">
            No analyses yet. Start by analyzing a message!
          </p>
        </div>
      </div>
    </div>
  );
}
