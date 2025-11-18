## Requisitos funcionales (MVP)

1. El sistema debe generar papeletas de sorteo para una cesta de Navidad.

2. Cada papeleta llevará:

    - un número único (p. ej. 0001),

    - el nombre del participante (opcional),

    - un código QR que represente el ID / URL de verificación,

    - un diseño imprimible (PDF o PNG) listo para imprimir varias por página.

3. Entrada esperada:

    - lista de participantes (CSV o texto con nombres),

    - número de papeletas por participante (p. ej. 1..N),

    - plantilla/tema (opcional).

4. Salida:

    - archivo PDF con N papeletas (configurable por página),

    - o una carpeta con PNGs individuales.

5. CLI básica: python -m papeletas generate --input participantes.csv --out tickets.pdf --per-page 6

## Requisitos no funcionales

    - Código en Python 3.10+.

    - Uso de virtualenv/poetry para gestionar dependencias.

    - Tests automatizados con pytest.

    - Formato de código con black y lint con flake8/isort.

    - CI: GitHub Actions que ejecuta tests y lint en cada PR.

    - Licencia MIT.

    - Documentación básica en README y ejemplos.

## Casos de uso (user stories) y criterios de aceptación

    - Como organizador quiero generar papeletas en PDF para imprimir, aceptación: puedo pasar --input y obtengo tickets.pdf.

    - Como organizador quiero QR por ticket para verificar, aceptación: cada ticket contiene QR con el numero y un codigo.