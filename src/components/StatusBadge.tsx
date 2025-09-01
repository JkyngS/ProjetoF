import React from 'react';
import { Surgery } from '../types/surgery';

interface StatusBadgeProps {
  status: Surgery['status'];
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'preparing':
        return {
          text: 'Preparando',
          className: 'bg-orange-100 text-orange-800 border-orange-200'
        };
      case 'in_progress':
        return {
          text: 'Em Andamento',
          className: 'bg-blue-100 text-blue-800 border-blue-200'
        };
      case 'completed':
        return {
          text: 'Finalizado',
          className: 'bg-gray-100 text-gray-800 border-gray-200'
        };
      case 'called':
        return {
          text: 'Chamado',
          className: 'bg-green-100 text-green-800 border-green-200'
        };
      default:
        return {
          text: 'Indefinido',
          className: 'bg-gray-100 text-gray-800 border-gray-200'
        };
    }
  };

  const { text, className } = getStatusConfig();

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${className}`}>
      {text}
    </span>
  );
};