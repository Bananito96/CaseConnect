// frontend/src/components/CaseSearch.jsx
import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { searchCases } from '../lib/api';
import CaseCard from './CaseCard';

const DateRangePicker = ({ onDateChange, dateRange }) => {
  return (
    <div className="flex gap-2 items-center">
      <input
        type="date"
        className="p-2 border rounded-md text-sm"
        value={dateRange.from}
        onChange={(e) => onDateChange('from', e.target.value)}
      />
      <span>to</span>
      <input
        type="date"
        className="p-2 border rounded-md text-sm"
        value={dateRange.to}
        onChange={(e) => onDateChange('to', e.target.value)}
      />
    </div>
  );
};

export default function CaseSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedJurisdictions, setSelectedJurisdictions] = useState([]);
  const [dateRange, setDateRange] = useState({
    from: '',
    to: '',
  });
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Update the jurisdictions to match those available in your backend
  const jurisdictions = [
    'CODICES_Hackathon_Art6_ENG',
    'hudoc',
    'cjue',
    'codices',
    'CODICES-dataset-Hackathton_2024_11_15',
  ];

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    try {
      const response = await searchCases({
        query: searchQuery,
        jurisdictions: selectedJurisdictions,
        dateRange: dateRange,
      });
      console.log('Search response:', response);

      if (response.results && Array.isArray(response.results)) {
        setResults(response.results);
      } else {
        console.error('No results in response:', response);
        setResults([]);
      }
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleDateChange = (type, value) => {
    setDateRange((prev) => ({
      ...prev,
      [type]: value,
    }));
  };

  return (
    <div className="min-h-screen bg-pink-50">
      <div className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <img
              src="/images/logo.png"
              alt="Logo"
              className="w-10 h-10 rounded"
            />
            <h1 className="text-2xl font-semibold text-gray-800">CaseConnect</h1>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white p-6 rounded-lg shadow-sm mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search for similar cases..."
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-200"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>

          <div className="mt-4 flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Jurisdictions
              </label>
              <div className="flex flex-wrap gap-2">
                {jurisdictions.map((jurisdiction) => (
                  <button
                    key={jurisdiction}
                    className={`px-3 py-1 rounded-full text-sm ${
                      selectedJurisdictions.includes(jurisdiction)
                        ? 'bg-pink-200 text-pink-800'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                    onClick={() => {
                      setSelectedJurisdictions((prev) =>
                        prev.includes(jurisdiction)
                          ? prev.filter((j) => j !== jurisdiction)
                          : [...prev, jurisdiction]
                      );
                    }}
                  >
                    {jurisdiction}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date Range
              </label>
              <DateRangePicker onDateChange={handleDateChange} dateRange={dateRange} />
            </div>
          </div>

          <button
            onClick={handleSearch}
            className="mt-4 px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600"
          >
            Search
          </button>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Most Relevant Cases</h2>
          {isLoading ? (
            <p>Loading...</p>
          ) : results.length > 0 ? (
            <div className="space-y-4">
              {results.map((caseData, index) => (
                <CaseCard key={index} caseData={caseData} />
              ))}
            </div>
          ) : (
            <p>No results found.</p>
          )}
        </div>
      </div>
    </div>
  );
}
