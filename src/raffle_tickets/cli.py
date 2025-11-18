import argparse
import sys

from .generator import read_participants, generate_tickets_from_digits
from .pdf_renderer import render_tickets_pdf


def main():
    parser = argparse.ArgumentParser(
        prog="raffle_tickets",
        description="Generar papeletas de sorteo"
    )

    parser.add_argument(
        "--input", "-i",
        help="CSV con participantes (columnas: nombre, numero)"
    )

    parser.add_argument(
        "--digits", "-d",
        type=int,
        choices=range(1, 5),
        default=3,
        help="Número de cifras del sorteo (1–4). Por defecto: 3."
    )

    parser.add_argument(
        "--out", "-o",
        default="tickets.pdf",
        help="PDF de salida"
    )

    parser.add_argument(
        "--logo",
        help="Ruta del archivo de logo (opcional)"
    )

    parser.add_argument(
        "--basket",
        help="Ruta de la imagen de la cesta (opcional)"
    )

    parser.add_argument(
        "--orientation",
        choices=["A4", "landscape"],
        default="A4",
        help="Orientación del PDF: A4 (vertical) o landscape (horizontal)"
    )

    args = parser.parse_args()

    # Generar tickets
    try:
        if args.input:
            tickets = read_participants(args.input, args.digits)
        else:
            tickets = generate_tickets_from_digits(args.digits)
    except Exception as e:
        print(f"❌ Error leyendo participantes: {e}")
        sys.exit(1)

    # Renderizar PDF
    try:
        print("📄 Generando PDF...")
        render_tickets_pdf(
            tickets,
            args.out,
            logo_path=args.logo,
            basket_path=args.basket,
            orientation=args.orientation,
        )
        print(f"✅ Generados {len(tickets)} tickets en '{args.out}'")
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
