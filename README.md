# GA for Itinerary Planning — port a Python

Port a Python (NumPy / SciPy / Matplotlib) del proyecto de la PC3 de Computación Evolutiva
(CC521, UNI): un algoritmo genético que arma itinerarios turísticos optimizando distancia,
tiempo y costo bajo un presupuesto, usando los datasets **Burma** (TSPLIB, 14 lugares) e
**Istanbul** (museos de la ciudad).

Código original en MATLAB: [MuhammedSehab/GA-for-Itinerary-Planning](https://github.com/MuhammedSehab/GA-for-Itinerary-Planning) (MIT, © 2024 MuhammedSehab).

Paper de referencia: Şehab, M. & Turan, M. (2024). *An enhanced genetic algorithm solution for
itinerary recommendation considering various constraints*. PeerJ Computer Science 10:e2340.
DOI [10.7717/peerj-cs.2340](https://doi.org/10.7717/peerj-cs.2340)

## Estructura

```
.
├── Turism_Burma/                    dataset TSPLIB (14 lugares)
│   ├── Main_prog.py                 punto de entrada: parámetros + ejecución
│   ├── GA.py                        ciclo evolutivo (selección por torneo, elitismo)
│   ├── Fitness.py                   fitness = 1 / distancia total
│   ├── Distance.py                  distancia total de una ruta
│   ├── COX.py                       Copy Order Crossover
│   ├── CX.py                        Cycle Crossover
│   ├── Mutation.py                  swap mutation
│   ├── SortPop.py                   ordena población por fitness
│   ├── Norm.py                      normalización min-max
│   ├── Burma_initial_pop.py         genera población inicial aleatoria
│   ├── City.mat, distance_matrix.mat, burma_ind.mat
│   └── Burma figures/               figuras de referencia del repo original (.fig)
└── Turism_Istanbul/                 dataset propio (museos de Estambul)
    ├── Main_prog.py                 pide presupuesto por teclado (2000 en el paper)
    ├── GA.py, Fitness.py, COX.py, CX.py, Mutation.py, SortPop.py, Norm.py
    ├── TravelCost.py, Travel_Time.py
    ├── initial_pop.py
    ├── Places.mat, Travel_Dis.mat, Travel_Times.mat, Travel_Costs.mat, ind.mat
    └── Istanbul Figs/               figuras de referencia del repo original (.fig)
```

## Requisitos

```
numpy
scipy
matplotlib
```

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Cada dataset es autocontenido: hay que entrar a su carpeta porque los módulos se importan
por nombre plano (`from GA import GA`).

```bash
cd Turism_Burma
python Main_prog.py
```

Bajo WSL o servidor sin pantalla usar backend sin ventana:

```bash
MPLBACKEND=Agg python Main_prog.py
```

Estambul pide el presupuesto por consola, así que en modo no interactivo:

```bash
cd Turism_Istanbul
echo 2000 | MPLBACKEND=Agg python Main_prog.py
```

Parámetros en `Main_prog.py`: 100 generaciones, población 100, `pMut = 0.1`.

## Salida

Corrida de verificación (Python 3.12, NumPy/SciPy actuales):

| Dataset  | Presupuesto | Distancia total | Ruta óptima encontrada | Tiempo |
|----------|-------------|-----------------|------------------------|--------|
| Burma    | –           | 27.2032         | 1 11 9 10 2 8 13 7 6 12 14 3 4 5 | 4.5 s |
| Istanbul | 2000        | 85 (costo 837, tiempo 147) | 6 12 4 11 7 9 10 8 5 1 2 3 | 3.1 s |

## Notas de la traducción

- Los planes guardan IDs de lugar **1-based**, igual que en MATLAB, para no tocar la
  aritmética de índices de `COX`, `CX`, `Mutation` y las matrices `.mat`.
- `Mutation.py` reproduce fielmente el original: construye una matriz `n×n` de Bernoulli y
  solo intercambia si la fila entera es 1, o sea probabilidad efectiva `pMut**n`. Es un
  comportamiento del código original, no un bug de la traducción.
- Las matrices `.mat` se cargan una sola vez con `lru_cache` en lugar de en cada evaluación
  de fitness (única desviación de rendimiento; no altera el resultado).
- `num2str` imita el formato de MATLAB para la salida por consola.
- Las figuras `.fig` de cada carpeta son del repo original en MATLAB y se conservan solo
  como referencia de los resultados esperados.

## Licencia

MIT — ver [LICENSE](LICENSE). Obra derivada del repositorio original de MuhammedSehab
(© 2024), que se distribuye bajo la misma licencia.
