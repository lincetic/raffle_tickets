# 🎟️ Raffle Tickets Generator

Generador de papeletas de sorteo (tipo Lotería de Navidad) con soporte para:

- ✔ Generar papeletas automáticas a partir del número de cifras  
- ✔ Importar participantes desde CSV (nombre, número)  
- ✔ Incluir logo, imagen de cesta y QR codes de verificación  
- ✔ Papeletas recortables con zona para organización y zona para el participante  
- ✔ Diseño compatible con impresión en A4 (vertical u horizontal)  
- ✔ Totalmente ejecutable vía CLI  

---

## 📦 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/lincetic/raffle_tickets.git
cd raffle_tickets
```

### 2. Crea un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Instala el paquete

**Opción A: Instalación en modo desarrollo (recomendado para desarrollo)**

```bash
pip install -e .
```

**Opción B: Instalación desde archivo de requisitos**

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso desde la línea de comandos (CLI)

### Como comando ejecutable (después de instalar con `pip install -e .`)

Una vez instalado el paquete en modo desarrollo, puedes usar el comando `raffle-tickets` directamente:

```bash
raffle-tickets --digits 3
```

Genera **000–999** (1000 tickets) y los exporta a `tickets.pdf`.

### Alternativa: Usando `python -m`

También puedes ejecutar el módulo directamente sin necesidad de instalación:

```bash
python -m raffle_tickets --digits 3
```

---

## 📥 Uso con CSV de participantes

### Formato obligatorio

```csv
nombre,numero
Juan Pérez,25
Marta López,007
```

El número se rellenará automáticamente (`zfill`) según las cifras del sorteo.

### Ejemplo

```bash
raffle-tickets --input participantes.csv --digits 3
```

O usando `python -m`:

```bash
python -m raffle_tickets --input participantes.csv --digits 3
```

---

## 🔧 Argumentos disponibles

| Parámetro | Descripción |
|----------|-------------|
| `--digits N` | Cifras del número del sorteo (1–4) |
| `--input archivo.csv` | CSV con nombre y número |
| `--logo logo.png` | Imagen opcional para el logo |
| `--basket cesta.png` | Imagen opcional para la cesta |
| `--out salida.pdf` | Nombre del PDF final |
| `--orientation A4 / landscape` | Orientación del documento |

### Ejemplo completo (con `raffle-tickets`)

```bash
raffle-tickets \
   --input participantes.csv \
   --digits 3 \
   --logo logo.png \
   --basket basket.png \
   --out navidad2025.pdf \
   --orientation landscape
```

---

## 📄 Funcionamiento interno

### 1. `read_participants()`

- Lee un CSV con columnas `nombre` y `numero`
- Detecta delimitador con `csv.Sniffer`
- Maneja archivos con BOM (`utf-8-sig`)
- Ignora filas inválidas

Ejemplo de retorno:

```
[("025", "Juan Pérez"), ("007", "Ana García"), ...]
```

---

### 2. `generate_tickets_from_digits()`

Genera todos los números posibles:

- 1 cifra → 0–9  
- 2 cifras → 00–99  
- 3 cifras → 000–999  
- 4 cifras → 0000–9999  

---

### 3. `render_tickets_pdf()`

Construye el PDF:

- Diseño A4 o apaisado  
- Cálculo automático de cuántos tickets caben por página  
- Línea punteada de corte  
- Logo escalado  
- Cesta escalada  
- Texto multilínea  
- QR codes  
- Fecha automática  

---

### 4. `draw_ticket()`

Dibuja cada papeleta:

- Marco del ticket  
- Línea vertical punteada  
- Logo arriba y abajo  
- Cesta a la derecha  
- Título y descripción  
- Número `#XYZ`  
- Nombre del participante rotado 90º  
- Dos QR con payload:  

```
?{ticket_id} - {key_secret}
```

---

### 5. `add_image()`

Carga y escala imágenes manteniendo proporciones según altura en cm.

---

### 6. `make_qr_image()`

Genera un QR utilizando la librería `qrcode`.

---

## 🧪 Tests incluidos

```
tests/
├── test_digits_generator.py
├── test_cli.py
├── test_csv_reader.py
├── test_pdf_renderer.py
```

---

## 📂 Estructura del proyecto

```
raffle_tickets/
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── pytest.ini
│
├── logo.png
├── basket.png
├── participantes.csv
├── tickets.pdf
│
├── docs/
│
├── src/
│   └── raffle_tickets/
│       ├── __init__.py
│       ├── cli.py
│       ├── generator.py
│       ├── pdf_renderer.py
│       └── ...
│
└── tests/
    ├── test_digits_generator.py
    └── ...
```

---

## 📜 Licencia

**MIT License** — libre para usar, modificar y distribuir.
