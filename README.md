# Routing & Optimization Framework

>Framework modular para el estudio, implementación y análisis de problemas de optimización combinatoria, con foco en problemas de ruteo como el Traveling Salesman Problem (TSP) y extensiones hacia VRP y variantes generales.
>
>El objetivo del proyecto es construir un entorno reproducible y extensible para comparar algoritmos exactos, heurísticos y (en el futuro) enfoques basados en aprendizaje, evaluando su rendimiento en términos de costo, tiempo de ejecución y escalabilidad.



## Tabla de contenidos
* [Objetivos](#objetivos)
* [Problemas abordados](#problemas-abordados)
* [Estructura del proyecto](#estructura-del-proyecto)
* [Pipeline del sistema](#pipeline-del-sistema)
* [Instalación](#instalación)
* [Uso](#uso)
* [Ejemplo de análisis](#ejemplo-de-análisis)
* [Extensiones futuras](#extensiones-futuras)
* [Notas técnicas](#notas-técnicas)
* [Contacto](#contacto)



## Objetivos

- Implementar y comparar algoritmos de optimización combinatoria (exactos y heurísticos)
- Analizar rendimiento en términos de:
  - tiempo de ejecución
  - consumo de memoria
  - calidad de solución (optimalidad vs aproximación)
- Construir un pipeline reproducible de experimentación
- Centralizar resultados mediante persistencia en base de datos (SQLite)
- Diseñar una arquitectura extensible hacia VRP y variantes más complejas
- Explorar integración futura con técnicas de Machine Learning para heurísticas y aproximaciones



## Problemas abordados

### Traveling Salesman Problem (TSP)
- Algoritmos exactos:
  - brute force (enumeración completa)
  - programación dinámica (Held-Karp, si aplica)
- Heurísticas constructivas:
  - nearest neighbor
- Métodos de mejora local:
  - 2-opt
  - 3-opt (en desarrollo)
- Evaluación basada en matrices de distancia y análisis comparativo

### Vehicle Routing Problem (VRP) *(en desarrollo)*
- Capacitated VRP (CVRP)
- Heurísticas constructivas base
- Refinamiento mediante búsqueda local
- Extensión natural del framework de TSP

### Generalizaciones (roadmap)
- TSP con restricciones (time windows, penalties)
- VRP con múltiples restricciones
- Problemas multi-objetivo (costo vs distancia vs balance de carga)



## Estructura del proyecto

El proyecto sigue una arquitectura modular orientada a escalabilidad y experimentación reproducible, separando claramente lógica de optimización, generación de datos, experimentación y persistencia.

```
src/
├── core/           # Componentes fundamentales (distancias, métricas, evaluación)
├── tsp/            # Implementaciones de algoritmos para TSP
├── data/           # Generación de instancias y datasets
├── experiments/    # Benchmarks, análisis y pipelines experimentales
├── db/             # Persistencia y manejo de SQLite
```

### Principios de diseño
- Separación de responsabilidades
- Extensibilidad de algoritmos y problemas
- Reproducibilidad de experimentos
- Trazabilidad de resultados mediante base de datos
- Enfoque experimental tipo benchmarking



## Pipeline del sistema

El flujo general del framework es el siguiente:

```text
[ data ]
    ↓
[ core (distance + evaluation) ]
    ↓
[ tsp (solvers) ]
    ↓
[ db (results storage) ]
    ↓
[ experiments (benchmarking + analysis) ]
```



## Instalación
``` bash
git clone <repo-url>
cd routing-optimization-framework
pip install -r requirements.txt
```



## Uso

Ejecutar benchmark principal
```bash
python src/experiments/benchmark.py
```

Benchmark de matrices de distancia
```bash
python src/experiments/distance_benchmark.py
```



## Ejemplo de análisis

El sistema permite comparar algoritmos en función de múltiples métricas:

- tiempo de ejecución
- costo de solución
- escalabilidad respecto al número de nodos

Ejemplo de consulta SQL sobre resultados:

```sql
SELECT 
    algorithm,
    AVG(runtime) AS avg_time,
    AVG(cost) AS avg_cost
FROM runs
GROUP BY algorithm;
```



## Extensiones futuras

- Metaheurísticas:
  - Simulated Annealing
  - Genetic Algorithms
  - Tabu Search
- Extensión completa a VRP (capacidades, ventanas de tiempo)
- Integración con Machine Learning:
  - aprendizaje de heurísticas
  - predicción de soluciones iniciales
  - aproximación de costos
- Optimización del pipeline de benchmarking para grandes volúmenes de experimentos



## Notas técnicas

- Los algoritmos exactos presentan complejidad factorial/exponencial, por lo que su uso se restringe a instancias pequeñas.
- El diseño prioriza claridad experimental y análisis comparativo por sobre optimización micro de implementación.
- El sistema está pensado como base extensible para investigación en optimización combinatoria.



## Contacto

**Autor:** José Sepúlveda \
**Correo:** josepulveda01@hotmail.com
