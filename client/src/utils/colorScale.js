export const getSeverityColor = (severity) => {
  switch (severity?.toLowerCase()) {
    case 'critical':
    case 'high':
      return '#EF4444'; // danger
    case 'medium':
    case 'warning':
      return '#F59E0B'; // warning
    case 'low':
    case 'info':
      return '#3B82F6'; // accent
    default:
      return '#10B981'; // success
  }
};

export const crimeTypeColors = {
  'Theft': '#3B82F6',
  'Assault': '#EF4444',
  'Fraud': '#F59E0B',
  'Cyber': '#8B5CF6',
  'Narcotics': '#10B981',
};
