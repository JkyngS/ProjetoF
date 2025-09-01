import { SurgeryRoom } from '../types/surgery';

export const surgeryData: SurgeryRoom[] = [
  {
    id: '1',
    name: 'SALA5',
      surgeries: [
        {
          nr_sequencia: '1',
          sala: 'SALA5',
          horario: '07:00',
          codigo_procedimento_principal: 'AMVB 47 F',
          paciente: 'Camila Cuidado Santos',
          medico: 'Dr. João Silva',
          procedimento: 'Cirurgia geral - Apendicectomia por via laparoscópica com ou sem tratamento',
          status_agenda: 'preparing',
          duracao: '2h 30min'
        }
      ]
    },
    {
      id: '2',
      name: 'SALA4',
      surgeries: [
        {
          nr_sequencia: '2',
          sala: 'SALA4',
          horario: '08:00',
          codigo_procedimento_principal: 'EMS 72 F',
          paciente: 'Inácio Faco Ventura Vieira',
          medico: 'Dr. Maria Santos',
          procedimento: 'Cirurgia reconstrutiva - Transplante orofacial',
          status_agenda: 'preparing',
          duracao: '4h 15min'
        }
      ]
    },
    {
      id: '3',
      name: 'SALA2',
      surgeries: [
        {
          nr_sequencia: '3',
          sala: 'SALA2',
          horario: '10:00',
          codigo_procedimento_principal: 'USO 15 F',
          paciente: 'Marcelli Tainah Marcante',
          medico: 'Dr. Carlos Mendes',
          procedimento: 'Cirurgia de coluna - Artrodese',
          status_agenda: 'preparing',
          duracao: '3h 45min'
        }
      ]
    },
    {
      id: '4',
      name: 'SALA1',
      surgeries: [
        {
          nr_sequencia: '4',
          sala: 'SALA1',
          horario: '10:00',
          codigo_procedimento_principal: 'LLP 30 F',
          paciente: 'Giovanna Bernardes De Lima Mizeira',
          medico: 'Dr. Ana Costa',
          procedimento: 'Cirurgia cardiovascular - Correção de valvopatia com recolocação percutânea (endoscópica)',
          status_agenda: 'called',
          duracao: '2h 15min'
        }
      ]
    },
    {
      id: '5',
      name: 'SALA6',
      surgeries: [
        {
          nr_sequencia: '5',
          sala: 'SALA6',
          horario: '10:00',
          codigo_procedimento_principal: 'GGM 25 M',
          paciente: 'Bruno Azevedo Veronesi',
          medico: 'Dr. Roberto Lima',
          procedimento: 'Microcirurgia - Neurocirurgia',
          status_agenda: 'called',
          duracao: '5h 30min'
        },
        {
          nr_sequencia: '6',
          sala: 'SALA6',
          horario: '12:00',
          codigo_procedimento_principal: 'FMMA 38 M',
          paciente: 'Marcelli Tainah Marcante',
          medico: 'Dr. Patricia Rocha',
          procedimento: 'Cirurgia de coluna - Artrodese',
          status_agenda: 'preparing',
          duracao: '2h 30min'
        }
      ]
    },
    {
      id: '6',
      name: 'SALA3',
      surgeries: [
        {
          nr_sequencia: '7',
          sala: 'SALA3',
          horario: '13:00',
          codigo_procedimento_principal: 'ALVR 44 F',
          paciente: 'Eduardo Mulinari Darold',
          medico: 'Dr. Fernando Alves',
          procedimento: 'Transplante de órgãos (coração)',
          status_agenda: 'preparing',
          duracao: '6h 00min'
        }
      ]
    }
  ];