# Changelog

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
