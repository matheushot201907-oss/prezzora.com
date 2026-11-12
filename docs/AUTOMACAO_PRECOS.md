# Atualização automática de preços — Prezzora

Esta é a infraestrutura inicial, **não uma integração pronta com marketplaces**.

## Ativação
1. Obtenha um feed JSON autorizado de produtos/preços (API própria ou parceiro que permita redistribuição).
2. No GitHub, abra Settings > Secrets and variables > Actions e crie o segredo `PREZZORA_FEED_URL` com a URL HTTPS desse feed.
3. Após aprovar o pull request, abra Actions > Atualizar preços Prezzora > Run workflow para testar.
4. O agendamento tenta atualizar a cada duas horas (GitHub Actions pode atrasar execuções).

Formato esperado: uma lista JSON como:
```json
[
  {"id":"sku-001","name":"Produto de exemplo","store":"Loja autorizada","price":199.9,"url":"https://loja.example/produto"}
]
```
O exemplo acima **não é uma oferta real**.

O script valida preço, URL e campos, e gera `data/offers.json` com data de verificação. Se a fonte falhar, preserva os dados existentes. A atualização não está ligada à vitrine atual, que permanece demonstrativa até haver fonte real e revisão da integração.

## Próximas etapas
- Integrar um provedor autorizado, respeitando limites e termos da API.
- Conectar a vitrine ao arquivo de ofertas, mostrando data da última verificação e aviso para preços desatualizados.
- Guardar histórico de preços em banco de dados, em vez de depender de commits Git.
- Garantir que links de afiliado e imagens sejam permitidos pela fonte.
- Não adicionar chaves de API ao repositório.
