# Estado real do projeto

| Funcionalidade | Estado |
|---|---|
| Interface inicial | HTML/CSS implementados; não ligada ao runtime |
| Configuração ReDroid Android 11 | Criada; ainda não testada em host Linux |
| API de status ADB | Implementada no código; não testada ponta a ponta |
| Endpoint de upload/instalação APK | Implementado no código; não testado ponta a ponta |
| Listagem de aplicativos instalados | Endpoint implementado no código; não testado |
| Tentativa de abrir aplicativo por pacote | Endpoint implementado no código; não testado |
| Boot Android concluído | Não verificado |
| APK real instalado e aberto | Ainda não demonstrado |
| Streaming de tela no navegador | Não implementado |
| Toque e teclado remotos | Não implementados |
| Interface ligada à API | Não implementada |
| Login/sessões multiusuário | Não implementados |

## Critérios para considerar funcional

- Android 11 inicializa e `sys.boot_completed=1`.
- Um APK autorizado instala e abre de verdade.
- A tela real aparece no navegador.
- Toque e teclado controlam o Android.
- ADB não está acessível publicamente.
- Os testes são realizados num host Linux compatível e documentados.

## Próxima etapa

Encontrar um ambiente Linux gratuito que permita os recursos de kernel e o contêiner privilegiado exigidos pelo ReDroid. Codespaces pode servir para editar/testar a API, mas não é considerado um host Android funcional. Enquanto não houver host compatível, manter o estado do projeto como experimental.
