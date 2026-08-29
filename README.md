# Cotação do Boi

Busca a cotação diária da arroba do boi gordo (SP, MS, MG, GO, MT, RJ) no
Pecuária.com.br e guarda o histórico em `data/historico.json`, rodando
sozinho todo dia via GitHub Actions.

## Como colocar pra rodar (tudo pelo navegador, dá pra fazer pelo celular)

1. **Ative a permissão de escrita** em Settings → Actions → General →
   Workflow permissions → marque **"Read and write permissions"**.
2. Pronto. O workflow roda automaticamente no horário configurado
   (09h de Brasília, seg–sáb). Pra testar sem esperar, vá na aba **Actions**
   do repositório → escolha o workflow → **Run workflow**.

## Onde o site vai buscar os dados

O arquivo do histórico fica disponível nesse endereço:

https://raw.githubusercontent.com/cqrAgro/Agro-/main/data/historico.json

Seu site (hospedado no Vercel/Netlify) pode simplesmente fazer um fetch
nessa URL pra pegar o histórico mais recente.

## Antes de deixar rodando de verdade

- Dê uma olhada em `pecuaria.com.br/robots.txt` e nos Termos de Uso do site
  antes de automatizar a coleta.
- O script foi escrito com base no conteúdo da página em 27/08/2026. Se o
  site mudar o layout da tabela, o scraper vai parar de achar os dados —
  é só ajustar a função `extrair_tabela()` no `scrape_boi.py`.

