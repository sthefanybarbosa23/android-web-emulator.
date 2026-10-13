# Android Web Emulator — Android 11

Projeto para executar Android 11 real num servidor Linux compatível e evoluir para acesso pelo navegador. A interface HTML é só o cliente, não é um sistema Android.

## O que está no repositório
- Interface inicial em \`web/\`.
- Runtime Android 11 via ReDroid em \`infra/compose.yaml\`.
- API inicial em \`server/\` para consultar status e enviar APK para instalação.
- Instruções para IA em \`AGENTS.md\`.

## Iniciar num servidor Linux compatível
Consulte os requisitos de kernel na documentação oficial do ReDroid. No host preparado:
\`\`\`bash
cd infra
cp .env.example .env
\`\`\`
Edite \`.env\` e substitua \`EMULATOR_API_TOKEN\` por um segredo longo e aleatório. Depois:
\`\`\`bash
docker compose up -d --build
docker compose logs -f android api
\`\`\`

A API fica em \`127.0.0.1:8080\` e o ADB fica na rede Docker privada. Não publique a porta 5555. O container Android usa privilégios elevados; não execute num servidor que você não controla.

## Estado honesto
A configuração e a API inicial foram adicionadas ao repositório, mas **não foram executadas/testadas num host Linux**. Streaming da tela real no browser, toque/teclado, login e conexão da interface à API ainda não estão implementados. Consulte \`docs/STATUS.md\`.