import React, { useState, useEffect } from 'react';
import StatCard from '../components/StatCard';
import EventsTable from '../components/EventsTable';
import { fetchLogs, fetchLogsCount, fetchAnomaliesCount, fetchReportsCount } from '../services/api';

function DashboardPage() {
  const [stats, setStats] = useState({
    logs: '--',
    anomalies: '--',
    reports: '--',
  });
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        setLoading(true);
        const [logsCount, anomaliesCount, reportsCount, eventsData] = await Promise.all([
          fetchLogsCount(),
          fetchAnomaliesCount(),
          fetchReportsCount(),
          fetchLogs(0, 10), // Fetch first 10 events for the table
        ]);
        setStats({
          logs: logsCount,
          anomalies: anomaliesCount,
          reports: reportsCount,
        });
        setEvents(eventsData);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error("Failed to load dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }

    loadDashboardData();
  }, []);


  return (
    <>
      <h2 className="text-3xl font-bold mb-6">Dashboard Overview</h2>
      
      {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert"><strong>Error:</strong> {error}</div>}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <StatCard 
          title="Total Events" 
          value={loading ? '...' : stats.logs}
          icon={<svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" /></svg>}
        />
        <StatCard 
          title="Anomalies Detected" 
          value={loading ? '...' : stats.anomalies}
          icon={<svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>}
        />
        <StatCard 
          title="Reports Generated" 
          value={loading ? '...' : stats.reports}
          icon={<svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>}
        />
      </div>

      <div>
        <h3 className="text-2xl font-bold mb-4">Recent Events</h3>
        <EventsTable events={events} loading={loading} />
      </div>
    </>
  );
}

export default DashboardPage;
