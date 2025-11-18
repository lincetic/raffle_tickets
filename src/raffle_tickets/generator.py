import csv
from pathlib import Path
from typing import List, Tuple, Optional


# ============================================================
# Public API
# ============================================================

def read_participants(csv_path: str, digits: int) -> List[Tuple[str, str]]:
    """
    Read participants from a CSV file and normalize ticket numbers.

    Returns:
        List[Tuple[ticket_number, participant_name]]
    """
    validate_digits(digits)

    participants = []

    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo CSV no encontrado: {csv_path}")

    # --- Aquí NO cerramos el archivo hasta terminar ---
    with path.open(newline="", encoding="utf-8-sig") as csvfile:
        sample = csvfile.read(2048)
        csvfile.seek(0)

        # Detectar delimitador seguro
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,")
        except Exception:
            dialect = csv.excel  # fallback

        reader = csv.DictReader(csvfile, dialect=dialect)

        validate_csv_header(reader.fieldnames or [])

        for row in reader:
            name = normalize_name(row.get("nombre", ""))
            number = normalize_number(row.get("numero", ""), digits)

            if number is None:
                continue  # ignorar filas inválidas

            participants.append((number, name))

    return participants


def generate_tickets_from_digits(digits: int) -> List[Tuple[str, Optional[str]]]:
    """
    Generate all possible number combinations for the given digit amount.
    """
    validate_digits(digits)

    limit = 10 ** digits
    return [(str(i).zfill(digits), None) for i in range(limit)]


# ============================================================
# Validation
# ============================================================

def validate_digits(digits: int):
    if not isinstance(digits, int) or digits < 1 or digits > 10:
        raise ValueError("digits must be an integer between 1 and 10.")


def validate_csv_header(fields):
    required = {"nombre", "numero"}
    missing = required - set(fields)

    if missing:
        raise ValueError(
            f"El CSV debe contener las columnas {required}. "
            f"Columnas encontradas: {fields}"
        )


# ============================================================
# Normalization helpers
# ============================================================

def normalize_name(name: str) -> str:
    name = (name or "").strip()
    return name if name else "Desconocido"


def normalize_number(number: str, digits: int) -> Optional[str]:
    if not number:
        return None

    number = number.strip()
    if not number.isdigit():
        return None

    return number.zfill(digits)
