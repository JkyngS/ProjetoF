import React, { useEffect, useState } from 'react';
import { Header } from './components/Header';
import { StatsOverview } from './components/StatsOverview';
import { RoomColumn } from './components/RoomColumn';
import { SurgeryRoom } from './types/surgery';

function App() {
  const [rooms, setRooms] = useState<SurgeryRoom[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const params = new URLSearchParams();
        const dataParam = '';
        const alergiaParam = '';

        if (dataParam) params.append('data', dataParam);
        if (alergiaParam) params.append('ie_alergia', alergiaParam);

        const url = `http://${window.location.hostname}:8080/cirurgias${
          params.toString() ? `?${params.toString()}` : ''
        }`;

        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_API_TOKEN || ''}`,
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data: SurgeryRoom[] = await response.json();
        setRooms(data);
      } catch {
        setError('Falha ao carregar cirurgias');
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-6 py-6">
        <StatsOverview />
        {error && <p className="text-red-500">{error}</p>}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {rooms.map((room) => (
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
