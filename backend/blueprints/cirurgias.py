from flask import Blueprint, request, jsonify
import cx_Oracle
import datetime
from database import get_db_connection
from .auth import verificar_token

# Blueprint para rotas de cirurgias
cirurgias_bp = Blueprint('cirurgias', __name__)

# --- Funções auxiliares ---
def tratar_codigo(tipo, codigo):
    mapeamentos = {
        "carater_cirurgia": {
            "U": "Urgência",
            "E": "Eletiva",
        },
        "status_agenda": {
            "E": "Executada",
            "A": "Aguardando",
            "CN": "Confirmada",
            "PA": "Pré-Agendado",
        }
    }
    return mapeamentos.get(tipo, {}).get(codigo, f"{tipo.capitalize()} Desconhecido")

# --- Rotas de Cirurgias ---
@cirurgias_bp.route('/cirurgias', methods=['GET'])
def listar_cirurgias():
    # Verificar o token de autenticação
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"erro": "Token de autorização não fornecido"}), 401
    
    try:
        token = auth_header.split(" ")[1]  # Remove o prefixo "Bearer "
    except IndexError:
        return jsonify({"erro": "Formato de token inválido. Use 'Bearer <token>'"}), 401
    
    # Validar o token
    resultado = verificar_token(token)
    if resultado in ['Token expirado', 'Token inválido', 'Token inválido (logout realizado)']:
        return jsonify({"erro": resultado}), 401

    # Se o token for válido, continuar com o processamento
    data = request.args.get('data')
    ie_alergia = request.args.get('ie_alergia', 'S')
    
    if not data:
        data = datetime.datetime.today().strftime('%Y-%m-%d')

    with get_db_connection() as conn:
        if conn is None:
            return jsonify({"erro": "Erro na conexão com o banco de dados"}), 500

        try:
            with conn.cursor() as cursor:
                query = """
        WITH alergias_paciente AS (
            SELECT 
                pa.cd_pessoa_fisica,
                MAX(pa.ie_nega_alergias) AS ie_nega_alergias
            FROM TASY.paciente_alergia pa
            WHERE pa.dt_liberacao IS NOT NULL
              AND pa.dt_inativacao IS NULL
              AND NVL(:ie_alergia,'S') = 'S'
            GROUP BY pa.cd_pessoa_fisica
        ),
        agentes_paciente AS (
            SELECT 
                a.cd_pessoa_alerta AS cd_pessoa_fisica,
                LISTAGG(
                    NVL(NVL(NVL(NVL(NVL(NVL(NVL(
                        a.ds_ficha_tecnica,
                        a.ds_dcb),
                        a.ds_dcb_mat),
                        a.ds_material),
                        a.ds_classe_mat),
                        a.ds_familia),
                        a.ds_medic_nao_cad),
                        a.ds_alergeno
                    ), '; '
                ) WITHIN GROUP (ORDER BY a.nr_seq_apresent) AS ds_agente
            FROM TASY.alerta_v a
            INNER JOIN TASY.parametro_medico b ON b.cd_estabelecimento = 1
            WHERE a.ie_tipo_alerta = 'A'
              AND (('T' = 'T') OR (('T' <> 'T' AND a.ie_alerta = 'S')))
              AND ((b.ie_liberar_hist_saude = 'N') OR (a.dt_liberacao IS NOT NULL))
              AND ((a.ie_tipo_alerta <> 'A') OR (b.ie_exibir_nega_alergia = 'S' OR EXISTS (
                    SELECT 1 FROM TASY.paciente_alergia x
                    WHERE x.nr_sequencia = a.nr_seq_alerta
                      AND NVL(x.ie_nega_alergias, 'N') = 'N'
                )))
              AND ((a.ie_tipo_alerta <> 'I') OR (NVL(a.nr_atendimento, 0) = 0 OR NVL(378241, 0) = 0 OR a.nr_atendimento = 378241))
              AND (('N' = 'N') OR ('N' = 'S' AND a.nr_seq_nivel IS NOT NULL))
            GROUP BY a.cd_pessoa_alerta
        )
        SELECT DISTINCT
            ap.cd_pessoa_fisica,
            NVL(a.nm_paciente, 'Sem nome') AS nm_paciente,
            NVL(a.qt_idade_paciente, 0) AS qt_idade_paciente,
            NVL(a.ds_convenio, 'Sem convênio') AS ds_convenio,
            TO_CHAR(a.hr_inicio, 'DD/MM/YYYY HH24:MI:SS') AS hr_inicio,
            NVL(p.ds_exame_curto, a.ds_procedimento) AS ds_procedimento,
            NVL(a.nm_medico_cirurgiao, 'Sem médico') AS nm_medico_cirurgiao,
            NVL(a.ds_sala, 'Sem sala') AS ds_sala,
            NVL(ap.ds_observacao, 'Sem observação') AS ds_observacao,
            p.nr_seq_classif AS tipo_procedimento,
            a.cd_procedimento AS codigo_procedimento_principal,
            (
                SELECT LISTAGG(b.cd_procedimento || ' - ' || TASY.obter_descricao_procedimento(b.cd_procedimento, b.ie_origem_proced), '; ')
                WITHIN GROUP (ORDER BY b.cd_procedimento)
                FROM TASY.AGENDA_PACIENTE_PROC b
                WHERE b.nr_sequencia = a.nr_sequencia_p
            ) AS procedimentos_adicionais,
            UPPER(TASY.OBTER_VALOR_DOMINIO(1372, ap.ie_lado)) AS lado,
            UPPER(NVL(pf.ie_sexo, 'Sem informação')) AS sexo_paciente,
            ap.IE_CARATER_CIRURGIA,
            ap.IE_STATUS_AGENDA,
            ap.nr_sequencia,
            NVL(alergia.ie_nega_alergias, 'N') AS ie_nega_alergias,
            CASE 
                WHEN NVL(alergia.ie_nega_alergias, 'N') = 'N' THEN (
                    SELECT LISTAGG(
                        NVL(NVL(NVL(TASY.obter_desc_dcb(pa.nr_seq_dcb),
                            SUBSTR(TASY.obter_desc_material(pa.cd_material),1,254)),
                            SUBSTR(TASY.obter_desc_classe_mat(pa.cd_classe_mat),1,255)),
                            pa.ds_medic_nao_cad), '; '
                    ) WITHIN GROUP (ORDER BY pa.dt_registro)
                    FROM TASY.paciente_alergia pa
                    WHERE pa.cd_pessoa_fisica = ap.cd_pessoa_fisica
                      AND pa.dt_liberacao IS NOT NULL
                      AND pa.dt_inativacao IS NULL
                      AND NVL(:ie_alergia,'S') = 'S'
                )
                ELSE NULL
            END AS ds_principio,
            CASE 
                WHEN NVL(alergia.ie_nega_alergias, 'N') = 'N' THEN agente.ds_agente
                ELSE NULL
            END AS ds_agente
        FROM TASY.hmsl_agenda_paciente_v a
        LEFT JOIN TASY.agenda_paciente ap ON a.nr_sequencia_p = ap.nr_sequencia
        LEFT JOIN TASY.proc_interno p ON ap.nr_seq_proc_interno = p.nr_sequencia
        LEFT JOIN TASY.pessoa_fisica pf ON ap.cd_pessoa_fisica = pf.cd_pessoa_fisica
        LEFT JOIN alergias_paciente alergia ON alergia.cd_pessoa_fisica = ap.cd_pessoa_fisica
        LEFT JOIN agentes_paciente agente ON agente.cd_pessoa_fisica = ap.cd_pessoa_fisica
        WHERE a.dt_agenda = TO_DATE(:data, 'YYYY-MM-DD')
          AND a.ie_status_agenda NOT IN ('L', 'B', 'C')
        ORDER BY TO_CHAR(a.hr_inicio, 'DD/MM/YYYY HH24:MI:SS')
        """
        
                cursor.execute(query, {'data': data, 'ie_alergia': ie_alergia})

                # Obter a descrição das colunas para mapeamento correto
                columns = [col[0].lower() for col in cursor.description]

                procedimentos = []
                for row in cursor.fetchall():
                    # Criar dicionário com os nomes das colunas como chaves
                    row_dict = dict(zip(columns, row))

                    # Tipo de procedimento
                    if row_dict['tipo_procedimento'] == 96:
                        tipo_procedimento = "Cirúrgico"
                    elif row_dict['tipo_procedimento'] == 98:
                        tipo_procedimento = "Pequenos Procedimentos"
                    else:
                        tipo_procedimento = "Outro"

                    # Estágio de autorização
                    estagio_autorizacao = "Particular" if row_dict['ds_convenio'] == "Particular" else "Não verificado"

                    procedimentos.append({
                        "prontuario": row_dict['cd_pessoa_fisica'],
                        "paciente": row_dict['nm_paciente'] if row_dict['nm_paciente'] != " " else "Sem nome",
                        "idade": row_dict['qt_idade_paciente'] if row_dict['qt_idade_paciente'] is not None else 0,
                        "convenio": row_dict['ds_convenio'] if row_dict['ds_convenio'] != " " else "Sem convênio",
                        "horario": row_dict['hr_inicio'],
                        "procedimento": row_dict['ds_procedimento'] if row_dict['ds_procedimento'] != " " else "Sem procedimento",
                        "medico": row_dict['nm_medico_cirurgiao'] if row_dict['nm_medico_cirurgiao'] != " " else "Sem médico",
                        "sala": row_dict['ds_sala'] if row_dict['ds_sala'] != " " else "Sem sala",
                        "observacao": row_dict['ds_observacao'] if row_dict['ds_observacao'] != " " else "Sem observação",
                        "tipo_procedimento": tipo_procedimento,
                        "codigo_procedimento_principal": row_dict['codigo_procedimento_principal'],
                        "procedimentos_adicionais": row_dict['procedimentos_adicionais'] if row_dict['procedimentos_adicionais'] is not None else "Sem procedimentos adicionais",
                        "lado": row_dict['lado'],
                        "sexo_paciente": row_dict['sexo_paciente'],
                        "carater_cirurgia": tratar_codigo("carater_cirurgia", row_dict['ie_carater_cirurgia']),
                        "status_agenda": tratar_codigo("status_agenda", row_dict['ie_status_agenda']),
                        "estagio_autorizacao": estagio_autorizacao,
                        "alergias": {
                            "nega_alergias": row_dict['ie_nega_alergias'],
                            "principio_ativo": row_dict['ds_principio'],
                            "agente_alergenico": row_dict['ds_agente']
                        },
                        "nr_sequencia": row_dict['nr_sequencia']
                    })

                return jsonify(procedimentos)
        except cx_Oracle.DatabaseError as e:
            return jsonify({"erro": "Erro ao acessar o banco de dados", "detalhes": str(e)}), 500


