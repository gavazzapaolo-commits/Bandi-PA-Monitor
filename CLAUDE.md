# Bandi Pubblici — Monitoraggio Profili Tecnico-Digitali

## Contesto

Paolo Gavazza, AI Manager & Strategist, 25 anni di background in UI/UX design, oggi
specializzato in AI strategy, sistemi agentici e pipeline di generative media.
Brand attuale: KeyHuman.

Questa cartella serve a monitorare bandi/concorsi pubblici italiani come possibile
piano B, condizionato all'esito di una questione debitoria con una vecchia società
che si chiarirà entro fine 2026. Non è un'urgenza immediata, ma le tempistiche dei
concorsi pubblici sono lunghe (mesi tra bando, prove, graduatoria), quindi il
monitoraggio inizia ora anche se la decisione di candidarsi è condizionale.

## Filtro profili — SOLO questi, scartare tutto il resto

Includere esclusivamente bandi per:
- Funzionario per la transizione digitale / esperto PNRR digitalizzazione
- Esperto/funzionario informatico, categoria D o equivalente
- Profili tecnico-digitali in enti pubblici, ministeri, agenzie, enti locali
- Posizioni legate a innovazione, trasformazione digitale, sistemi informativi PA

Scartare sempre (anche se segnalati da fonti esterne): sanità, forze armate/polizia,
scuola, profili amministrativi generici, profili impiegatizi senza componente
digitale/tecnica, posizioni private (es. accordi sindacali bancari — non sono bandi
pubblici), stage/tirocini.

## Fonti da usare

Fonte primaria: **inPA** (inpa.gov.it) — portale unico di reclutamento PA, filtrabile
per categoria/ruolo. Usare sempre questa come prima fonte.

Fonti secondarie (solo per integrare, mai come fonte unica): Gazzetta Ufficiale
sezione concorsi, portali regionali, bandi specifici di ministeri/agenzie con
desk digitalizzazione (es. Dipartimento Trasformazione Digitale, AgID, PA digitale).

Evitare aggregatori SEO generalisti (concorsando.it, concorsipubblici.net,
ticonsiglio.com, lavorofacile.info) come fonte primaria: mescolano bandi pubblici,
accordi sindacali privati e contenuti sponsorizzati senza filtro di pertinenza.
Possono essere usati solo per verificare una segnalazione specifica che Paolo
porta già in chat.

## Modalità di lavoro

- **Ricerca on-demand:** Paolo chiede esplicitamente un controllo (es. "controlla bandi", "cosa c'è di nuovo").
- **Routine settimanale automatizzata (GitHub Actions Cloud):** Ogni lunedì alle 09:00 (ora italiana) un workflow su GitHub Actions esegue automaticamente lo script `.agents/scripts/cloud_monitor.py` per cercare nuovi bandi, aggiorna il file `bandi-tracking.md` ed invia il report email a `gavazzapaolo@gmail.com` via SMTP (configurato in modo sicuro tramite GitHub Secrets).

Ogni bando rilevante trovato va:
1. Verificato contro il filtro profili sopra.
2. Aggiunto/aggiornato nel file `bandi-tracking.md` con la struttura definita lì.
3. Segnalato a Paolo con un riepilogo breve (non l'intero bando) + scadenza in evidenza.

## File della cartella

- `CLAUDE.md` — questo file
- `bandi-tracking.md` — tabella persistente dei bandi trovati nel tempo, con stato
- `.github/workflows/weekly_monitor.yml` — workflow di GitHub Actions per l'esecuzione in cloud ogni lunedì mattina
- `.agents/skills/bandi-watch/SKILL.md` — skill locale che descrive le istruzioni e regole di ricerca per l'agente
- `.agents/scripts/cloud_monitor.py` — script Python autonomo per cercare i bandi e aggiornare la tabella di tracciamento
- `.agents/scripts/send_email.py` — script Python di utilità per inviare il report email (tramite AppleScript/Mail.app o SMTP)
- `.agents/AGENTS.md` — regole e linee guida comportamentali del progetto per l'agente


