# reserva.py
# Une cliente, servicio, duracion y estado para las reservas de Software FJ.

from fj.entidad import EntidadBase
from fj.excepciones import (ReservaInvalidaError, OperacionNoPermitidaError,
                            ServicioNoDisponibleError, CalculoInconsistenteError,
                            DatoInvalidoError, ParametroFaltanteError)
from fj.logger import logger


class Reserva(EntidadBase):

    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        # Sin cliente o sin servicio no puedo armar nada.
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva necesita cliente y servicio")
        # Si el servicio esta apagado o no disponible, tampoco se deja crear.
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio " + servicio.nombre + " no esta disponible")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.costo = None

    # Pasa a confirmada solo si aun esta pendiente.
    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError("Solo se confirma una reserva pendiente, estado actual: " + self.estado)
        self.estado = "CONFIRMADA"
        logger.info("Reserva %s confirmada", self.get_id())

    # Cancela la reserva; si ya estaba cancelada, lanzo error.
    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada")
        self.estado = "CANCELADA"
        logger.info("Reserva %s cancelada", self.get_id())

    # Calcula el total y confirma usando try/except/else/finally.
    def procesar(self, impuesto=0.0, descuento=0.0):
        try:
            costo = self.servicio.calcular_total(self.duracion, impuesto, descuento)
        except (DatoInvalidoError, CalculoInconsistenteError) as e:
            # Anoto el fallo en el log y encadeno con from para dar contexto claro.
            logger.error("Fallo al procesar reserva %s: %s", self.get_id(), e)
            raise ReservaInvalidaError("No se pudo procesar la reserva") from e
        else:
            # Solo entra aqui cuando calcular_total salio bien.
            self.costo = costo
            self.confirmar()
            return costo
        finally:
            # Siempre dejo constancia de que termino este intento.
            logger.info("Fin del procesamiento de la reserva %s", self.get_id())

    def describir(self):
        return (f"Reserva {self.get_id()}: {self.cliente.nombre} -> "
                f"{self.servicio.nombre}, duracion {self.duracion}, estado {self.estado}")