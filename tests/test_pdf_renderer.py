import os
from raffle_tickets.pdf_renderer import render_tickets_pdf

def test_pdf_generation_tmp(tmp_path):
    output = tmp_path / "test.pdf"
    tickets = [("001", "Ana"), ("002", "Luis")]

    render_tickets_pdf(tickets, str(output), per_page=6)

    assert output.exists()
    assert output.stat().st_size > 1000
