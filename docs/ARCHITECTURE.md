# Arquitetura

## Objetivo

O Music Reference Lab separa a análise musical em camadas para permitir execução leve na VPS e enriquecimento opcional em uma máquina com maior capacidade computacional.

## Fluxo principal

```mermaid
flowchart TD
    UI[Interface Flask] --> META[Reference Metadata]
    UI --> AUDIO[Audio Analysis]
    META --> HEUR[Heuristic Engine]
    AUDIO --> HEUR
    HEUR --> DECISION{IA complementar ativada?}
    DECISION -->|Não| RESULT[Analysis JSON]
    DECISION -->|Sim| AI[AI Engine]
    AI --> RESULT
    RESULT --> EXPORT[Exporters]
    EXPORT --> STABLE[Stable Audio]
    EXPORT --> SOUNDRAW[SOUNDRAW]
    EXPORT --> HEART[HeartMuLa]
```

## Componentes

### `app.py`

Responsável por:

- rotas Flask;
- validação básica do formulário;
- recebimento de áudio;
- orquestração da análise;
- seleção da IA complementar;
- geração e download do JSON final.

### `audio_analysis.py`

Camada de DSP baseada em Librosa e NumPy. Mede características acústicas que não dependem de um LLM.

### `reference_metadata.py`

Identifica links e consulta os metadados públicos disponíveis para referências do YouTube.

### `heuristic_engine.py`

Produz uma análise conservadora a partir dos dados disponíveis. Evita inventar precisão quando não há áudio ou IA complementar.

### `ai_engine.py`

Camada opcional de enriquecimento. Atualmente suporta:

- Ollama;
- endpoints compatíveis com OpenAI, incluindo LM Studio.

### `exporters.py`

Converte o JSON de análise em formulários específicos para cada plataforma de destino.

### `schemas.py`

Define as estruturas compacta e avançada usadas como contrato da análise.

## Princípio de separação

O LLM não precisa receber o arquivo de áudio. O desenho atual permite que a VPS faça a extração acústica e envie somente metadados e JSON para o provedor remoto de IA.

Isso reduz consumo de banda, evita enviar áudio ao modelo e permite manter a VPS sem carga de inferência.

## Dados persistentes

Os diretórios abaixo são tratados como dados de runtime:

```text
uploads/
exports/
```

Eles não devem ser versionados no Git.

Em Docker, podem ser montados como volumes para persistência fora do container.

## Limites atuais

- não existe banco de dados;
- não existe autenticação;
- os arquivos de upload ainda não possuem rotina automática de expurgo;
- a aplicação Flask integrada ainda não é um servidor WSGI de produção;
- gênero e arranjo ficam deliberadamente genéricos sem áudio ou IA complementar.
