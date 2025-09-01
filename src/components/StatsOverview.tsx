import React from 'react';
import { Activity, Clock, CheckCircle, AlertCircle } from 'lucide-react';

export const StatsOverview: React.FC = () => {
  const stats = [
    {
      label: 'Salas Ativas',
      value: '6',
      icon: Activity,
      color: 'text-blue-600 bg-blue-100'
    },
    {
      label: 'Em Andamento',
      value: '2',
      icon: Clock,
      color: 'text-orange-600 bg-orange-100'
    },
    {
      label: 'Finalizadas',
      value: '3',
      icon: CheckCircle,
      color: 'text-green-600 bg-green-100'
    },
    {
      label: 'Preparando',
      value: '4',
      icon: AlertCircle,
      color: 'text-yellow-600 bg-yellow-100'
    }
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
            <div className={`p-2 rounded-lg ${stat.color}`}>
              <stat.icon className="w-5 h-5" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};