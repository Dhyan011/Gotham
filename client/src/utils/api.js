import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  getCase: async (id) => {
    const res = await axios.get(`${API_BASE}/cases/${id}`);
    return res.data;
  },
  getGraphNeighbors: async (personName) => {
    const res = await axios.get(`${API_BASE}/graph/neighbors`, { params: { person_name: personName } });
    return res.data;
  },
  getRiskScore: async (personName) => {
    const res = await axios.get(`${API_BASE}/risk/score`, { params: { person_name: personName } });
    return res.data;
  },
  triggerCopilot: async (command) => {
    const res = await axios.post(`${API_BASE}/copilot/investigate`, { command });
    return res.data;
  }
};
