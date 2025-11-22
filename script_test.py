# Prueba manual en Python
from flask_app.models.partido import Partido
from flask_app.models.reserva import Reserva

# Ver partido antes de eliminar
partido = Partido.obtener_por_id(1)
print(f"Partido ID: {partido.id_partido}, Reserva ID: {partido.id_reserva}")

# Eliminar
resultado = Partido.eliminar(1)
print(f"Resultado eliminación: {resultado}")

# Verificar que se eliminó la reserva
if partido.id_reserva:
    reserva = Reserva.obtener_por_id(partido.id_reserva)
    print(f"Reserva existe después de eliminar: {reserva is not None}")