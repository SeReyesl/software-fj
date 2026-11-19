# main.py
# Pruebas con 11 operaciones para Software FJ, sin usar base de datos.
# Cada paso va en try/except para que el programa no se caiga si algo falla.

from fj.cliente import Cliente
from fj.servicios import ReservaSala, AlquilerEquipo, Asesoria
from fj.reserva import Reserva
from fj.excepciones import ErrorFJ
from fj.logger import logger

# Listas en memoria para guardar lo que se crea durante la corrida.
clientes = []
servicios = []
reservas = []

exitos = 0
fallos = 0


def operacion(numero, descripcion, funcion):
    # Corre una prueba y atrapa errores esperados o inesperados.
    global exitos, fallos
    print(f"\n[{numero}] {descripcion}")
    try:
        resultado = funcion()
    except ErrorFJ as e:
        fallos += 1
        logger.error("Operacion %s fallo: %s", numero, e)
        print("   ERROR controlado:", e)
    except Exception as e:
        # Si sale otro fallo distinto, tambien queda anotado en el log.
        fallos += 1
        logger.error("Error inesperado en operacion %s: %s", numero, e)
        print("   ERROR inesperado:", e)
    else:
        exitos += 1
        logger.info("Operacion %s exitosa", numero)
        print("   OK:", resultado)
    finally:
        logger.info("Termina operacion %s", numero)


def crear_cliente(*datos):
    c = Cliente(*datos)
    clientes.append(c)
    return c.describir()


def crear_servicio(clase, *datos):
    s = clase(*datos)
    servicios.append(s)
    return s.describir()


def crear_reserva(id_r, cliente, servicio, duracion, **extra):
    r = Reserva(id_r, cliente, servicio, duracion)
    costo = r.procesar(**extra)
    reservas.append(r)
    return f"{r.describir()} | costo ${costo}"


def cancelar_dos_veces():
    r = reservas[0]
    r.cancelar()
    r.cancelar()  # La segunda vez debe lanzar error.
    return "no deberia llegar aqui"


logger.info("===== INICIO DE LA SIMULACION =====")

operacion(1, "Cliente valido", lambda: crear_cliente(1, "Ana Torres", "1098765432", "ana@correo.com", "3101234567"))
operacion(2, "Cliente con email invalido", lambda: crear_cliente(2, "Luis Perez", "1090000001", "luis-correo.com", "3109876543"))
operacion(3, "Cliente con documento vacio", lambda: crear_cliente(3, "Marta Diaz", "", "marta@correo.com", "3115556677"))
operacion(4, "Sala valida", lambda: crear_servicio(ReservaSala, 10, "Sala Norte", 50000, 12))
operacion(5, "Equipo con tarifa negativa", lambda: crear_servicio(AlquilerEquipo, 11, "Proyector", -20000, 100000))
operacion(6, "Asesoria valida", lambda: crear_servicio(Asesoria, 12, "Asesoria en Python", 80000, "senior"))
operacion(7, "Reserva exitosa (sala 3 horas con IVA 19%)", lambda: crear_reserva(100, clientes[0], servicios[0], 3, impuesto=0.19))
operacion(8, "Reserva con duracion 0", lambda: crear_reserva(101, clientes[0], servicios[0], 0))
operacion(9, "Reserva de servicio no disponible", lambda: crear_reserva(102, clientes[0], Asesoria(13, "Asesoria IA", 90000, "experto", disponible=False), 2))
operacion(10, "Cancelar una reserva dos veces", cancelar_dos_veces)
operacion(11, "Descuento mayor al 100%", lambda: crear_reserva(103, clientes[0], servicios[1], 2, descuento=1.5))

print("\n===== RESUMEN =====")
print("Clientes:", len(clientes), "| Servicios:", len(servicios), "| Reservas:", len(reservas))
print("Operaciones exitosas:", exitos, "| Con error controlado:", fallos)
print("Revisa el archivo logs/sistema.log")
logger.info("===== FIN DE LA SIMULACION: %s exitosas, %s fallidas =====", exitos, fallos)