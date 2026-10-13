# Android Web Emulator — Android 11

Objetivo: acessar um Android real remotamente pelo navegador. O Android roda num servidor Linux; HTML não é o Android.

## Estado atual
A interface e a configuração inicial estão aqui. O boot do Android não foi testado; instalação de APK pelo navegador, streaming de tela e controle por toque/teclado ainda não estão implementados.

## Requisitos
Host Linux compatível com ReDroid, Docker Engine e Docker Compose. Consulte a documentação oficial do ReDroid para requisitos de kernel.

## Iniciar em host Linux preparado
\`\`\`bash
cd infra
docker compose up -d
docker compose logs -f android
\`\`\`

Não exponha ADB (porta 5555) à internet. O container usa privilégios elevados e só deve rodar em host que você controla.

Abra web/index.html ou sirva a pasta web por HTTP. Leia docs/STATUS.md e AGENTS.md antes de continuar.