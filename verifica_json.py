#!/usr/bin/env python3
"""
Verifica JSON - Tool per verificare e listare record da file JSON
Elenca tutti i record ordinati per data o descrizione
"""

import json
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Any


def parse_date(date_string: str) -> datetime:
    """Parse various date formats"""
    date_formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%m/%d/%Y'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    # If no format matches, return a default date for sorting purposes
    return datetime.min


def extract_date_field(record: Dict[str, Any]) -> str:
    """Extract date field from record, trying common field names"""
    date_fields = ['data', 'date', 'timestamp', 'created_at', 'datetime', 'time']
    
    for field in date_fields:
        if field in record:
            return str(record[field])
    
    return ""


def extract_description_field(record: Dict[str, Any]) -> str:
    """Extract description field from record, trying common field names"""
    desc_fields = ['descrizione', 'description', 'desc', 'summary', 'title', 'name', 'evento', 'event']
    
    for field in desc_fields:
        if field in record:
            return str(record[field])
    
    return ""


def load_json_file(filename: str) -> List[Dict[str, Any]]:
    """Load and parse JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # If it's a dict, look for common array keys
            for key in ['records', 'data', 'items', 'entries']:
                if key in data and isinstance(data[key], list):
                    return data[key]
            # If no array found, treat the dict as a single record
            return [data]
        else:
            raise ValueError("JSON deve contenere un array di record o un oggetto")
    
    except FileNotFoundError:
        print(f"Errore: File '{filename}' non trovato")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Errore nella lettura del file: {e}")
        sys.exit(1)


def sort_records(records: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    """Sort records by date or description"""
    if sort_by == 'data' or sort_by == 'date':
        return sorted(records, key=lambda x: parse_date(extract_date_field(x)))
    elif sort_by == 'descrizione' or sort_by == 'description':
        return sorted(records, key=lambda x: extract_description_field(x).lower())
    else:
        print(f"Criterio di ordinamento non valido: {sort_by}")
        print("Usa 'data' o 'descrizione'")
        sys.exit(1)


def display_records(records: List[Dict[str, Any]], sort_by: str):
    """Display records in a formatted way"""
    if not records:
        print("Nessun record trovato nel file JSON")
        return
    
    print(f"\n=== RECORD ORDINATI PER {sort_by.upper()} ===")
    print(f"Totale record: {len(records)}\n")
    
    for i, record in enumerate(records, 1):
        print(f"--- Record {i} ---")
        
        # Display date field
        date_value = extract_date_field(record)
        if date_value:
            print(f"Data: {date_value}")
        
        # Display description field  
        desc_value = extract_description_field(record)
        if desc_value:
            print(f"Descrizione: {desc_value}")
        
        # Display other fields
        for key, value in record.items():
            if key.lower() not in ['data', 'date', 'timestamp', 'created_at', 'datetime', 'time', 
                                  'descrizione', 'description', 'desc', 'summary', 'title', 'name', 'evento', 'event']:
                print(f"{key}: {value}")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Verifica e lista record da file JSON ordinati per data o descrizione'
    )
    parser.add_argument('file', help='File JSON da analizzare')
    parser.add_argument(
        '--ordina', '-o', 
        choices=['data', 'date', 'descrizione', 'description'],
        default='data',
        help='Criterio di ordinamento: data o descrizione (default: data)'
    )
    
    args = parser.parse_args()
    
    # Load and parse JSON file
    records = load_json_file(args.file)
    
    # Sort records
    sorted_records = sort_records(records, args.ordina)
    
    # Display results
    display_records(sorted_records, args.ordina)


if __name__ == "__main__":
    main()