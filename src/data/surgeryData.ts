import { Surgery, SurgeryRoom } from '../types/surgery';

export const surgeryData: SurgeryRoom[] = [
  {
    id: '1',
    name: 'SALA5',
    surgeries: [
      {
        id: '1',
        room: 'SALA5',
        time: '07:00',
        code: 'AMVB 47 F',
        patient: 'Camila Cuidado Santos',
        doctor: 'Dr. João Silva',
        procedure: 'Cirurgia geral - Apendicectomia por via laparoscópica com ou sem tratamento',
        status: 'preparing',
        duration: '2h 30min'
      }
    ]
  },
  {
    id: '2',
    name: 'SALA4',
    surgeries: [
      {
        id: '2',
        room: 'SALA4',
        time: '08:00',
        code: 'EMS 72 F',
        patient: 'Inácio Faco Ventura Vieira',
        doctor: 'Dr. Maria Santos',
        procedure: 'Cirurgia reconstrutiva - Transplante orofacial',
        status: 'preparing',
        duration: '4h 15min'
      }
    ]
  },
  {
    id: '3',
    name: 'SALA2',
    surgeries: [
      {
        id: '3',
        room: 'SALA2',
        time: '10:00',
        code: 'USO 15 F',
        patient: 'Marcelli Tainah Marcante',
        doctor: 'Dr. Carlos Mendes',
        procedure: 'Cirurgia de coluna - Artrodese',
        status: 'preparing',
        duration: '3h 45min'
      }
    ]
  },
  {
    id: '4',
    name: 'SALA1',
    surgeries: [
      {
        id: '4',
        room: 'SALA1',
        time: '10:00',
        code: 'LLP 30 F',
        patient: 'Giovanna Bernardes De Lima Mizeira',
        doctor: 'Dr. Ana Costa',
        procedure: 'Cirurgia cardiovascular - Correção de valvopatia com recolocação percutânea (endoscópica)',
        status: 'called',
        duration: '2h 15min'
      }
    ]
  },
  {
    id: '5',
    name: 'SALA6',
    surgeries: [
      {
        id: '5',
        room: 'SALA6',
        time: '10:00',
        code: 'GGM 25 M',
        patient: 'Bruno Azevedo Veronesi',
        doctor: 'Dr. Roberto Lima',
        procedure: 'Microcirurgia - Neurocirurgia',
        status: 'called',
        duration: '5h 30min'
      },
      {
        id: '6',
        room: 'SALA6',
        time: '12:00',
        code: 'FMMA 38 M',
        patient: 'Marcelli Tainah Marcante',
        doctor: 'Dr. Patricia Rocha',
        procedure: 'Cirurgia de coluna - Artrodese',
        status: 'preparing',
        duration: '2h 30min'
      }
    ]
  },
  {
    id: '6',
    name: 'SALA3',
    surgeries: [
      {
        id: '7',
        room: 'SALA3',
        time: '13:00',
        code: 'ALVR 44 F',
        patient: 'Eduardo Mulinari Darold',
        doctor: 'Dr. Fernando Alves',
        procedure: 'Transplante de órgãos (coração)',
        status: 'preparing',
        duration: '6h 00min'
      }
    ]
  }
];