#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime

# Assicuriamoci che duckduckgo_search sia disponibile
try:
    from duckduckgo_search import DDGS
except ImportError:
    print("duckduckgo_search non installato. Installalo con: pip install duckduckgo-search")
    sys.exit(1)

def clean_markdown_cell(text):
    """Pulisce il testo per evitare che rompa il formato della tabella markdown."""
    if not text:
        return ""
    return str(text).replace('|', '\\|').replace('\n', ' ').strip()

def parse_deadline(text):
    """Tenta di estrarre una data di scadenza (formato italiano gg/mm/aaaa) dal testo."""
    match = re.search(r'\b(0?[1-9]|[12]\d|3[01])[-/.](0?[1-9]|1[012])[-/.](20\d\d)\b', text)
    if match:
        day, month, year = match.groups()
        return f"{int(day):02d}/{int(month):02d}/{year}"
    return "Verificare"

def run_search():
    """Esegue la ricerca su inPA tramite DuckDuckGo e restituisce i risultati strutturati."""
    query = "site:inpa.gov.it/bandi-e-avvisi/ \"funzionario\" OR \"specialista\" OR \"esperto\" informatico OR digitale OR tecnologie OR \"sistemi informativi\" OR \"transizione digitale\""
    print(f"Esecuzione ricerca DDGS con query: {query}")
    
    results = []
    try:
        with DDGS() as ddgs:
            ddgs_results = ddgs.text(query, max_results=15)
            for r in ddgs_results:
                title = r.get("title", "")
                snippet = r.get("body", "")
                href = r.get("href", "")
                
                # Applica filtri rigidi di inclusione/esclusione sul titolo e snippet
                title_lower = title.lower()
                snippet_lower = snippet.lower()
                
                # Filtri di esclusione
                exclusions = ["sanità", "sanitario", "scuola", "università", "polizia", "militare", "forze armate", "privato", "stage", "tirocinio"]
                if any(exc in title_lower or exc in snippet_lower for exc in exclusions):
                    print(f"Escluso per filtri negativi: {title}")
                    continue
                
                # Filtri di inclusione (informatico, digitale, tecnologie, sistemi informativi, transizione digitale)
                inclusions = ["informatico", "digitale", "tecnologie", "sistemi informativi", "transizione digitale", "ict", "cybersecurity"]
                if not any(inc in title_lower or inc in snippet_lower for inc in inclusions):
                    print(f"Escluso per mancanza di parole chiave tecniche: {title}")
                    continue
                
                # Estrai l'ente dal titolo
                # Spesso il titolo su inPA è nel formato: "Concorso per... - ENTE" o simile
                ente = "PA (vedi link)"
                parts = title.split(" - ")
                if len(parts) > 1:
                    ente = parts[-1].strip()
                elif "presso" in title_lower:
                    match_ente = re.search(r'presso (?:il|la|l\')\s*([^,.-]+)', title, re.IGNORECASE)
                    if match_ente:
                        ente = match_ente.group(1).strip()
                
                # Determina categoria e posti
                posti = "1"
                match_posti = re.search(r'\b(\d+)\s*(?:posti|unità|posto)\b', title_lower)
                if match_posti:
                    posti = match_posti.group(1)
                    
                categoria = "Funzionari (ex D)"
                if "dirigente" in title_lower:
                    categoria = "Dirigenti"
                elif "istruttore" in title_lower or "assistente" in title_lower:
                    categoria = "Istruttori (ex C)"
                
                deadline = parse_deadline(snippet)
                if deadline == "Verificare" and "scadenza" in snippet_lower:
                    # Cerca di estrarre data vicino a "scadenza"
                    match_scad = re.search(r'scadenza\s*(?:il)?\s*(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})', snippet_lower)
                    if match_scad:
                        deadline = parse_deadline(match_scad.group(1))

                results.append({
                    "bando": title.split(" - ")[0].replace("Concorso pubblico", "").replace("Concorso", "").strip(),
                    "ente": ente,
                    "posti": posti,
                    "categoria": categoria,
                    "requisiti": "Laurea ICT / Esperienza digitale (verifica nel bando)",
                    "scadenza": deadline,
                    "fonte": "inPA",
                    "url": href
                })
    except Exception as e:
        print(f"Errore durante la ricerca DuckDuckGo: {e}", file=sys.stderr)
        
    return results

