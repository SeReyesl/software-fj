# servicios.py
# Clase abstracta Servicio y los tres tipos de servicio para Software FJ.

from abc import ABC, abstractmethod
from fj.entidad import EntidadBase
from fj.excepciones import (DatoInvalidoError, ParametroFaltanteError,
                            CalculoInconsistenteError)
from fj.logger import logger


class Servicio(EntidadBase, ABC):

    def __init__(self, id_servicio, nombre, tarifa, disponible=True):
        super().__init__(id_servicio)
        # Si no mandan nombre, corto de una vez.
        if nombre is None or str(nombre).strip() == "":
            raise ParametroFaltanteError("El servicio necesita un nombre")
        # La tarifa no puede ser cero ni negativa.
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatoInvalidoError("La tarifa debe ser un numero mayor que 0")
        self.nombre = str(nombre).strip()
        self.tarifa = tarifa
        self.disponible = disponible

    # Cada clase hija define su propio calculo y validacion.
    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    # Uso parametros opcionales para simular sobrecarga en impuestos y descuentos.
    def calcular_total(self, duracion, impuesto=0.0, descuento=0.0):
        self.validar_parametros(duracion)
        if impuesto < 0 or impuesto > 1:
            raise CalculoInconsistenteError("El impuesto debe estar entre 0 y 1")
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 1 (sin incluir 1)")
        costo = self.calcular_costo(duracion)
        # Primero aplico descuento y luego impuesto sobre lo que queda.
        total = costo - costo * descuento
        total = total + total * impuesto
        if total <= 0:
            raise CalculoInconsistenteError("El total calculado no es valido")
        return round(total, 2)


# Salas: se cobran por hora y tienen limite de horas por reserva.
class ReservaSala(Servicio):

    def __init__(self, id_servicio, nombre, tarifa, capacidad, disponible=True):
        super().__init__(id_servicio, nombre, tarifa, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero mayor que 0")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion < 1 or duracion > 12:
            raise DatoInvalidoError("La sala se reserva entre 1 y 12 horas")

    def calcular_costo(self, duracion):
        return self.tarifa * duracion

    def describir(self):
        return f"Sala {self.nombre} (capacidad {self.capacidad}), ${self.tarifa} por hora"


# Equipos: se cobran por dia y llevan deposito aparte.
class AlquilerEquipo(Servicio):

    def __init__(self, id_servicio, nombre, tarifa, deposito, disponible=True):
        super().__init__(id_servicio, nombre, tarifa, disponible)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise DatoInvalidoError("El deposito no puede ser negativo")
        self.deposito = deposito

    def validar_parametros(self, duracion):
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise DatoInvalidoError("El equipo se alquila entre 1 y 30 dias")

    def calcular_costo(self, duracion):
        return self.tarifa * duracion + self.deposito

    def describir(self):
        return f"Equipo {self.nombre}, ${self.tarifa} por dia, deposito ${self.deposito}"


# Asesorias: multiplican la tarifa base segun el nivel elegido.
class Asesoria(Servicio):

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, id_servicio, nombre, tarifa, nivel, disponible=True):
        super().__init__(id_servicio, nombre, tarifa, disponible)
        if nivel not in Asesoria.NIVELES:
            raise DatoInvalidoError("El nivel debe ser junior, senior o experto")
        self.nivel = nivel

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion < 1 or duracion > 8:
            raise DatoInvalidoError("La asesoria dura entre 1 y 8 horas")

    def calcular_costo(self, duracion):
        return self.tarifa * duracion * Asesoria.NIVELES[self.nivel]

    def describir(self):
        return f"Asesoria {self.nombre} nivel {self.nivel}, ${self.tarifa} por hora"