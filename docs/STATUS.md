# Estado real do projeto

| Funcionalidade | Estado |
|---|---|
| Interface inicial | HTML/CSS implementados |
| Configuração ReDroid Android 11 | Criada, ainda não testada em host Linux |
| API de status ADB | Implementada, não testada ponta a ponta |
| Endpoint de upload/instalação APK | Implementado, não testado ponta a ponta |
| Boot Android concluído | Não verificado |
| Streaming de tela no navegador | Não implementado |
| Toque e teclado remotos | Não implementados |
| Interface ligada à API | Não implementada |
| Login e sessões multiusuário | Não implementados |

## Critérios para considerar funcional
- Android 11 inicializa e \`sys.boot_completed=1\`.
- APK autorizado instala e abre.
- A tela real aparece no navegador.
- Toque e teclado controlam o Android.
- ADB não está acessível publicamente.
- Os testes são realizados num host Linux compatível e documentados.