export interface Surgery {
  nr_sequencia: string;
  sala: string;
  horario: string;
  codigo_procedimento_principal: string;
  paciente: string;
  medico: string;
  procedimento: string;
  status_agenda: 'preparing' | 'in_progress' | 'completed' | 'called';
  duracao?: string;
  progress?: number;
}

export interface SurgeryRoom {
  id: string;
  name: string;
  surgeries: Surgery[];
}