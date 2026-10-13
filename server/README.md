# Backend API (primeira etapa)

Existe uma API inicial para consultar o estado do runtime e instalar APK por upload. Ainda **não** existe streaming de tela, controles remotos, gestão de sessões nem uma interface web ligada a estes endpoints.

## Configurar num host Linux compatível
1. Entre na pasta \`infra\`.
2. Copie \`.env.example\` para \`.env\`.
3. Troque \`EMULATOR_API_TOKEN\` por um segredo aleatório longo. Não publique o arquivo \`.env\`.
4. Execute \`docker compose up -d --build\`.
5. Consulte os logs: \`docker compose logs -f android api\`.

A API fica ligada a \`127.0.0.1:8080\` no host, não à internet. ADB fica apenas na rede privada Docker. O container Android usa \`privileged: true\`; execute somente num servidor Linux controlado e compatível com ReDroid.

## Endpoints
- \`GET /health\`: verificação simples do processo.
- \`GET /api/status\`: exige \`Authorization: Bearer SEU_TOKEN\`.
- \`POST /api/install\`: exige o mesmo token e recebe multipart/form-data no campo \`file\` com um arquivo \`.apk\`. O limite padrão é 200 MiB.

Exemplo local para status:
\`\`\`bash
curl -H "Authorization: Bearer SEU_TOKEN" http://127.0.0.1:8080/api/status
\`\`\`

Exemplo de instalação:
\`\`\`bash
curl -X POST -H "Authorization: Bearer SEU_TOKEN" \\
  -F "file=@/caminho/para/app.apk" \\
  http://127.0.0.1:8080/api/install
\`\`\`

## Limitações e segurança
- Não exponha ADB (5555) publicamente.
- Não coloque token no JavaScript/frontend nem em repositório público.
- Não encaminhe a API diretamente à internet sem HTTPS, autenticação reforçada, rate limiting e proteção contra abuso.
- O estado do Android depende do kernel/host. O runtime ainda precisa ser testado num servidor real.
- Upload APK não garante compatibilidade ou segurança do aplicativo enviado.
- O browser ainda não recebe vídeo e não envia eventos de toque/teclado.