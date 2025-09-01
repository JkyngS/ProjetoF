export interface Surgery {
  id: string;
  room: string;
  time: string;
  code: string;
  patient: string;
  doctor: string;
  procedure: string;
  status: 'preparing' | 'in_progress' | 'completed' | 'called';
  duration: string;
  progress?: number;
}

export interface SurgeryRoom {
  id: string;
  name: string;
  surgeries: Surgery[];
}