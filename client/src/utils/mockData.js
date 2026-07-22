export const mockStats = {
  totalFirs: 12450,
  activeCases: 3201,
  arrests: 843,
  activeAlerts: 12
};

export const mockCrimeTypes = [
  { name: 'Theft', value: 400 },
  { name: 'Assault', value: 300 },
  { name: 'Fraud', value: 300 },
  { name: 'Cyber', value: 200 },
  { name: 'Narcotics', value: 100 },
];

export const mockDistricts = [
  { name: 'Bengaluru Urban', count: 1200 },
  { name: 'Mysuru', count: 800 },
  { name: 'Hubballi', count: 650 },
  { name: 'Mangaluru', count: 500 },
  { name: 'Belagavi', count: 450 },
];

export const mockRecentFirs = [
  { id: 'FIR-2023-001', type: 'Cyber', district: 'Bengaluru Urban', status: 'Active', date: '2023-10-25' },
  { id: 'FIR-2023-002', type: 'Assault', district: 'Mysuru', status: 'Closed', date: '2023-10-24' },
  { id: 'FIR-2023-003', type: 'Theft', district: 'Hubballi', status: 'Active', date: '2023-10-23' },
  { id: 'FIR-2023-004', type: 'Narcotics', district: 'Bengaluru Urban', status: 'Active', date: '2023-10-22' },
];

export const mockAlerts = [
  { id: 1, text: 'High probability of gang activity in East Bengaluru', severity: 'critical' },
  { id: 2, text: 'New cyber fraud pattern detected across 3 districts', severity: 'warning' },
];

export const mockCases = [
  { id: 'CAS-101', title: 'Downtown Syndicate', status: 'Open', risk: 'High' },
  { id: 'CAS-102', title: 'Tech Park Phishing', status: 'Investigating', risk: 'Medium' },
];

export const mockOffender = {
  name: 'Raju "The Ghost" Kumar',
  riskScore: 88,
  cases: 5,
  lastKnown: 'Shivajinagar, Bengaluru',
  tags: ['Extortion', 'Armed', 'Flight Risk']
};
