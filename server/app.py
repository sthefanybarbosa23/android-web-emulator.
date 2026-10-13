import hmac
import os
import re
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Android Web Emulator API", version="0.2.0")
TOKEN = os.environ.get("EMULATOR_API_TOKEN", "")
ANDROID_HOST = os.environ.get("ANDROID_ADB_HOST", "android")
ANDROID_PORT = os.environ.get("ANDROID_ADB_PORT", "5555")
MAX_APK_BYTES = int(os.environ.get("MAX_APK_BYTES", str(200 * 1024 * 1024)))
PACKAGE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(?:\\.[A-Za-z][A-Za-z0-9_]*)+$")

# CORS is deliberately not opened to arbitrary browser origins.
allowed_origin = os.environ.get("WEB_ORIGIN", "")
if allowed_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[allowed_origin],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )


def require_token(authorization: str | None) -> None:
    if not TOKEN:
        raise HTTPException(status_code=503, detail="Backend não configurado: defina EMULATOR_API_TOKEN.")
    expected = f"Bearer {TOKEN}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Token inválido ou ausente.")


def adb(*args: str, timeout: int = 20) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["adb", *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=504, detail="Tempo limite ao comunicar com Android.") from exc


def android_target() -> str:
    return f"{ANDROID_HOST}:{ANDROID_PORT}"


def connect_android() -> None:
    result = adb("connect", android_target(), timeout=10)
    combined = (result.stdout + result.stderr).lower()
    if result.returncode != 0 or "unable" in combined or "failed" in combined:
        raise HTTPException(status_code=503, detail="Não foi possível conectar ao Android. Verifique o runtime e a rede privada.")


def require_package_name(package_name: str) -> None:
    if len(package_name) > 255 or not PACKAGE_RE.fullmatch(package_name):
        raise HTTPException(status_code=400, detail="Nome de pacote inválido. Exemplo: com.exemplo.app.")


@app.get("/health")
def health():
    return {"ok": True, "service": "android-web-emulator-api", "version": app.version}


@app.get("/api/status")
def status(authorization: str | None = Header(default=None)):
    require_token(authorization)
    connect_android()
    target = android_target()
    state = adb("-s", target, "get-state")
    if state.returncode != 0 or state.stdout.strip() != "device":
        return {"connected": False, "android": "unavailable", "message": "ADB ainda não reconhece o dispositivo."}

    boot = adb("-s", target, "shell", "getprop", "sys.boot_completed")
    version = adb("-s", target, "shell", "getprop", "ro.build.version.release")
    return {
        "connected": True,
        "boot_completed": boot.stdout.strip() == "1",
        "android_version": version.stdout.strip() or "unknown",
    }


@app.get("/api/apps")
def list_apps(authorization: str | None = Header(default=None)):
    """Lista os pacotes de terceiros instalados no Android virtual."""
    require_token(authorization)
    connect_android()
    result = adb("-s", android_target(), "shell", "pm", "list", "packages", "-3", timeout=30)
    if result.returncode != 0:
        raise HTTPException(status_code=502, detail=(result.stderr or "Não foi possível listar os apps.")[-1000:])
    packages = sorted(
        line.removeprefix("package:").strip()
        for line in result.stdout.splitlines()
        if line.strip().startswith("package:")
    )
    return {"apps": packages, "count": len(packages)}


@app.post("/api/launch")
def launch_app(package_name: str, authorization: str | None = Header(default=None)):
    """Tenta abrir a atividade principal de um app já instalado."""
    require_token(authorization)
    require_package_name(package_name)
    connect_android()
    target = android_target()
    installed = adb("-s", target, "shell", "pm", "path", package_name)
    if installed.returncode != 0 or "package:" not in installed.stdout:
        raise HTTPException(status_code=404, detail="Esse pacote não parece estar instalado.")
    result = adb(
        "-s", target, "shell", "monkey", "-p", package_name,
        "-c", "android.intent.category.LAUNCHER", "1", timeout=30,
    )
    combined = (result.stdout + result.stderr).strip()
    if result.returncode != 0 or "No activities found" in combined:
        raise HTTPException(status_code=502, detail=(combined or "Não foi possível abrir o aplicativo.")[-1200:])
    return {"launched": True, "package_name": package_name, "output": combined[-1200:]}


@app.post("/api/install")
async def install_apk(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
):
    require_token(authorization)
    if not file.filename or not file.filename.lower().endswith(".apk"):
        raise HTTPException(status_code=400, detail="Envie um arquivo com extensão .apk.")

    # Stream to a temporary file with a strict size cap; never trust the client filename.
    fd, temp_name = tempfile.mkstemp(prefix="upload-", suffix=".apk")
    os.close(fd)
    path = Path(temp_name)
    total = 0
    try:
        with path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_APK_BYTES:
                    raise HTTPException(status_code=413, detail="APK excede o limite configurado.")
                output.write(chunk)
        if total == 0:
            raise HTTPException(status_code=400, detail="O arquivo está vazio.")

        # APKs are ZIP containers. This is a basic file sanity check, not a security scan.
        with path.open("rb") as uploaded:
            if uploaded.read(4) != b"PK\\x03\\x04":
                raise HTTPException(status_code=400, detail="O arquivo não parece ser um APK/ZIP válido.")

        connect_android()
        result = adb("-s", android_target(), "install", "-r", str(path), timeout=180)
        if result.returncode != 0 or "success" not in (result.stdout + result.stderr).lower():
            message = (result.stderr or result.stdout or "Falha ao instalar APK.")[-1500:]
            raise HTTPException(status_code=502, detail=message)
        return {"installed": True, "output": result.stdout.strip() or "Success", "bytes": total}
    finally:
        await file.close()
        path.unlink(missing_ok=True)
