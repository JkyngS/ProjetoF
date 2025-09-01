import React from 'react';

import { Surgery } from '../types/surgery';

interface ProgressBarProps {
  duration?: string;
  status: Surgery['status_agenda'];
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ duration, status }) => {
  const getProgressColor = () => {
    switch (status) {
      case 'in_progress':
        return 'bg-blue-500';
      case 'completed':
        return 'bg-green-500';
      case 'called':
        return 'bg-green-500';
      default:
        return 'bg-orange-500';
    }
  };

  const getProgressPercentage = () => {
    switch (status) {
      case 'in_progress':
        return 45;
      case 'completed':
        return 100;
      case 'called':
        return 15;
      default:
        return 5;
    }
  };

  return (
    <div className="mt-3">
      <div className="flex justify-between items-center text-xs text-gray-600 mb-1">
        <span>DURAÇÃO: {duration}</span>
        <span>DESTINO:</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className={`h-2 rounded-full transition-all duration-300 ${getProgressColor()}`}
          style={{ width: `${getProgressPercentage()}%` }}
        />
      </div>
    </div>
  );
};