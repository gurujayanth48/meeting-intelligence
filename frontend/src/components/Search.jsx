import React, { useState } from 'react';
import { searchMeetings } from '../services/api';

const Search = ({ meetingId }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const data = await searchMeetings(query, meetingId);
      setResults(data.results);
    } catch (error) {
      console.error('Search failed:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Search Meeting Content</h3>
      </div>
      <div className="p-6">
        <form onSubmit={handleSearch} className="mb-6">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for keywords in meeting content..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className={`px-4 py-2 rounded-md font-medium text-white ${
                loading || !query.trim()
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>

        {results.length > 0 && (
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">
              Found {results.length} result{results.length !== 1 ? 's' : ''}
            </h4>
            {results.map((result, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <p className="text-gray-700">{result.content}</p>
                <div className="mt-2 text-xs text-gray-500">
                  <span>Relevance: {Math.round((1 - result.distance) * 100)}%</span>
                  {result.metadata.meeting_id && (
                    <span className="ml-2">Meeting ID: {result.metadata.meeting_id}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {results.length === 0 && query && !loading && (
          <div className="text-center py-8 text-gray-500">
            No results found for "{query}"
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;