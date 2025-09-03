import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math
import numpy as np

def declinacion_solar(date):
  """
  Calcula la declinación solar en grados para una fecha dada.

  Args:
    date (datetime): Fecha.

  Returns:
    float: La declinación solar en grados.
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

def ec_tiempo(date):
  """
  Calcula la ecuación del tiempo en minutos para una fecha dada.

  Args:
     date (Datetime): Fecha.

  Returns:
    float: La ecuación del tiempo.
  """
  # El día juliano (j) se calcula como el día del año (1-365 o 1-366)
  j = date.timetuple().tm_yday
  
  q = 2 * math.pi / 366
  e1 = 0.43177
  e2 = -3.1650
  e3 = 0.07272
  f1 = -7.3764
  f2 = -9.3893
  f3 = -0.24498
  suma = (e1 * math.cos(q * j) + f1 * math.sin(q * j)) + \
         (e2 * math.cos(2 * q * j) + f2 * math.sin(2 * q * j)) + \
         (e3 * math.cos(3 * q * j) + f3 * math.sin(3 * q * j))
  epsilon = suma + 0.00037
  
  return epsilon

def tiempo_solar_verdadero(fecha, longitud_sitio, meridiano_oficial):
    """
    Calcula el tiempo solar verdadero (TSV) en horas para una fecha, hora y ubicación dadas.

    Args:
        fecha (datetime): Incluye la fecha y hora local.
        longitud_sitio (float): La longitud geográfica del sitio en grados.
        meridiano_oficial (float): El meridiano oficial de la zona horaria en grados.

    Returns:
        float: El tiempo solar verdadero en horas.
    """
    # Descomponer la hora local
    Hloc = fecha.hour
    Mloc = fecha.minute
    Sloc = fecha.second
    
    # Calcular el tiempo solar verdadero
    TSV = Hloc + (Mloc / 60) + (Sloc / 3600) + (meridiano_oficial - longitud_sitio) / 15 + ec_tiempo(fecha) / 60
    
    return TSV

def angulo_horario(longitud, hora, meridiano_oficial):
    """
    Parameters
    ----------
    longitud : float
        La longitud geográfica del sitio en grados.
    hora : datetime
        Hora local.
    meridiano_oficial : float
        El meridiano oficial de la zona horaria en grados.

    Returns
    -------
    float
        El ángulo horario en radianes.

    """
    TSV = tiempo_solar_verdadero(hora, longitud, meridiano_oficial)
  
    return math.pi*(TSV-12)/12 # Ya está en radianes

def altitud_solar(latitud, longitud, fecha, omega, declinacion):
    """
    Parameters
    ----------
    latitud : float
        La latitud geográfica del sitio en GRADOS.
    longitud : float
        La longitud geográfica del sitio en GRADOS.
    fecha : datetime
        La fecha local.
    omega : float
        El ángulo horario en RADIANES.
    declinacion : float
        La declinación solar en GRADOS.

    Returns
    -------
    altitud : float
        El ángulo de altitud solar en grados.

    """
    
    altitud = math.degrees( math.asin(math.sin(math.radians(latitud)) * math.sin(math.radians(declinacion)) +
                  math.cos(math.radians(latitud)) * math.cos(math.radians(declinacion)) * math.cos(omega)))
    
    return altitud

def comprobaciones():
    
    # Parámetros iniciales
    lat = 40.435932462951065   # Latitud en grados
    lon = -3.6989564141131925   # Longitud en grados
    fecha_inicial = datetime(2025, 6, 21, 0, 0, 0) # Fecha y hora
    meridiano = 0 # Meridiano oficial de Colombia
    
    
    #### Comprobación de la declinación solar #### 
    
    # Generar datos para un año completo
    fechas = [fecha_inicial + timedelta(days=i) for i in range(365)]
    declinacion_valores = [declinacion_solar(fecha_inicial) for fecha_inicial in fechas]
    
    # Graficar
    plt.figure(figsize=(8, 5))
    plt.plot(fechas, declinacion_valores)
    plt.xlabel("Fecha")
    plt.ylabel("Declinación solar (grados)")
    plt.title("Declinación solar a lo largo de un año")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
    
    
    #### Comprobación de la ecuación de tiempo #### 
    
    ecuacion_tiempo_valores = [ec_tiempo(fecha) for fecha in fechas]
    
    # Graficar
    plt.figure(figsize=(8, 5))
    plt.plot(fechas, ecuacion_tiempo_valores)
    plt.xlabel("Fecha")
    plt.ylabel("Ecuación del tiempo (Minutos)")
    plt.title("Ecuación del tiempo a lo largo de un año")
    plt.grid(True,linestyle='--', alpha=0.6)
    plt.show()
    
    
    #### Comprobación de la altitud solar #### 
    
    # Generar 24 horas (1 día)
    horas_dia = [fecha_inicial + timedelta(hours=i) for i in range(24)]    
    
    altitudes = [altitud_solar(lat, lon, hora, angulo_horario(lon, hora, meridiano), declinacion_solar(fecha_inicial)) for hora in horas_dia]
    
    # Graficar
    plt.figure(figsize=(10, 5))
    plt.plot(horas_dia, altitudes, marker='o')
    plt.xlabel("Hora del día")
    plt.ylabel("Altura solar (°)")
    plt.title(f"Trayectoria solar en lat:{lat:.2f}, lon:{lon:.2f} ({fecha_inicial.date()})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
    
    #### Comprobación del angulo acimutal solar #### 
    angulos_acimutales = []
    # Calcular declinación y ecuación del tiempo para el día
    declinacion = declinacion_solar(fecha_inicial)
    # Simular un día completo, hora a hora
    for hora in horas_dia:  # 24 horas
    
        omega = angulo_horario(lon, hora, meridiano)
        # Ángulo cenital (theta_c)
        theta_c = angulo_cenital(lat,lon, declinacion, hora, omega)                                                                
        gamma = angulo_acimutal(lat, declinacion, omega, theta_c)
        
        angulos_acimutales.append(gamma)

    # Graficar los resultados
    plt.figure(figsize=(10, 6))
    plt.plot(angulos_acimutales)
    plt.title('Ángulo Acimutal Solar a lo largo del día')
    plt.xlabel('Hora del día (hora local)')
    plt.ylabel('Ángulo Acimutal ($\gamma$) [grados]')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(np.arange(0, 25, 2))
    plt.tight_layout()
    plt.show()
    return None

# Ecuación del ángulo cenital (theta_z)
def angulo_cenital(latitud, longitud, declinacion, hora, omega):
    """
    Calcula el ángulo cenital en radianes.
    """
    theta_z = math.acos(math.sin(math.radians(latitud)) * math.sin(math.radians(declinacion)) + \
                  math.cos(math.radians(latitud)) * math.cos(math.radians(declinacion)) * math.cos(omega))
    return math.degrees(theta_z)


def angulo_acimutal_modificado(latitud, declinacion, omega, theta_c):
    """
    Calcula el ángulo acimutal modificado (gamma_prima) en radianes.

    Args:
        latitud (float): Latitud en radianes.
        declinacion (float): Declinación solar en radianes.
        omega (float): Ángulo horario en radianes.

    Returns:
        float: El ángulo acimutal modificado en radianes.
    """
    # Cálculo de gamma_prima
    gamma_prima = math.asin((math.cos(math.radians(declinacion)) * math.sin(omega))/math.sin(math.radians(theta_c)))
    return gamma_prima

def angulo_acimutal(phi, delta, omega, theta_c):
    """
    Calcula el ángulo acimutal (gamma) en grados para una fecha, hora y ubicación dadas.

    Args:
        phi (float): Latitud en grados.
        delta (float): Declinación solar en grados.
        omega (float): Ángulo horario en grados.

    Returns:
        float: El ángulo acimutal en grados.
    """
    gamma_prima = angulo_acimutal_modificado(phi, delta, omega, theta_c)


    # Coeficientes C1, C2 y C3

    if abs(delta) < abs(phi):         
        # Ángulo horario modificado (omega_w)
        omega_w = math.acos(math.tan(math.radians(delta)) / math.tan(math.radians(phi)))

        C1 = (omega_w - abs(omega)) / (omega_w - abs(omega))     
    else: C1 = 1
    C2 = (phi - delta) / abs(phi - delta)
    C3 = omega / abs(omega)

    # Ecuación del ángulo acimutal
    gamma = C1 * C2 * gamma_prima + (180 * C3 * (1 - C1*C2)/2)
    return math.degrees(gamma)

if __name__ == "__main__":
    comprobaciones()