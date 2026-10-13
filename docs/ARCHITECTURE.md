# Arquitetura

1. web/: interface cliente; nesta etapa é apenas visual.
2. infra/compose.yaml: configuração inicial do ReDroid Android 11.
3. server/: futuro serviço autenticado de sessões.
4. Ponte de vídeo: captura da tela e transmissão ao navegador.
5. Ponte de entrada: toque e teclado enviados ao Android.
6. Pipeline APK: upload validado e instalação via ADB privado.

Fluxo futuro:
Browser --HTTPS/WSS--> API autenticada
Browser <-- vídeo ------ ponte de streaming <-- Android 11
Browser -- toque/teclas -> ponte de entrada --> Android 11
Browser -- APK -------> API -> worker isolado -> ADB privado -> Android

Segurança: nunca publique ADB (5555), não monte Docker socket na API e não use container privilegiado para serviços web. Para uso público, implemente autenticação, TLS, quotas, isolamento e auditoria.