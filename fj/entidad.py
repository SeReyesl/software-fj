# entidad.py
# Base abstracta para las cosas del sistema de Software FJ.

from abc import ABC, abstractmethod


# Clase abstracta: sirve de molde, no se instancia directo.
class EntidadBase(ABC):

    # Guarda el id por dentro para que no lo toquen directo desde afuera.
    def __init__(self, id_entidad):
        self.__id = id_entidad

    # Saca el id cuando lo necesito desde otro lado.
    def get_id(self):
        return self.__id

    # Obliga a las clases que hereden a armar su propio describir.
    @abstractmethod
    def describir(self):
        pass