# verifica-il-file-json-estratto
verifica il file json estratto per doppioni errori o eventi simili

## Uso

Questo tool permette di leggere file JSON contenenti record e listarli ordinati per data o descrizione.

### Sintassi

```bash
python3 verifica_json.py <file.json> [--ordina <criterio>]
```

### Parametri

- `file.json`: Il file JSON da analizzare
- `--ordina` o `-o`: Criterio di ordinamento
  - `data` o `date`: Ordina per data (default)
  - `descrizione` o `description`: Ordina per descrizione

### Esempi

```bash
# Ordina per data (default)
python3 verifica_json.py esempio.json

# Ordina per descrizione  
python3 verifica_json.py esempio.json --ordina descrizione

# Usando la forma breve
python3 verifica_json.py esempio.json -o description
```

### Formato JSON supportato

Il tool supporta diversi formati JSON:

1. **Array di record diretto:**
```json
[
  {"data": "2024-01-15", "descrizione": "Evento 1"},
  {"data": "2024-01-10", "descrizione": "Evento 2"}
]
```

2. **Oggetto con array di record:**
```json
{
  "records": [
    {"data": "2024-01-15", "descrizione": "Evento 1"},
    {"data": "2024-01-10", "descrizione": "Evento 2"}
  ]
}
```

### Campi supportati

Il tool riconosce automaticamente questi campi per date:
- `data`, `date`, `timestamp`, `created_at`, `datetime`, `time`

E questi per descrizioni:
- `descrizione`, `description`, `desc`, `summary`, `title`, `name`, `evento`, `event`

### File di esempio

È incluso un file `esempio.json` con dati di test.
