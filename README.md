🎟️ Raffle Tickets Generator

Generador de papeletas de sorteo (tipo Lotería de Navidad) con soporte para:

✔ Generar papeletas automáticas a partir del número de cifras
✔ Importar participantes desde CSV (nombre, numero)
✔ Incluir logo, imagen de cesta y QR codes de verificación
✔ Papeletas recortables con zona para organización y zona para el participante
✔ Diseño compatible con impresión en A4 (vertical u horizontal)
✔ Totalmente ejecutable vía CLI

📦 Instalación

Clona el repositorio:

git clone https://github.com/lincetic/raffle-tickets.git
cd raffle-tickets


Crea un entorno virtual (opcional pero recomendado):

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


Instala dependencias:

pip install -r requirements.txt

🚀 Uso desde la línea de comandos (CLI)

Ejemplo básico:

python -m raffle_tickets --digits 3


Genera 000-999 (1000 tickets) y los exporta a tickets.pdf.

📥 1. Con CSV de participantes

Formato obligatorio:

nombre	numero
Juan Pérez	25
Marta López	007

El número se rellenará automáticamente (zfill) según las cifras del sorteo.

Ejemplo:

python -m raffle_tickets --input participantes.csv --digits 3

🔧 2. Otros argumentos
Parámetro	Descripción
--digits N	Cifras del número del sorteo (1–4)
--logo logo.png	Imagen para el logo (opcional)
--basket cesta.png	Imagen de cesta de Navidad (opcional)
--out salida.pdf	Nombre del PDF final
--orientation A4 / landscape	Orientación de la página

Ejemplo completo:

python -m raffle_tickets \
   --input participantes.csv \
   --digits 3 \
   --logo logo.png \
   --basket basket.png \
   --out navidad2025.pdf \
   --orientation landscape

📄 Funcionamiento interno
1. read_participants()

Lee un CSV con las columnas:

nombre

numero

Corrige BOM (utf-8-sig), detecta separadores con csv.Sniffer e ignora filas vacías.

Devuelve:

[("025", "Juan Pérez"), ("007", "Ana García"), ...]

2. generate_tickets_from_digits()

Genera TODOS los números posibles de:

1 cifra → 0–9

2 cifras → 00–99

3 cifras → 000–999

4 cifras → 0000–9999

Devuelve:

[("000", None), ("001", None), ..., ("999", None)]

3. render_tickets_pdf()

Crea un PDF con:

Diseño A4 o apaisado

Cálculo dinámico del número de tickets por página

Corte vertical punteado

Logo escalado por altura fija

Imagen de cesta escalada por altura fija

Texto multilínea

Nombre del participante en vertical

Dos QR codes por papeleta

Fecha automática del sorteo

4. draw_ticket()

Dibuja cada entrada:

Marco del ticket

Línea punteada de separación

Logo arriba y abajo

Cesta en la esquina

Título

Descripción multilínea

Número #XYZ

Nombre del participante rotado 90°

Dos QR con payload:

?{ticket_id} - {key_secret}

5. add_image()

Carga y escala imágenes según altura en centímetros, manteniendo proporciones usando DPI reales o por defecto (72).

6. make_qr_image()

Genera un QR cuadrado usando qrcode y lo devuelve como ImageReader.

🧪 Tests incluidos
tests/
.
├── test_digits_generator.py
├── test_cli.py
├── test_cesv_reader.py
├── test_pdf_renderer.py

📄 Ejemplo de salida (estructura del PDF)

Cada hoja incluye:

6 papeletas en horizontal (o las que quepan)

Zona de corte

Logo arriba y abajo

Cesta a la derecha

Texto multilínea

QR en dos partes

Información del sorteo

📂 Estructura del proyecto
raffle_tickets/
.
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── pytest.ini
│
├── logo.png                 # Imagen opcional para el logo
├── basket.png               # Imagen opcional de la cesta
├── participantes.csv        # Ejemplo de archivo de entrada
├── tickets.pdf              # Ejemplo de PDF generado
│
├── docs/                    # Documentación adicional
│
├── src/
│   └── raffle_tickets/
│       ├── __init__.py
│       ├── cli.py           # Entrada CLI
│       ├── generator.py     # Lectura CSV y lógica del sorteo
│       ├── pdf_renderer.py  # Creación del PDF
│       └── ...              # Otros módulos si los añades
│
└── tests/
    ├── test_digits_generator.py
    ├── ...                  # Más tests

📜 Licencia

MIT — úsalo libremente en cualquier proyecto.