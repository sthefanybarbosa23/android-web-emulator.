# Android Web Emulator — Android 11

Projeto experimental para executar Android 11 real num host Linux compatível e, numa etapa posterior, acessá-lo pelo navegador. A interface HTML não é Android; o runtime é o ReDroid.

## Componentes atuais

- `web/`: interface inicial, ainda não ligada ao runtime.
- `infra/compose.yaml`: contêiner ReDroid Android 11 e API na rede Docker privada.
- `server/`: API FastAPI para status, instalação de APK, listagem de apps e tentativa de abertura de um app instalado.
- `docs/PLANO_GRATUITO.md`: plano para desenvolver pelo celular, limites de hospedagem grátis e primeiros testes reais.
- `docs/STATUS.md`: estado honesto do projeto.

## Hospedagem gratuita

Não existe garantia de que um provedor gratuito permita o ReDroid: ele exige recursos específicos do kernel Linux e contêiner privilegiado. GitHub Pages hospeda apenas arquivos estáticos e não executa Android. O Codespaces pode ajudar a editar e validar código, mas não é uma hospedagem garantida para o runtime Android. Veja [o plano gratuito](docs/PLANO_GRATUITO.md).

## Iniciar num host Linux compatível

Consulte primeiro os [requisitos oficiais do ReDroid](https://github.com/remote-android/redroid-doc). Num host preparado e controlado por você:

```bash
cd infra
cp .env.example .env
```

Edite `.env` e substitua `EMULATOR_API_TOKEN` por um segredo longo e aleatório. Depois:

```bash
docker compose config
docker compose up -d --build
docker compose logs -f android api
```

A API está vinculada a `127.0.0.1:8080`; não fica pública automaticamente. O ADB fica na rede Docker privada. **Nunca publique a porta 5555 nem exponha a API sem HTTPS e autenticação.** O contêiner Android usa privilégios elevados; não execute num servidor que você não controla.

## Endpoints disponíveis no código

Todos os endpoints `/api/*` exigem `Authorization: Bearer SEU_TOKEN`.

- `GET /health`: verifica apenas se a API responde.
- `GET /api/status`: consulta ADB, versão e conclusão do boot.
- `POST /api/install`: instala um arquivo APK enviado no campo multipart `file`.
- `GET /api/apps`: lista pacotes de terceiros instalados.
- `POST /api/launch?package_name=com.exemplo.app`: tenta abrir um pacote instalado.

Esses endpoints ainda não foram testados ponta a ponta num host Linux. Use somente APKs de fontes confiáveis e que você tem direito de usar.

## Estado honesto

O backend é um protótipo. Boot Android, instalação/abertura real de APK, streaming da tela no navegador, controles por toque/teclado e integração da interface ainda não foram verificados ou concluídos. Consulte `docs/STATUS.md`.
