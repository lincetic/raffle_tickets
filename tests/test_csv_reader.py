import os
from raffle_tickets.generator import read_participants

DATA = os.path.join(os.path.dirname(__file__), "data")

def test_read_participants_ok():
    path = os.path.join(DATA, "participants_ok.csv")
    rows = read_participants(path, digits=3)

    assert len(rows) == 3
    assert rows[0] == ("001", "Juan")
    assert rows[1] == ("123", "Ana")
    assert rows[2] == ("999", "Pedro")


def test_read_participants_wrong_header():
    path = os.path.join(DATA, "participants_wrong_header.csv")

    try:
        read_participants(path, 3)
    except ValueError as e:
        assert "CSV debe contener las columnas" in str(e)
    else:
        assert False, "Debe lanzar ValueError"


def test_read_participants_missing_number():
    path = os.path.join(DATA, "participants_missing_number.csv")
    rows = read_participants(path, digits=3)
    assert len(rows) == 1  # solo la fila válida
    assert rows[0] == ("333", "Valid")
