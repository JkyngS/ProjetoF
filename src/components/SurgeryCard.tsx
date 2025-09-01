import React from 'react';
import { Clock, User, Stethoscope, FileText, Users } from 'lucide-react';
import { Surgery } from '../types/surgery';
import { StatusBadge } from './StatusBadge';
import { ProgressBar } from './ProgressBar';
import { getInitials } from '../utils/string';

interface SurgeryCardProps {
  surgery: Surgery;
}

export const SurgeryCard: React.FC<SurgeryCardProps> = ({ surgery }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow duration-200">
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">{surgery.time}</span>
        </div>
        <div className="text-right">
          <div className="text-sm font-medium text-gray-900">{surgery.code}</div>
          <div className="text-xs text-gray-500">Sala {surgery.room}</div>
        </div>
      </div>

      <div className="mb-3">
        <StatusBadge status={surgery.status} />
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-start gap-2">
          <User className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-sm font-medium text-gray-900">{getInitials(surgery.patient)}</div>
            <div className="text-xs text-gray-500">Paciente</div>
          </div>
        </div>

        <div className="flex items-start gap-2">
          <Stethoscope className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-sm font-medium text-gray-900">{surgery.doctor}</div>
            <div className="text-xs text-gray-500">Médico Responsável</div>
          </div>
        </div>

        <div className="flex items-start gap-2">
          <FileText className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-sm text-gray-700 leading-relaxed">{surgery.procedure}</div>
            <div className="text-xs text-gray-500">Procedimento</div>
          </div>
        </div>
      </div>

      <ProgressBar duration={surgery.duration} status={surgery.status} />

      <div className="flex justify-end mt-3 gap-1">
        <button className="p-1.5 text-gray-400 hover:text-blue-600 transition-colors">
          <Users className="w-4 h-4" />
        </button>
        <button className="p-1.5 text-gray-400 hover:text-blue-600 transition-colors">
          <FileText className="w-4 h-4" />
        </button>
        <button className="p-1.5 text-gray-400 hover:text-blue-600 transition-colors">
          <Stethoscope className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
