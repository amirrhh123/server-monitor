#!/usr/bin/env python3
# ═══════════════════════════════════════════════════
#  monitor.py — ابزار CLI کامل برای مانیتورینگ سرور
#  استفاده: python monitor.py check --all --verbose
# ═══════════════════════════════════════════════════
import argparse, json, logging, os, subprocess
from datetime import datetime
from pathlib import Path

# ── اپیزود ۸: logging ──────────────────────────────
def setup_logger(name, log_file, verbose=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    for handler in [logging.FileHandler(log_file), logging.StreamHandler()]:
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger

# ── اپیزود ۴: config ───────────────────────────────
def load_config(path="config/settings.json"):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"services": ["nginx", "ssh"],
                "thresholds": {"cpu": 85, "mem": 90},
                "endpoints": ["http://localhost:8069/health"]}

# ── اپیزود ۶: subprocess ───────────────────────────
def check_service(name, logger):
    try:
        r = subprocess.run(["systemctl", "is-active", name],
                           capture_output=True, text=True, timeout=5)
        is_up = r.stdout.strip() == "active"
        level = logging.INFO if is_up else logging.ERROR
        logger.log(level, f"[SERVICE] {name}: {'running ✓' if is_up else 'DOWN ✗'}")
        return is_up
    except Exception as e:
        logger.error(f"[SERVICE] {name}: error — {e}")
        return False

# ── اپیزود ۵: HTTP health check ────────────────────
def check_endpoint(url, logger, timeout=5):
    try:
        import requests
        r = requests.get(url, timeout=timeout)
        ok = r.status_code == 200
        level = logging.INFO if ok else logging.ERROR
        logger.log(level, f"[HTTP] {url} → {r.status_code}")
        return ok
    except Exception as e:
        logger.error(f"[HTTP] {url} → error: {e}")
        return False

# ── اپیزود ۲ و ۳: check_resources ─────────────────
def check_resources(thresholds, logger):
    try:
        r = subprocess.run(["bash", "-c", "top -bn1|grep Cpu|awk '{print int($2)}'"],
                           capture_output=True, text=True, timeout=10)
        cpu = int(r.stdout.strip() or 0)
        limit = thresholds.get("cpu", 85)
        if cpu > limit:
            logger.warning(f"[CPU] {cpu}% > threshold {limit}%")
        else:
            logger.info(f"[CPU] {cpu}% OK")
    except Exception as e:
        logger.error(f"[CPU] check failed: {e}")

# ── اپیزود ۷: argparse + main ──────────────────────
def main():
    parser = argparse.ArgumentParser(prog="monitor")
    parser.add_argument("--config", default="config/settings.json")
    parser.add_argument("--verbose", "-v", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    chk = sub.add_parser("check")
    chk.add_argument("--service")
    chk.add_argument("--all", action="store_true")
    sub.add_parser("report")
    args = parser.parse_args()

    log_path = Path("monitoring-app/logs/monitor.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = setup_logger("monitor", log_path, args.verbose)
    config = load_config(args.config)

    logger.info(f"════ Monitor Start | {datetime.now():%Y-%m-%d %H:%M} ════")

    if args.cmd == "check":
        services = config["services"] if args.all else [args.service]
        for svc in services:
            check_service(svc, logger)
        check_resources(config["thresholds"], logger)
        for url in config["endpoints"]:
            check_endpoint(url, logger)

    logger.info("════ Monitor Done ════")

if __name__ == "__main__":
    main()