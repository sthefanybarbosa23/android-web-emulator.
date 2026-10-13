# Plano gratuito: Android 11 real no navegador

## Objetivo e limite atual

O objetivo é executar o Android 11 real com ReDroid, instalar APKs e depois transmitir/controlar a tela pelo navegador. A página em `web/` não é o Android: o sistema operacional precisa inicializar num host Linux separado.

**Não há, neste momento, hospedagem gratuita garantida que execute este projeto de ponta a ponta.** O ReDroid exige recursos do kernel Linux, como binderfs e ashmem/memfd, e execução de contêiner privilegiado. Hospedagem estática, como GitHub Pages, só pode publicar a interface. Não publique a porta ADB 5555 na internet.

## O que fazer somente pelo celular

1. Abra o repositório no navegador: https://github.com/sthefanybarbosa23/android-web-emulator.
2. Para editar arquivos, abra o menu do repositório e escolha **Code → Codespaces → Create codespace on main**, se a opção estiver disponível.
3. Em contas pessoais gratuitas, a cota publicada do Codespaces é de 120 core-hours (equivalente a 60 horas de uma máquina de 2 núcleos) e 15 GB-mês de armazenamento. A disponibilidade/cota restante depende da conta. Consulte a página de cobrança antes de iniciar e não configure gastos pagos.
4. Use o Codespaces para editar e validar código. Não conte com ele como servidor do Android: a cota gratuita de desenvolvimento não garante os recursos de kernel e contêiner privilegiado exigidos pelo ReDroid.
5. Procure um host Linux gratuito que declare suporte a Docker privilegiado e aos recursos de kernel exigidos pelo ReDroid. Se nenhum estiver disponível para sua conta/região, você poderá continuar desenvolvendo gratuitamente, mas não manter o Android 11 real hospedado até encontrar um host compatível.

## Preparar um host Linux compatível

Estes comandos são para o terminal do host Linux, não para o terminal do navegador Android:

```bash
git clone https://github.com/sthefanybarbosa23/android-web-emulator..git
cd android-web-emulator./infra
cp .env.example .env
```

Edite `.env` e coloque um token longo e aleatório em `EMULATOR_API_TOKEN`. Nunca publique esse token no GitHub nem envie para outra pessoa. Depois, somente num host compatível e controlado por você:

```bash
docker compose config
docker compose up -d --build
docker compose logs -f android api
```

O serviço API está vinculado a `127.0.0.1:8080` no Compose atual, por segurança. Isso significa que ele não fica público automaticamente; para usar remotamente será necessária uma configuração de acesso HTTPS segura. Não exponha ADB.

## Primeira meta de teste: instalar e abrir um APK

Depois que o Android inicializar e a API estiver acessível com segurança:

- `GET /health`: verifica apenas se a API responde; não prova que Android iniciou.
- `GET /api/status`: com `Authorization: Bearer SEU_TOKEN`, verifica a conexão ADB e o estado do boot.
- `POST /api/install`: envie um arquivo no campo multipart `file`, com o mesmo cabeçalho de autorização.
- `GET /api/apps`: lista pacotes de terceiros instalados.
- `POST /api/launch?package_name=com.exemplo.app`: tenta abrir o app pelo nome de pacote.

O nome `com.exemplo.app` é apenas um exemplo; use o pacote real do APK. Faça testes somente com APKs de fontes confiáveis e que você tem direito de usar.

## O que ainda falta para ser um emulador no navegador

- Executar a stack em host Linux compatível e registrar logs reais.
- Testar instalação e abertura de um APK de verdade.
- Transmitir a tela Android em tempo real para o navegador.
- Enviar toques, gestos e teclado do navegador para Android.
- Ligar os controles da página web aos endpoints protegidos.
- Implementar sessão, HTTPS e limites de uso.

Até esses testes serem concluídos, descreva o projeto como **protótipo de backend para Android 11**, não como emulador online pronto.
