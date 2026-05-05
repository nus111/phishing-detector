'use client';

export default function AdminPage() {
  // TODO: Fetch from GET /api/v1/admin/dashboard
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">⚙️ Admin Dashboard</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Threat Overview */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Threat Trends</h2>
            <div className="h-64 flex items-center justify-center text-gray-400">
              {/* TODO: Recharts line chart */}
              <p>Chart placeholder — threat trends over time</p>
            </div>
          </div>

          {/* Language Distribution */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Language Distribution</h2>
            <div className="h-64 flex items-center justify-center text-gray-400">
              {/* TODO: Recharts pie chart */}
              <p>Chart placeholder — analysis by language</p>
            </div>
          </div>

          {/* Recent Feedback */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">User Feedback</h2>
            <p className="text-gray-400 text-center py-8">
              No feedback yet.
            </p>
          </div>

          {/* Model Status */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Model Status</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Current Version</span>
                <span className="font-mono">v1.0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Status</span>
                <span className="text-green-600 font-medium">Active</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Last Retrained</span>
                <span className="text-gray-400">—</span>
              </div>
              <button className="w-full mt-4 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
                Trigger Retrain
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
