---
name: bandi-watch
description: Linee guida ed istruzioni per monitorare, ricercare e filtrare bandi di concorso e avvisi per profili tecnico-digitali nella Pubblica Amministrazione italiana.
---

# Skill `bandi-watch`

Questa skill automatizza e standardizza la ricerca dei bandi pubblici per profili digitali e tecnologici, come specificato in [CLAUDE.md](file:///Users/paolo/Desktop/Second_Brain/Bandi-PA-Monitor/CLAUDE.md).

## Criteri di Ricerca e Selezione

### Profili da INCLUDERE
Includi esclusivamente bandi per i seguenti ruoli tecnico-digitali:
- **Funzionario per la transizione digitale** / Esperto PNRR digitalizzazione.
- **Esperto/Funzionario informatico** (Area dei Funzionari, ex Categoria D, o equivalenti).
- **Profili tecnico-digitali** in enti pubblici (ministeri, agenzie nazionali, regioni, comuni, province).
- **Specialista in sistemi informativi**, sicurezza informatica, data science nella PA, gestione di progetti di innovazione/trasformazione digitale.

### Profili da ESCLUDERE
Scarta sempre, senza eccezioni:
- Bandi in ambito sanitario (medici, infermieri, amministrativi sanitari).
- Bandi per forze armate, forze dell'ordine o polizia locale.
- Bandi del settore scolastico/accademico (personale docente, ATA, amministrativo scolastico).
- Profili amministrativi generici, contabili o gestionali privi di focus ICT/digitale.
- Posizioni in aziende private o a partecipazione privata (es. accordi sindacali bancari).
- Stage, tirocini e borse di studio.

## Fonti di Ricerca

1. **Fonte Primaria**:
   - **inPA (inpa.gov.it)**: Portale unico del reclutamento PA. Effettuare qui la ricerca principale inserendo parole chiave come "informatico", "tecnologie", "transizione digitale", "digitalizzazione", "sistemi informativi".
2. **Fonti Secondarie**:
   - **Gazzetta Ufficiale (gazzettaufficiale.it)**: Sezione 4ª Serie Speciale "Concorsi ed Esami".
   - **AgID (agid.gov.it)**: Amministrazione Trasparente - Bandi di Concorso.
   - **Dipartimento Trasformazione Digitale (innovazione.gov.it)**: Sezione avvisi e collaborazioni per esperti.
   - **Formez PA (formez.it)**: Sezione concorsi per bandi in corso gestiti da Formez/RIPAM.

## Procedura di Aggiornamento `bandi-tracking.md`

Quando esegui una ricerca on-demand:
1. Effettua la ricerca tramite gli strumenti web, filtrando rigorosamente secondo i criteri sopra descritti.
2. Per ogni bando idoneo identificato, aggiungi una riga nella tabella principale di [bandi-tracking.md](file:///Users/paolo/Desktop/Second_Brain/Bandi-PA-Monitor/bandi-tracking.md) compilando tutte le colonne.
3. Seleziona lo stato appropriato (solitamente `da valutare`).
4. Aggiorna lo **Storico ricerche** con la data odierna e un breve esito (es. *"trovati 2 bandi compatibili su inPA"*).
5. Presenta al partner di programmazione un riassunto dei bandi rilevanti trovati, evidenziando la scadenza per l'invio della candidatura e i requisiti chiave.
