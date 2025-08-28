import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getMeetingStatus = async (meetingId) => {
  const response = await api.get(`/meetings/${meetingId}/status`);
  return response.data;
};

export const getMeetingDetails = async (meetingId) => {
  const response = await api.get(`/meetings/${meetingId}`);
  return response.data;
};

export const listMeetings = async (skip = 0, limit = 100) => {
  const response = await api.get(`/meetings?skip=${skip}&limit=${limit}`);
  return response.data;
};

export const searchMeetings = async (query, meetingId = null) => {
  const response = await api.post('/search', { query, meeting_id: meetingId });
  return response.data;
};