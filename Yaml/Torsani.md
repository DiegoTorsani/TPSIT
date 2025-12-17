# Descrizione dell'ultimo lavoro versionato su GitHub

## Sintesi del progetto
**Nome progetto:** *rubrica*  
**Scopo principale:** *Implementare l'export dati e la validazione dello schema (XSD)*  
**Stato attuale:** **Beta / in fase di integrazione** (branch principale: **main**)

### Dettagli tecnici
- **Repository:** *[github.com/tuo-account/rubrica](https://github.com/DiegoTorsani/TPSIT.git)*  
- **Branch principale:** **main**  
- **Ultimo commit:** That's it(vedere la pagina del repo)
- **Tecnologie:** *YAML*, *XML*, *XSD*, *Git*  
- **File chiave:** `dati/rubrica.yml`, `xml/rubrica.xml`, `schema/rubrica.xsd`  
- **Test:** test unitari inclusi; pipeline CI configurata per lint e test
- **Prova** Per validare il testo si può usare un editor online[^1]

#### Note di rilascio
- Calcolo automatico della *media* e impostazione del flag *insufficiente* nel generatore.  
- XML generato conforme allo XSD previsto (se convalidato).

---

## Considerazioni e lavori futuri
- Migliorare la copertura test per casi limite (voti non numerici, valori fuori range).  
- Integrare la validazione XSD nella pipeline CI per prevenire regressioni.  
- Aggiungere metadati (timestamp, autore) nell'XML di output se richiesto.
  
[^1]: https://stackedit.io

---
## Domande (seleziona con la checklist)
1. Come si chiama il babbo di Massa?  
   - [ ] Eldar  
   - [x] Enrico
   - [ ] Dario
   - [ ] Non lo sa neanche lui

2. Che voto mi darà Gianpiero?  
   - [ ] 6
   - [ ] 7
   - [ ] 5
   - [ ] 4

3. Quanto costa l'hotdog senza salse qui al bar del degasperi?  
   - [ ] 3  
   - [x] 2.50
   - [ ] 2.70
   - [ ] 3.20