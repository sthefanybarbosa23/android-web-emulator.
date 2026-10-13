import hmac
import os
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Android Web Emulator API", version="0.1.0")
TOKEN = os.environ.get("EMULATOR_API_TOKEN", "")
ANDROID_HOST = os.environ.get("ANDROID_ADB_HOST", "android")
ANDROID_PORT = os.environ.get("ANDROID_ADB_PORT", "5555")
MAX_APK_BYTES = int(os.environ.get("MAX_APK_BYTES", str(200 * 1024 * 1024)))

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


def connect_android() -> None:
    result = adb("connect", f"{ANDROID_HOST}:{ANDROID_PORT}", timeout=10)
    if result.returncode != 0 or "unable" in (result.stdout + result.stderr).lower():
        raise HTTPException(status_code=503, detail="Não foi possível conectar ao Android. Verifique o runtime e a rede privada.")


@app.get("/health")
def health():
    return {"ok": True, "service": "android-web-emulator-api"}


@app.get("/api/status")
def status(authorization: str | None = Header(default=None)):
    require_token(authorization)
    connect_android()
    state = adb("-s", f"{ANDROID_HOST}:{ANDROID_PORT}", "get-state")
    if state.returncode != 0 or "device" not in state.stdout:
        return {"connected": False, "android": "unavailable", "message": "ADB ainda não reconhece o dispositivo."}

    boot = adb("-s", f"{ANDROID_HOST}:{ANDROID_PORT}", "shell", "getprop", "sys.boot_completed")
    version = adb("-s", f"{ANDROID_HOST}:{ANDROID_PORT}", "shell", "getprop", "ro.build.version.release")
    return {
        "connected": True,
        "boot_completed": boot.stdout.strip() == "1",
        "android_version": version.stdout.strip() or "unknown",
    }


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

        connect_android()
        target = f"{ANDROID_HOST}:{ANDROID_PORT}"
        result = adb("-s", target, "install", "-r", str(path), timeout=180)
        if result.returncode != 0:
            message = (result.stderr or result.stdout or "Falha ao instalar APK.")[-1500:]
            raise HTTPException(status_code=502, detail=message)
        return {"installed": True, "output": result.stdout.strip() or "Success", "bytes": total}
    finally:
        await file.close()
        path.unlink(missing_ok=True)
