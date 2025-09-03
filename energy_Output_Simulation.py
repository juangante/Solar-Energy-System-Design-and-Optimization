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
    omega = np.deg2rad(classproject1.angulo_horario(lon, date, standard_meridian))  
    
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
lat, lon = 13.268488823253558,-75.56770800028933
mer = -75.0
beta, gamma = 20, 180  # panel inclinado 20°, mirando al sur
eta, A = 0.18, 1.6     # eficiencia 18%, área 1.6 m²

date = datetime(2025, 8, 21, 0, 0)  # 21 de marzo
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
plt.plot([h.hour for h in hours], Power, marker='o')
plt.xlabel("Hora del día")
plt.ylabel("Potencia generada (W)")
plt.title(f"Simulación FV  /  lat: {lat:.2f}°, lon: {lon:.2f}°")
plt.grid(True)
plt.show()
