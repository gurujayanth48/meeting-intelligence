import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getMeetingDetails, getMeetingStatus } from '../services/api';
import ActionItems from '../components/ActionItems';
import Analytics from '../components/Analytics';
import Search from '../components/Search';

const MeetingDetails = () => {
  const { meetingId } = useParams();
  const [meeting, setMeeting] = useState(null);
  const [status, setStatus] = useState('processing');
  const [activeTab, setActiveTab] = useState('actionItems');

  useEffect(() => {
    loadMeetingDetails();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, [meetingId]);

  const loadMeetingDetails = async () => {
    try {
      const data = await getMeetingDetails(meetingId);
      setMeeting(data);
    } catch (error) {
      console.error('Failed to load meeting details:', error);
    }
  };

  const checkStatus = async () => {
    try {
      const statusData = await getMeetingStatus(meetingId);
      setStatus(statusData.status);
      
      if (statusData.status === 'completed' && !meeting) {
        loadMeetingDetails();
      }
    } catch (error) {
      console.error('Failed to check status:', error);
    }
  };

  if (!meeting && status === 'processing') {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <h2 className="mt-4 text-xl font-medium text-gray-900">Processing your meeting</h2>
          <p className="mt-2 text-gray-600">
            We're analyzing your meeting recording. This may take a few minutes...
          </p>
        </div>
      </div>
    );
  }

  if (!meeting) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <h2 className="text-xl font-medium text-gray-900">Meeting not found</h2>
          <p className="mt-2 text-gray-600">
            The meeting you're looking for doesn't exist or is still processing.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{meeting.filename}</h1>
        <div className="mt-2 flex items-center">
          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
            meeting.status === 'completed' ? 'bg-green-100 text-green-800' : 
            meeting.status === 'processing' ? 'bg-yellow-100 text-yellow-800' : 
            'bg-red-100 text-red-800'
          }`}>
            {meeting.status}
          </span>
          <span className="ml-4 text-sm text-gray-500">
            Created: {new Date(meeting.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('actionItems')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'actionItems'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Action Items
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'analytics'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Analytics
          </button>
          <button
            onClick={() => setActiveTab('search')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'search'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Search
          </button>
        </nav>
      </div>

      {activeTab === 'actionItems' && <ActionItems meetingId={meetingId} />}
      {activeTab === 'analytics' && <Analytics meetingId={meetingId} />}
      {activeTab === 'search' && <Search meetingId={meetingId} />}
    </div>
  );
};

export default MeetingDetails;