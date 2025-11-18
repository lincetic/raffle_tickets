from raffle_tickets.generator import generate_tickets_from_digits


def test_generate_tickets_from_digits():
    digits=3
    tickets=generate_tickets_from_digits(digits)
    assert len(tickets) == 1000
    assert tickets[0][0] == "000"
    assert tickets[-1][0] == "999"

def test_generate_tickets_1_digit():
    tickets = generate_tickets_from_digits(1)
    assert len(tickets) == 10
    assert tickets[0] == ("0".zfill(1), None)
    assert tickets[-1] == ("9".zfill(1), None)


def test_generate_tickets_4_digits():
    tickets = generate_tickets_from_digits(4)
    assert len(tickets) == 10000