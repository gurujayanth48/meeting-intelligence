import React, { useState, useEffect } from 'react';
import { getMeetingDetails } from '../services/api';

const ActionItems = ({ meetingId }) => {
  const [actionItems, setActionItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (meetingId) {
      loadActionItems();
    }
  }, [meetingId]);

  const loadActionItems = async () => {
    try {
      setLoading(true);
      const data = await getMeetingDetails(meetingId);
      setActionItems(data.action_items || []);
    } catch (error) {
      console.error('Failed to load action items:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No deadline';
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return <div className="text-center py-8">Loading action items...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Action Items</h3>
      </div>
      <div className="p-6">
        {actionItems.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No action items found for this meeting.</p>
        ) : (
          <div className="space-y-4">
            {actionItems.map((item, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium text-gray-900">{item.task}</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      <span className="font-medium">Assignee:</span> {item.assignee}
                    </p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    new Date(item.deadline) < new Date() 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    Due: {formatDate(item.deadline)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ActionItems;