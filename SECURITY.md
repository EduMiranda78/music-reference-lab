# Segurança

## Escopo

O Music Reference Lab processa arquivos de áudio, aceita texto fornecido pelo usuário e pode se comunicar com serviços locais ou remotos de IA.

## Recomendações

- mantenha o repositório privado quando houver configurações internas;
- nunca versione `.env`, tokens ou chaves;
- mantenha `uploads/` e `exports/` fora do Git;
- não exponha Ollama ou LM Studio diretamente à Internet;
- use uma rede privada para a IA remota;
- limite o acesso ao serviço Flask quando ele estiver em uma VPS;
- use proxy reverso, HTTPS e autenticação antes de disponibilizar o serviço publicamente;
- mantenha Docker, Python e dependências atualizados;
- revise arquivos enviados antes de compartilhá-los externamente.

## Uploads

A aplicação limita uploads a 35 MB e verifica a extensão permitida. Essa validação não substitui controles adicionais de segurança para uma instalação pública.

Para exposição externa, considere acrescentar:

- autenticação;
- rate limiting;
- validação de MIME real;
- expurgo automático de arquivos;
- diretório de upload isolado;
- limites por usuário;
- WSGI de produção;
- proxy reverso com limites de corpo de requisição.

## Credenciais

Use somente variáveis de ambiente e arquivos `.env` não versionados.

Se uma credencial for publicada acidentalmente, revogue e substitua a credencial antes de apenas removê-la do histórico.

## Relato de problemas

Como o repositório é privado, registre problemas de segurança diretamente no sistema de issues do repositório ou comunique o mantenedor por um canal privado.
