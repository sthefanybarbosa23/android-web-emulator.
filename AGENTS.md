# Instruções para IA

## Objetivo
Construir um Android 11 real, acessível pelo navegador, com instalação de APKs legítimos. O Android roda no servidor Linux via ReDroid.

## Regras
1. Nunca descreva HTML como se fosse Android real.
2. Não marque funções como prontas sem teste ponta a ponta.
3. Nunca exponha ADB (5555) publicamente nem coloque segredos no frontend.
4. Upload de APK exige autenticação, limite de tamanho e validação.
5. Não monte docker.sock numa API web pública.
6. Não execute shell construído diretamente a partir da entrada do usuário.
7. Mantenha o runtime numa rede privada.
8. Documente codecs, latência, navegadores e encaminhamento de toque/teclado.
9. Registre testes reproduzíveis e seus resultados.
10. Faça alterações pequenas e explique os arquivos modificados.

## Etapas
1. Iniciar ReDroid Android 11 num host Linux compatível.
2. Verificar boot completo e ADB privado.
3. Testar instalação manual de APK autorizado.
4. Criar API de sessão autenticada.
5. Implementar streaming e eventos de entrada.
6. Implementar upload APK seguro.
7. Adicionar isolamento por usuário, limites e hardening.