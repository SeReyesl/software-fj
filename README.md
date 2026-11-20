# software-fj
Sistema integral de gestión de clientes, servicios y reservas - Programación 213023
# Software FJ - Sistema integral de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 - Prácticas simuladas del curso Programación (213023), Universidad Nacional Abierta y a Distancia (UNAD), programa de Ingenieria de Sistemas.

## Descripcion

Aplicacion en Python, orientada a objetos y sin base de datos, que gestiona clientes, servicios y reservas para la empresa Software FJ. La empresa maneja tres servicios: reserva de salas, alquiler de equipos y asesorias especializadas.

El programa busca mantenerse estable durante la ejecucion: si pasa algo mal datos invalidos, servicio no disponible, operacion no permitida, etc., lo captura, lo anota en el archivo de log y sigue corriendo sin caerse.

## Requisitos

- Python 3.12 o superior.
- No necesita librerias externas; solo usa modulos estandar (`abc`, `logging`, `os`)[cite: 4].

## Estructura del proyecto

```text
software-fj/
├── main.py              # simulacion de 11 operaciones
├── README.md
├── .gitignore
├── logs/
│   └── sistema.log      # registro de eventos y errores
└── fj/
    ├── __init__.py
    ├── excepciones.py   # excepciones personalizadas
    ├── logger.py        # configuracion del archivo de log
    ├── entidad.py       # clase abstracta EntidadBase
    ├── cliente.py       # clase Cliente
    ├── servicios.py     # clase abstracta Servicio y 3 servicios
    └── reserva.py       # clase Reserva
