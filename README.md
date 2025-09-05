# Simulación de Sistema Fotovoltaico

Este proyecto implementa en **Python** una simulación sencilla de generación fotovoltaica a partir de la geometría solar y modelos básicos de irradiancia.  
El código calcula la posición del Sol en función de la fecha, la hora y la ubicación geográfica, estima la irradiancia en el plano de un panel solar y finalmente determina la potencia eléctrica producida por el mismo.

---

## 📂 Estructura del proyecto

- `classproject1.py`  
  Contiene las funciones relacionadas con la geometría solar (declinación, ángulo horario, ángulo cenital, altitud, acimutal, etc.).

- `energy_Output_Simulation.py`  
  Utiliza las funciones anteriores para calcular irradiancia (DNI, DHI, GHI), proyectarlas sobre un panel con orientación e inclinación definida y calcular la potencia generada.  
  Además, genera gráficas de la curva diaria de potencia.

---

## ⚙️ Dependencias

El proyecto requiere **Python 3.8 o superior** y las siguientes librerías:

- `numpy`
- `matplotlib`
- `datetime`
