from http.server import BaseHTTPRequestHandler
import subprocess
import threading
import os
import json
import tempfile
import cgi
import io

# Global bot process tracker
_bot_process = None
_bot_lock = threading.Lock()


def _install_and_run(py_code: str, packages: str, result_holder: list):
    """Install packages then run the bot. Runs in a thread."""
    global _bot_process

    output_lines = []

    # ── 1. Install packages ──
    if packages.strip():
        pkgs = [p.strip() for p in packages.splitlines() if p.strip()]
        for pkg in pkgs:
            try:
                proc = subprocess.run(
                    ["pip", "install", pkg, "--quiet"],
                    capture_output=True, text=True, timeout=120
                )
                if proc.returncode == 0:
                    output_lines.append(f"✅ Installed: {pkg}")
                else:
                    output_lines.append(f"⚠️ Warning installing {pkg}: {proc.stderr[:200]}")
            except subprocess.TimeoutExpired:
                output_lines.append(f"⏱ Timeout installing {pkg}")
            except Exception as e:
                output_lines.append(f"❌ Error: {e}")

    # ── 2. Write bot file to temp location ──
    bot_path = "/tmp/user_bot.py"
    with open(bot_path, "w", encoding="utf-8") as f:
        f.write(py_code)
    output_lines.append("📄 Bot file saved")

    # ── 3. Kill any existing bot ──
    with _bot_lock:
        if _bot_process and _bot_process.poll() is None:
            _bot_process.terminate()
            try:
                _bot_process.wait(timeout=5)
            except Exception:
                _bot_process.kill()
            output_lines.append("⏹ Previous bot stopped")

    # ── 4. Start new bot process ──
    try:
        env = os.environ.copy()
        with _bot_lock:
            _bot_process = subprocess.Popen(
                ["python", bot_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                text=True
            )
        output_lines.append(f"🚀 Bot process started (PID: {_bot_process.pid})")

        # Read first few lines of output (non-blocking, 3 sec)
        import select, sys
        import time
        deadline = time.time() + 3
        while time.time() < deadline:
            if _bot_process.stdout.readable():
                try:
                    line = _bot_process.stdout.readline()
                    if line:
                        output_lines.append(line.rstrip())
                except Exception:
                    break
            time.sleep(0.1)

        result_holder.append({"success": True, "output": "\n".join(output_lines), "pid": _bot_process.pid})
    except Exception as e:
        output_lines.append(f"❌ Failed to start: {e}")
        result_holder.append({"success": False, "error": str(e), "output": "\n".join(output_lines)})


def _parse_multipart(rfile, content_type, content_length):
    """Parse multipart/form-data manually."""
    environ = {
        "REQUEST_METHOD": "POST",
        "CONTENT_TYPE": content_type,
        "CONTENT_LENGTH": str(content_length),
    }
    form = cgi.FieldStorage(fp=rfile, environ=environ, keep_blank_values=True)
    return form


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        global _bot_process
        if self.path == "/api/status":
            if _bot_process is None:
                status = "idle"
            elif _bot_process.poll() is None:
                status = "running"
            else:
                status = "stopped"
            self._json({"status": status})
        elif self.path == "/api/stop":
            with _bot_lock:
                if _bot_process and _bot_process.poll() is None:
                    _bot_process.terminate()
                    self._json({"status": "stopped"})
                else:
                    self._json({"status": "not_running"})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/api/run":
            self.send_response(404)
            self.end_headers()
            return

        try:
            content_type = self.headers.get("Content-Type", "")
            content_length = int(self.headers.get("Content-Length", 0))

            if "multipart/form-data" not in content_type:
                self._json({"success": False, "error": "Expected multipart/form-data"}, 400)
                return

            body = self.rfile.read(content_length)
            body_io = io.BytesIO(body)
            environ = {
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": content_type,
                "CONTENT_LENGTH": str(content_length),
            }
            form = cgi.FieldStorage(fp=body_io, environ=environ, keep_blank_values=True)

            # Get file
            if "file" not in form:
                self._json({"success": False, "error": "No file uploaded"}, 400)
                return
            file_item = form["file"]
            py_code = file_item.file.read().decode("utf-8", errors="replace")

            # Get packages
            packages = ""
            if "packages" in form:
                packages = form["packages"].value or ""

            # Run in background thread, wait up to 15s for startup result
            result_holder = []
            t = threading.Thread(target=_install_and_run, args=(py_code, packages, result_holder), daemon=True)
            t.start()
            t.join(timeout=15)

            if result_holder:
                self._json(result_holder[0])
            else:
                # Still running (bot started but thread didn't finish) — treat as success
                self._json({"success": True, "output": "Bot process launched (still initializing...)"})

        except Exception as e:
            self._json({"success": False, "error": str(e)}, 500)

    def _json(self, data, code=200):
        payload = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self._cors()
        self.end_headers()
        self.wfile.write(payload)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        pass  # Suppress default logs
