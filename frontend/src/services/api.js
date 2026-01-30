const API_BASE_URL = 'http://localhost:8000'; // Assuming the backend runs on port 8000

export async function fetchLogs(skip = 0, limit = 100) {
  const response = await fetch(`${API_BASE_URL}/logs?skip=${skip}&limit=${limit}`);
  if (!response.ok) {
    throw new Error('Failed to fetch logs');
  }
  return response.json();
}

export async function fetchLogsCount() {
  const response = await fetch(`${API_BASE_URL}/logs/count`);
  if (!response.ok) {
    throw new Error('Failed to fetch logs count');
  }
  const data = await response.json();
  return data.count;
}

export async function fetchAnomaliesCount() {
  const response = await fetch(`${API_BASE_URL}/anomalies/count`);
  if (!response.ok) {
    throw new Error('Failed to fetch anomalies count');
  }
  const data = await response.json();
  return data.count;
}

// We can add fetchReportsCount later if needed
// For now, we'll use a placeholder
export async function fetchReportsCount() {
  // This is a placeholder as the API returns a list, not a count.
  const response = await fetch(`${API_BASE_URL}/reports`);
   if (!response.ok) {
    throw new Error('Failed to fetch reports');
  }
  const data = await response.json();
  return data.length;
}
