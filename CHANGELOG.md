# Changelog

## 0.5.0, 2026-08-21

- adiciona `presets_exporter.py` ao repositório oficial;
- integra quatro presets de alta intensidade para Suno e HeartMuLa;
- adiciona perfis vocais masculino rouco / marra RJ e feminino suave / imponente RJ;
- adapta as métricas reais de `audio_analysis.py` para o `ActionHeuristicMapper`;
- mantém a exportação normal quando o usuário escolhe `Sem preset temático`;
- preserva o limite de 3000 caracteres no JSON copiável do Suno;
- adiciona `Exclude` de calmaria aos presets de guerra do Suno;
- adiciona negative prompts na exportação temática do HeartMuLa;
- remove o arquivo de áudio temporário após a análise para evitar acúmulo no disco da VPS;
- amplia o smoke test para validar presets, heurísticas e limite do JSON Suno.

## 0.4.2, 2026-08-21

- corrige o botão `Copiar` em acessos HTTP sem contexto seguro;
- adiciona fallback de cópia para navegadores que bloqueiam `navigator.clipboard` fora de HTTPS;
- limita o JSON pronto para copiar do Suno a no máximo 3000 caracteres;
- mantém a letra completa disponível no formulário e no JSON completo baixável;
- adiciona contador de caracteres do JSON Suno na tela de resultado;
- adiciona teste automático para garantir o limite de 3000 caracteres.

## 0.4.1, 2026-08-21

- substitui o servidor de desenvolvimento do Flask por Gunicorn em produção;
- adiciona `wsgi.py` como entrypoint WSGI;
- configura 1 worker e 2 threads para reduzir consumo na VPS;
- aumenta o timeout para análises de áudio e chamadas de IA mais demoradas;
- adiciona reciclagem periódica do worker para limitar crescimento de memória;
- envia logs de acesso e erro do Gunicorn para stdout/stderr do container;
- adiciona healthcheck HTTP nativo à imagem Docker;
- mantém `python app.py` disponível apenas para desenvolvimento local.

## 0.4.0, 2026-08-21

- adiciona Suno como plataforma de destino;
- adiciona link direto para `suno.com/create`;
- gera formulário para Custom Mode com Title, Styles e Lyrics;
- adiciona campo Exclude para Advanced Options;
- adiciona sugestões iniciais de Weirdness, Style Influence e Audio Influence;
- preserva a letra original em português na exportação Suno;
- atualiza interface, documentação, arquitetura e smoke test para quatro plataformas.

## 0.3.0, 2026-08-21

- adiciona IA complementar opcional por análise;
- mantém IA desligada por padrão;
- permite configuração de Ollama remoto;
- permite configuração de LM Studio ou endpoint compatível;
- adiciona links diretos para plataformas de destino;
- melhora a interface de status da IA;
- documenta arquitetura VPS + desktop Ubuntu via Tailscale;
- adiciona estrutura de projeto para GitHub privado.

## 0.2.0, 2026-08-21

- adiciona links de destino para Stable Audio, SOUNDRAW e HeartMuLa;
- melhora indicação do estado da IA complementar.

## 0.1.0, 2026-08-21

- primeira versão funcional;
- análise acústica local;
- Schemas A e B;
- exportação para três plataformas;
- execução com Docker Compose.
