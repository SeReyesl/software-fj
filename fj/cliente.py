# cliente.py
# Manejo de clientes para Software FJ, guardando los datos privados y validando entradas.

from fj.entidad import EntidadBase
from fj.excepciones import DatoInvalidoError, ParametroFaltanteError
from fj.logger import logger


class Cliente(EntidadBase):

    def __init__(self, id_cliente, nombre, documento, email, telefono):
        # Mando el id a EntidadBase para no repetir esa parte.
        super().__init__(id_cliente)
        # Paso por las propiedades para que valide antes de guardar.
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
        logger.info("Cliente registrado: %s", self.nombre)

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Si viene vacio o puro espacio, lanzo error de parametro faltante.
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("Falta el nombre del cliente.")
        # Un nombre no deberia traer numeros.
        if any(c.isdigit() for c in str(valor)):
            raise DatoInvalidoError("El nombre no puede llevar numeros.")
        self.__nombre = str(valor).strip()

    # ---------- documento ----------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("Falta el numero de documento.")
        # Solo acepto digitos para el documento.
        if not str(valor).strip().isdigit():
            raise DatoInvalidoError("El documento solo debe tener numeros.")
        self.__documento = str(valor).strip()

    # ---------- email ----------
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("Falta el correo electronico.")
        correo = str(valor).strip()
        # Reviso que tenga @ y al menos un punto despues del arroba.
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise DatoInvalidoError("El correo no parece valido.")
        self.__email = correo

    # ---------- telefono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("Falta el telefono.")
        tel = str(valor).strip()
        # Que sean numeros y tenga entre 7 y 10 digitos.
        if not tel.isdigit() or not (7 <= len(tel) <= 10):
            raise DatoInvalidoError("El telefono debe tener entre 7 y 10 digitos.")
        self.__telefono = tel

    # Implemento describir() que quedo pendiente desde EntidadBase.
    def describir(self):
        return f"Cliente #{self.get_id()} - {self.nombre} | Doc: {self.documento} | Correo: {self.email}"