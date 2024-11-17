// frontend/src/lib/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

export async function searchCases({ query, jurisdictions, dateRange = {}, topK = 5 }) {
  try {
    console.log('searchCases params:', { query, jurisdictions, dateRange, topK });

    // Construct the request body
    const requestBody = {
      query,
      top_k: topK,
    };

    // Include jurisdictions only if they are specified
    if (jurisdictions && jurisdictions.length > 0) {
      requestBody.jurisdictions = jurisdictions;
    }

    // Include date_range only if both dates are specified
    if (dateRange.from && dateRange.to) {
      requestBody.date_range = dateRange;
    }

    const response = await fetch(`${API_BASE_URL}/api/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Search request failed:', response.status, errorText);
      throw new Error(`Search request failed: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('searchCases response data:', data);
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
