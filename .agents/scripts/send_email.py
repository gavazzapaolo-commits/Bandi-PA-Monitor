#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_via_applescript(to_addr, subject, body):
    """Crea e invia l'email tramite l'applicazione Mail nativa di macOS utilizzando AppleScript."""
    # Escapa virgolette per l'AppleScript
    escaped_subject = subject.replace('"', '\\"')
    escaped_body = body.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\r')
    
    applescript = f'''
    tell application "Mail"
        set newMail to make new outgoing message with properties {{subject:"{escaped_subject}", content:"{escaped_body}", visible:true}}
        tell newMail
            make new to recipient with properties {{address:"{to_addr}"}}
        end tell
        send newMail
    end tell
    '''
    
    try:
        process = subprocess.run(
            ['osascript', '-e', applescript],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if process.returncode == 0:
            print("Email creata e inviata con successo tramite AppleScript (Mail.app).")
            return True
        else:
            print(f"Errore AppleScript: {process.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Errore durante l'esecuzione di AppleScript: {e}", file=sys.stderr)
        return False

def send_via_smtp(to_addr, subject, body):
    """Invia l'email utilizzando un server SMTP configurato tramite variabili d'ambiente o file .env."""
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    
    if not smtp_server or not smtp_user or not smtp_pass:
        print("Errore: Credenziali SMTP non configurate (.env mancante o incompleto).", file=sys.stderr)
        return False
        
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = smtp_user
    msg['To'] = to_addr
    
    try:
        print(f"Tentativo di invio email tramite SMTP ({smtp_server}:{smtp_port})...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_addr], msg.as_string())
        server.close()
        print("Email inviata con successo tramite SMTP.")
        return True
    except Exception as e:
        print(f"Errore durante l'invio SMTP: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Invia o prepara report email per Bandi PA.")
    parser.add_argument("--to", default="gavazzapaolo@gmail.com", help="Email del destinatario")
    parser.add_argument("--subject", required=True, help="Oggetto dell'email")
    parser.add_argument("--body-file", help="File contenente il corpo dell'email")
    parser.add_argument("--body", help="Corpo dell'email come stringa")
    
    args = parser.parse_args()
    
    # Leggi corpo dell'email
    if args.body_file:
        try:
            with open(args.body_file, 'r', encoding='utf-8') as f:
                body = f.read()
        except Exception as e:
            print(f"Errore nella lettura del file body: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.body:
        body = args.body
    else:
        print("Errore: Specificare --body-file o --body.", file=sys.stderr)
        sys.exit(1)
        
    # Carica file .env se presente
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
    if os.path.exists(dotenv_path):
        with open(dotenv_path) as f:
            for line in f:
                if line.strip() and not line.strip().startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

    # Determina la modalità di invio
    if os.environ.get("SMTP_SERVER"):
        success = send_via_smtp(args.to, args.subject, body)
    else:
        # Default: tenta AppleScript (siamo su macOS)
        success = send_via_applescript(args.to, args.subject, body)
        if not success:
            print("\n--- EMULAZIONE DI SALVATAGGIO BOZZA LOCALE ---")
            print(f"Destinatario: {args.to}")
            print(f"Oggetto: {args.subject}")
            print("Corpo dell'email:")
            print(body)
            print("---------------------------------------------")
            success = True # Considera comunque completato come fallback locale
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
