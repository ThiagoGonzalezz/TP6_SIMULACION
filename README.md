# Simulación de Políticas de Descuento y Gestión de Repartidores para Glovo India

Este repositorio contiene el desarrollo del Trabajo Práctico Nº6 de la materia **Simulación** (UTN FRBA), enfocado en la gestión óptima de políticas de descuento y repartidores para maximizar la rentabilidad y la satisfacción del usuario en la empresa Glovo, utilizando un dataset real de India.

## Descripción General

El objetivo principal es modelar, simular y analizar el impacto de diferentes políticas de asignación de repartidores y descuentos sobre el negocio y los usuarios. El trabajo parte de un escenario donde la gerencia busca minimizar costos con pocos repartidores, lo que genera demoras y arrepentimiento de usuarios. Se estudian alternativas que incluyen aumentar la cantidad de trabajadores y aplicar descuentos, evaluando los efectos en:

- **Ganancia Neta**
- **Satisfacción del Usuario**
- **Arrepentimiento de Usuario**
- **Rentabilidad vs. Experiencia**

La simulación se realiza evento a evento, considerando el tiempo comprometido de los repartidores y una rutina de arrepentimiento de usuarios ante grandes demoras.

## Estructura del Repositorio

- **FDPS/**  
  Resultados del ajuste de funciones de densidad de probabilidad (fdp) para los modelos de simulación:
  - `DE/`  
    - `exponweib.txt`: Parámetros de la mejor distribución ajustada para la distancia de entrega.
    - `exponweib.jpg`: Gráfico de la fdp ajustada.
    - `histograma.jpg`: Histograma de distancias de entrega.
  - `IP/`
    - `weibull_min`: Parámetros de la mejor distribución ajustada para el intervalo entre pedidos.
    - `weibull_min.jpg`: Gráfico de la fdp ajustada.
    - `histograma.jpg`: Histograma de intervalos entre pedidos.

- **Presentación**  
  Archivo con la exposición utilizada para la defensa del trabajo.

- **Diagrama**  
  Imagen/esquema del diagrama de la simulación evento a evento y flujo de arrepentimiento.

- **TP 6 - Análisis Previo (1).txt**  
  Documento con la definición de variables, eventos y estructura de la simulación.

- **formato_papers_estudiantes (3).txt**  
  Formato requerido para la presentación del paper académico.

- **PAPER_EXAMPLE.txt**  
  Ejemplo de paper de simulación para referencia en la redacción.

## Metodología

- **Simulación Evento a Evento:**  
  El tiempo avanza hasta el próximo evento relevante (llegada de pedido, entrega, arrepentimiento).
- **Modelado de Variables:**  
  - Exógenas: Datos de entrada (intervalo entre pedidos, tiempo de entrega, precio, distancia).
  - De Control: Cantidad de repartidores, intervalo de descuento.
  - Endógenas: Estado y resultados (tiempo comprometido, espera, ociosidad, satisfacción, ganancia, arrepentimiento).
- **Ajuste con Distribuciones:**  
  Las FDPS se ajustan a los datos reales para intervalos y distancias, permitiendo una simulación representativa.

## Escenarios Analizados

1. **Escenario Actual:**  
   Gerencia minimiza costos con pocos repartidores. Alta tasa de arrepentimiento por demoras.
2. **Maximización de Ganancia Neta:**  
   Balance entre costos de repartidores/descuentos y utilidad.
3. **Maximización de Satisfacción de Usuario:**  
   Optimización con feedback por tiempo de espera y entrega.
4. **Maximización Dual:**  
   Estrategias que buscan simultáneamente la mejor experiencia y la mayor rentabilidad.

## Archivos Clave

- `FDPS/DE/exponweib.txt`, `.jpg`, `FDPS/IP/weibull_min`, `.jpg`, `histograma.jpg`: Ajuste y visualización de distribuciones.
- `TP 6 - Análisis Previo (1).txt`: Estructura y variables del modelo.
- `formato_papers_estudiantes (3).txt`: Normas para la redacción del paper.
- `PAPER_EXAMPLE.txt`: Ejemplo de trabajo final.
- **Presentación.pdf / Diagrama.png:** Material gráfico para explicación y defensa.

## Cómo usar este repositorio

1. **Revisar los archivos de análisis previo** para entender la estructura y variables del modelo.
2. **Consultar las FDPS** para ver cómo se modelan los tiempos y distancias reales.
3. **Utilizar la presentación y el diagrama** para entender el flujo de la simulación.
4. **Usar el formato y ejemplo de paper** para redactar el documento académico final.

## Autoría

Trabajo realizado por:  
- Thiago Martín Gonzalez  
- María Emilia Andersen  
- Agustín Podhainy Vignola  

Materia: **Simulación - K4573**  
Universidad Tecnológica Nacional, Facultad Regional Buenos Aires

---

> Para consultas sobre el modelo o el paper, revisar el archivo de análisis previo y la estructura del formato de presentación.

Autoría
Trabajo realizado por:

Thiago Martín Gonzalez
María Emilia Andersen
Agustín Podhainy Vignola
Materia: Simulación - K4573
Universidad Tecnológica Nacional, Facultad Regional Buenos Aires
