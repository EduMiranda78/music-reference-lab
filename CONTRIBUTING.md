# Contribuição e manutenção

Este é um projeto privado mantido por Eduardo Miranda.

## Fluxo sugerido

1. crie uma branch a partir de `main`;
2. faça alterações pequenas e identificáveis;
3. execute o smoke test;
4. valide a sintaxe Python;
5. revise alterações em `.env.example`, Docker e segurança;
6. abra um pull request para `main`.

## Validação local

```bash
python smoke_test.py
python -m compileall -q .
```

Com Docker:

```bash
docker compose build
```

## Commits

Prefira mensagens objetivas, por exemplo:

```text
Adiciona IA complementar opcional
Corrige persistência de exports
Melhora exportação para HeartMuLa
Documenta IA remota via Tailscale
```

## Cuidados

Não inclua em commits:

- `.env`;
- chaves ou tokens;
- arquivos de áudio reais;
- exports de usuários;
- backups;
- dumps ou logs com informações privadas.
