# Execução em produção

## Servidor WSGI

A imagem Docker do Music Reference Lab usa Gunicorn como servidor WSGI.

O entrypoint é:

```text
wsgi:app
```

A configuração atual prioriza baixo consumo de memória e tolerância a análises demoradas:

```text
workers: 1
threads: 2
timeout: 300s
graceful timeout: 30s
keep-alive: 5s
max requests: 200 + jitter de até 20
```

Os logs de acesso e erro são enviados para stdout e stderr e podem ser consultados com:

```bash
docker compose logs --tail=100 music-reference-lab
```

## Healthcheck

A imagem executa um healthcheck HTTP interno contra:

```text
http://127.0.0.1:8080/
```

Após o período inicial, o estado esperado é `healthy`.

## Deploy

Atualize primeiro os arquivos versionados:

```bash
git fetch origin
git merge --ff-only origin/main
```

Construa a imagem:

```bash
docker compose build music-reference-lab
```

Recrie somente este serviço:

```bash
docker compose up -d --no-deps music-reference-lab
```

Valide:

```bash
docker compose ps
curl -I http://localhost:8080/
docker exec music-reference-lab cat /app/VERSION
docker compose logs --tail=50 music-reference-lab
```

## Ambiente com Tailscale SSH

Neste servidor específico, operações que recriam containers ou interfaces Docker já interromperam sessões Tailscale SSH.

Por isso, operações de leitura, Git e preparação de arquivos podem ser feitas pela sessão Tailscale, mas a etapa que recria o container deve ser executada pelo console da provedora da VPS ou por outro acesso que não dependa do Tailscale.

## Desenvolvimento local

Para desenvolvimento simples ainda é possível executar:

```bash
python app.py
```

Esse modo usa o servidor integrado do Flask e não deve ser usado como servidor de produção.
