import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import classproject1

# -------------------------------
# Funciones de geometría solar
# -------------------------------
def day_of_year(date):
    return date.timetuple().tm_yday

def solar_angles(lat, lon, date, standard_meridian=0):
    # Declinación solar
    delta = classproject1.declinacion_solar(date)
    
    # Ángulo horario (radianes)
    omega = classproject1.angulo_horario(lon, date, standard_meridian)  
    
    # Ángulo cenital
    theta_z = classproject1.angulo_cenital(lat, lon, delta, date, omega)
    
    # Altura solar
    alpha = classproject1.altitud_solar(lat, lon, date, omega, delta)

    return theta_z, alpha, omega, delta

# -------------------------------
# Modelo A: Irradiancias
# -------------------------------
def air_mass(theta_z):
    if theta_z >= 90:  # Sol bajo el horizonte
        return np.inf
    return 1 / (np.cos(np.radians(theta_z)) + 0.50572 * (96.07995 - theta_z) ** -1.6364)

def irradiance_clear_sky(theta_z, n, Tb=0.7, cd=0.75, Gsc=1367):
    # Irradiancia extraterrestre normal
    E0 = 1 + 0.033 * np.cos(np.radians(360 * n / 365))
    I0n = Gsc * E0

    if theta_z >= 90:
        return 0, 0, 0  # de noche

    m = air_mass(theta_z)

    DNI = I0n * Tb**m
    DHI = cd * I0n * (1 - Tb**m)
    GHI = DHI + DNI * np.cos(np.radians(theta_z))

    return DNI, DHI, GHI

# -------------------------------
# Irradiancia en el plano del panel
# -------------------------------
def panel_irradiance(DNI, DHI, GHI, theta_z, theta_s, beta, gamma, rho=0.2):
    # Ángulo de incidencia (AOI)
    AOI = np.degrees(np.arccos(
        np.cos(np.radians(theta_z)) * np.cos(np.radians(beta)) +
        np.sin(np.radians(theta_z)) * np.sin(np.radians(beta)) *
        np.cos(np.radians(theta_s - gamma))
    ))

    Eb = DNI * max(0, np.cos(np.radians(AOI)))  # Directa en panel
    Ed = DHI * (1 + np.cos(np.radians(beta))) / 2  # Difusa isotrópica
    Er = GHI * rho * (1 - np.cos(np.radians(beta))) / 2  # Reflejada

    return Eb + Ed + Er, Eb, Ed, Er

# -------------------------------
# Ejemplo
# -------------------------------
lat = int(input("\nIngrese la latitud en grados (°): "))
lon = int(input("\nIngrese la longitud en grados (°): "))
mer = int(input("\nIngrese el meridiano oficial en grados (°): "))
beta = int(input("\nIngrese la inclinación del panel en grados (°): "))
gamma = int(input("\nIngrese la dirección del panel con respecto al sol en grados (°): "))
eta = int(input("\nIngrese la eficiencia del panel (%): "))
A = int(input("\nIngrese el área del panel (m^2): "))    

ano = int(input("\nIngrese el año: "))
mes = int(input("\nIngrese el mes: "))
dia = int(input("\nIngrese el día: "))
date = datetime(ano, mes, dia, 0, 0)
hours = [date + timedelta(hours=i) for i in range(24)]  # 24 horas

POA, Power = [], []
for h in hours:
    theta_z, alpha, omega, delta = solar_angles(lat, lon, h, mer)
    DNI, DHI, GHI = irradiance_clear_sky(theta_z, day_of_year(h))
    
    # Necesitamos acimut solar
    theta_s = classproject1.angulo_acimutal(lat, delta, omega, theta_z)
    
    Epoa, Eb, Ed, Er = panel_irradiance(DNI, DHI, GHI, theta_z, theta_s, beta, gamma)
    P = eta * A * Epoa
    
    POA.append(Epoa)
    Power.append(P)

# -------------------------------
# Gráfica
# -------------------------------
    plt.figure(figsize=(8, 5))
plt.plot([h.hour for h in hours], Power, marker='o')
plt.xlabel("Hora del día")
plt.ylabel("Potencia generada (W)")
plt.title(f"Simulación FV  /  lat: {lat:.2f}°, lon: {lon:.2f}°")
plt.grid(True)
plt.show()

plt.close()