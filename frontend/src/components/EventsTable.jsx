import React from 'react';

function EventsTable({ events = [], loading }) {

  const formatTimestamp = (ts) => {
    if (!ts) return 'N/A';
    return new Date(ts * 1000).toLocaleString();
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-x-auto">
      <table className="min-w-full leading-normal">
        <thead>
          <tr>
            <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-900 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">
              ID
            </th>
            <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-900 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">
              Timestamp
            </th>
            <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-900 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">
              Raw Message
            </th>
            <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-900 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan="4" className="px-5 py-5 border-b border-gray-200 dark:border-gray-700 text-center text-gray-500">
                Loading events...
              </td>
            </tr>
          ) : events.length === 0 ? (
            <tr>
              <td colSpan="4" className="px-5 py-5 border-b border-gray-200 dark:border-gray-700 text-center text-gray-500">
                No events to display.
              </td>
            </tr>
          ) : (
            events.map((event) => (
              <tr key={event.id} className="hover:bg-gray-100 dark:hover:bg-gray-700">
                <td className="px-5 py-5 border-b border-gray-200 dark:border-gray-700 text-sm">
                  <p className="text-gray-900 dark:text-gray-200 whitespace-no-wrap">{event.id}</p>
                </td>
                <td className="px-5 py-5 border-b border-gray-200 dark:border-gray-700 text-sm">
                  <p className="text-gray-900 dark:text-gray-200 whitespace-no-wrap">{formatTimestamp(event.ts)}</p>
                </td>
                <td className="px-5 py-5 border-b border-gray-200 dark:border-gray-700 text-sm">
                  <p className="text-gray-900 dark:text-gray-200 whitespace-no-wrap">{event.raw}</p>
                </td>
                <td className="px-5 py-5 border-b border-gray-200 dark:border-gray-700 text-sm">
                  {event.anomaly > 0 ? (
                     <span className="relative inline-block px-3 py-1 font-semibold text-red-900 leading-tight">
                        <span aria-hidden className="absolute inset-0 bg-red-200 opacity-50 rounded-full"></span>
                        <span className="relative">Anomaly</span>
                    </span>
                  ) : (
                     <span className="relative inline-block px-3 py-1 font-semibold text-green-900 leading-tight">
                        <span aria-hidden className="absolute inset-0 bg-green-200 opacity-50 rounded-full"></span>
                        <span className="relative">Normal</span>
                    </span>
                  )}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default EventsTable;
