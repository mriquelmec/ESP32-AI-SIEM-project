import React from 'react';

function Layout({ children }) {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 bg-white dark:bg-gray-800 border-r dark:border-gray-700">
        <div className="p-4">
          <h1 className="text-2xl font-bold text-blue-500">ESP32-SIEM</h1>
        </div>
        <nav className="mt-6">
          <a href="#" className="block px-4 py-2 text-lg font-semibold bg-gray-200 dark:bg-gray-700">
            Dashboard
          </a>
          {/* Future navigation links can go here */}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}

export default Layout;
