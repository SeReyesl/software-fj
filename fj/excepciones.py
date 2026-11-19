# excepciones.py
# Errores propios para el sistema de Software FJ.
# Todos salen de ErrorFJ para atrapar todo lo del proyecto o revisar cada fallo por aparte.


class ErrorFJ(Exception):
    # Error base del sistema.
    pass


class DatoInvalidoError(ErrorFJ):
    # Cuando llega un dato con formato raro o que no sirve.
    pass


class ParametroFaltanteError(ErrorFJ):
    # Falta algún dato obligatorio para seguir.
    pass


class OperacionNoPermitidaError(ErrorFJ):
    # Intentan hacer algo que no aplica en este estado.
    pass


class ServicioNoDisponibleError(ErrorFJ):
    # El servicio no está libre o no se puede usar ahorita.
    pass


class ReservaInvalidaError(ErrorFJ):
    # Problema al crear o procesar una reserva.
    pass


class CalculoInconsistenteError(ErrorFJ):
    # El cálculo del costo dio mal o salió negativo.
    pass