import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math

def declinacion_solar(date):
  """
  Calcula la declinación solar en grados para un día juliano dado.

  Args:
    j: El día juliano (1 para el 1 de enero, etc.).

  Returns:
    La declinación solar en grados.
  """
  # El día juliano (j) se calcula como el día del año (1-365 o 1-366)
  j = date.timetuple().tm_yday
  
  q = 2 * math.pi / 366
  c1 = -22.9840
  c2 = -0.3499
  c3 = -0.1398
  d1 = 3.78720
  d2 = 0.03205
  d3 = 0.0717
  suma = (c1 * math.cos(q * j) + d1 * math.sin(q * j)) + \
         (c2 * math.cos(2 * q * j) + d2 * math.sin(2 * q * j)) + \
         (c3 * math.cos(3 * q * j) + d3 * math.sin(3 * q * j))
  delta = suma + 0.33281
  return delta


# Parámetros iniciales
lat = 40.741895   # Latitud
lon = -73.989308   # Longitud
date = datetime(2025, 7, 15) 
hours = []
for i in range(24): 
    hours.append(date + timedelta(hours=i))  

altitudes = []
for t in hours:

    hour_angle = (t.hour + t.minute/60 - 12) * 15
    decl = declinacion_solar(date)
    altitude = math.degrees(
        math.asin(math.sin(math.radians(lat)) * math.sin(math.radians(decl)) +
                  math.cos(math.radians(lat)) * math.cos(math.radians(decl)) * math.cos(math.radians(hour_angle))))
    altitudes.append(altitude)


# Graficar
plt.plot(altitudes, marker='o')
plt.xlabel("Hora del día")
plt.ylabel("Altura solar (°)")
plt.title(f"Trayectoria solar en lat:{lat:.2f}, lon:{lon:.2f} ({date.date()})")
plt.show()