def update_tracking_file(new_bandi):
    """Aggiorna il file bandi-tracking.md con i nuovi bandi trovati."""
    tracking_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'bandi-tracking.md')
    
    if not os.path.exists(tracking_path):
        print(f"Errore: File {tracking_path} non trovato.", file=sys.stderr)
        return []
        
    with open(tracking_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Estrai bandi esistenti per evitare duplicati
    existing_titles = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith('|') and not line.startswith('| Bando') and not line.startswith('|---'):
            parts = line.split('|')
            if len(parts) > 1:
                existing_titles.append(parts[1].strip().lower())
                
    added_bandi = []
    new_rows = []
    for b in new_bandi:
        # Controlla se è già presente (confronto case-insensitive)
        if b["bando"].lower() in existing_titles or any(et in b["bando"].lower() for et in existing_titles):
            continue
            
        row = f"| {clean_markdown_cell(b['bando'])} | {clean_markdown_cell(b['ente'])} | {clean_markdown_cell(b['posti'])} | {clean_markdown_cell(b['categoria'])} | {clean_markdown_cell(b['requisiti'])} | {clean_markdown_cell(b['scadenza'])} | [{b['fonte']}]({b['url']}) | da valutare | Trovato da Cloud Monitor. |"
        new_rows.append(row)
        added_bandi.append(b)
        
    if new_rows:
        print(f"Aggiunta di {len(new_rows)} nuovi bandi a bandi-tracking.md...")
        # Inserisci i nuovi bandi sotto l'intestazione della tabella (linea 7/8)
        table_header_index = -1
        for idx, line in enumerate(lines):
            if line.startswith('|---'):
                table_header_index = idx
                break
                
        if table_header_index != -1:
            lines = lines[:table_header_index+1] + new_rows + lines[table_header_index+1:]
            
        # Aggiorna lo storico ricerche
        today = datetime.now().strftime("%d/%m/%Y")
        esito = f"Trovati {len(new_rows)} nuovi bandi attivi tramite Cloud Monitor."
        new_history_row = f"| {today} | {esito} |"
        
        history_header_index = -1
        for idx, line in enumerate(lines):
            if line.startswith('| Data ricerca |'):
                history_header_index = idx
                break
                
        if history_header_index != -1:
            # Trova la linea successiva all'intestazione (il divisore |---|---|)
            div_idx = history_header_index + 1
            lines = lines[:div_idx+1] + [new_history_row] + lines[div_idx+1:]
            
        new_content = '\n'.join(lines)
        with open(tracking_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    return added_bandi

def build_email_body(added_bandi, all_active):
    """Costruisce il corpo dell'email in base ai bandi aggiunti e a quelli in scadenza."""
    today = datetime.now().strftime("%d/%m/%Y")
    body = f"Report settimanale Bandi PA — Aggiornamento del {today}\n\n"
    
    # Sezione Nuovi Bandi
    body += "### 1. NUOVI BANDI TROVATI QUESTA SETTIMANA\n"
    if added_bandi:
        for idx, b in enumerate(added_bandi, 1):
            body += f"{idx}. {b['bando']} presso {b['ente']}\n"
            body += f"   - Posti: {b['posti']} | Categoria: {b['categoria']}\n"
            body += f"   - Scadenza: {b['scadenza']}\n"
            body += f"   - Link inPA: {b['url']}\n\n"
    else:
        body += "Nessuna novità.\n\n"
        
    # Sezione In Scadenza
    body += "### 2. BANDI IN SCADENZA ENTRO 30 GIORNI\n"
    in_scadenza = []
    # Cerchiamo bandi attivi nel file bandi-tracking.md
    tracking_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'bandi-tracking.md')
    if os.path.exists(tracking_path):
        with open(tracking_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for line in lines:
            if line.startswith('|') and not line.startswith('| Bando') and not line.startswith('|---') and "esempio:" not in line:
                parts = line.split('|')
                if len(parts) >= 9:
                    bando = parts[1].strip()
                    ente = parts[2].strip()
                    scadenza = parts[6].strip()
                    stato = parts[8].strip().lower()
                    
                    if stato in ["da valutare", "in scadenza", "in corso"]:
                        # Controlliamo la scadenza
                        try:
                            scad_date = datetime.strptime(scadenza, "%d/%m/%Y")
                            days_left = (scad_date - datetime.now()).days
                            if 0 <= days_left <= 30:
                                in_scadenza.append((bando, ente, scadenza, days_left))
                        except ValueError:
                            # Se la scadenza non è una data valida (es. "Verificare") la includiamo per sicurezza
                            in_scadenza.append((bando, ente, scadenza, 999))
                            
    if in_scadenza:
        # Ordina per giorni rimasti
        in_scadenza.sort(key=lambda x: x[3])
        for bando, ente, scadenza, days in in_scadenza:
            lbl_days = f"({days} giorni rimasti)" if days != 999 else "(verifica data)"
            body += f"- {bando} ({ente}) — SCADENZA: {scadenza} {lbl_days}\n"
        body += "\n"
    else:
        body += "Nessun bando in scadenza nei prossimi 30 giorni.\n\n"
        
    # Sezione Borderline
    body += "### 3. EVENTUALI BANDI BORDERLINE DA VALIDARE\n"
    borderline = [b for b in added_bandi if "istruttore" in b['bando'].lower() or "assistente" in b['bando'].lower() or "bolzano" in b['ente'].lower()]
    if borderline:
        for b in borderline:
            body += f"- {b['bando']} ({b['ente']}): verificare requisiti specifici (Cat. C o bilinguismo).\n"
    else:
        body += "Nessun bando borderline rilevato questa settimana.\n"
        
    return body

def main():
    print("Inizio scansione settimanale bandi PA...")
    new_bandi = run_search()
    print(f"Scansione completata. Trovati {len(new_bandi)} bandi potenzialmente idonei.")
    
    added_bandi = update_tracking_file(new_bandi)
    print(f"Aggiunti {len(added_bandi)} nuovi bandi in archivio.")
    
    # Prepara ed invia il report email
    email_body = build_email_body(added_bandi, new_bandi)
    
    # Salva copia locale del report
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    report_filename = f"report_{datetime.now().strftime('%Y%m%d')}.txt"
    report_path = os.path.join(reports_dir, report_filename)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(email_body)
    print(f"Copia del report salvata in: {report_path}")
    
    # Richiama send_email.py per inviare l'email
    # Se siamo su GitHub Actions, useremo SMTP
    send_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'send_email.py')
    subject = f"Bandi PA — aggiornamento {datetime.now().strftime('%d/%m/%Y')}"
    
    import subprocess
    cmd = [sys.executable, send_script, "--subject", subject, "--body-file", report_path]
    print(f"Esecuzione di send_email.py...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(f"Errori send_email.py: {res.stderr}", file=sys.stderr)

if __name__ == "__main__":
    main()
