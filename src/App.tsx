import React from 'react';
import { Header } from './components/Header';
import { StatsOverview } from './components/StatsOverview';
import { RoomColumn } from './components/RoomColumn';
import { surgeryData } from './data/surgeryData';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-6 py-6">
        <StatsOverview />
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {surgeryData.map((room) => (
            <div key={room.id} className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">{room.name}</h2>
                <span className="text-sm text-gray-500">{room.surgeries.length} procedimento(s)</span>
              </div>
              <RoomColumn room={room} />
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;