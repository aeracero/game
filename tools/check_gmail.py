import os
import sys
import ssl
import time
import socket
import smtplib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def step(name, fn):
    start = time.time()
    try:
        result = fn()
        print(f"  OK    {name} ({time.time() - start:.1f}s){': ' + str(result) if result else ''}")
        return True
    except Exception as ex:
        print(f"  FAIL  {name}: {type(ex).__name__}: {ex}")
        return False


def main():
    from starfall_pocket.config import load_mail_config
    cfg = load_mail_config()
    print(f"Python {sys.version.split()[0]}, OpenSSL {ssl.OPENSSL_VERSION}")
    print(f"Gmail address: {cfg['address'] or '(not set)'}, App Password: {'set, ' + str(len(cfg['app_password'])) + ' letters' if cfg['app_password'] else '(not set)'}")
    print()
    step("Find smtp.gmail.com", lambda: socket.gethostbyname("smtp.gmail.com"))
    for port in (465, 587):
        print(f"\nPort {port}:")
        if not step("Open connection", lambda: socket.create_connection(("smtp.gmail.com", port), 10).close()):
            continue
        holder = {}

        def connect():
            if port == 465:
                holder["s"] = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context(), timeout=20)
            else:
                s = smtplib.SMTP("smtp.gmail.com", port, timeout=20)
                s.ehlo()
                s.starttls(context=context())
                s.ehlo()
                holder["s"] = s
            return "Gmail answered"

        if not step("Secure connection and greeting", connect):
            continue
        if cfg["address"] and cfg["app_password"]:
            step("Log in with your App Password", lambda: holder["s"].login(cfg["address"], cfg["app_password"]) and None)
        try:
            holder["s"].quit()
        except Exception:
            pass
    print("\nCopy everything above and send it if you need help.")


if __name__ == "__main__":
    main()
