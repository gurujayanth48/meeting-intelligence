import React, { useState, useEffect } from 'react';
import { getMeetingDetails } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Analytics = ({ meetingId }) => {
  const [meetingData, setMeetingData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (meetingId) {
      loadMeetingData();
    }
  }, [meetingId]);

  const loadMeetingData = async () => {
    try {
      setLoading(true);
      const data = await getMeetingDetails(meetingId);
      setMeetingData(data);
    } catch (error) {
      console.error('Failed to load meeting data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading analytics...</div>;
  }

  if (!meetingData) {
    return <div className="text-center py-8">No data available</div>;
  }

  // Prepare data for charts
  const actionItemsByAssignee = meetingData.action_items?.reduce((acc, item) => {
    acc[item.assignee] = (acc[item.assignee] || 0) + 1;
    return acc;
  }, {}) || {};

  const actionItemsData = Object.entries(actionItemsByAssignee).map(([name, count]) => ({
    name,
    count
  }));

  const topicsData = (meetingData.topics || []).map((topic, index) => ({
    name: topic,
    count: Math.floor(Math.random() * 10) + 1 // Mock data
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Action Items by Assignee</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={actionItemsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Meeting Topics Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={topicsData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {topicsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Meeting Summary</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">Key Decisions</h4>
              <ul className="space-y-2">
                {(meetingData.decisions || []).slice(0, 3).map((decision, index) => (
                  <li key={index} className="text-sm text-gray-600">
                    <span className="font-medium">{decision.decision}</span>
                    <br />
                    <span className="text-xs">Made by: {decision.made_by}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">Participants</h4>
              <ul className="space-y-2">
                {(meetingData.participants || []).map((participant, index) => (
                  <li key={index} className="text-sm text-gray-600">
                    <span className="font-medium">{participant.name}</span>
                    <br />
                    <span className="text-xs">{participant.role}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">Topics Discussed</h4>
              <ul className="space-y-1">
                {(meetingData.topics || []).map((topic, index) => (
                  <li key={index} className="text-sm text-gray-600">
                    • {topic}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;