import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import Dashboard from '../components/Dashboard';

const Home = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const navigate = useNavigate();

  const handleUploadSuccess = (meetingId) => {
    // Navigate to meeting details page
    navigate(`/meeting/${meetingId}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AI Meeting Intelligence Platform</h1>
        <p className="mt-2 text-gray-600">
          Upload your meeting recordings and get actionable insights automatically extracted
        </p>
      </div>

      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('upload')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'upload'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Upload New Meeting
          </button>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'dashboard'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Dashboard
          </button>
        </nav>
      </div>

      {activeTab === 'upload' ? (
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      ) : (
        <Dashboard />
      )}
    </div>
  );
};

export default Home;