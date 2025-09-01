import React from 'react';
import { SurgeryRoom } from '../types/surgery';
import { SurgeryCard } from './SurgeryCard';

interface RoomColumnProps {
  room: SurgeryRoom;
}

export const RoomColumn: React.FC<RoomColumnProps> = ({ room }) => {
  return (
    <div className="flex flex-col gap-4">
      {room.surgeries.map((surgery) => (
        <SurgeryCard key={surgery.id} surgery={surgery} />
      ))}
    </div>
  );
};