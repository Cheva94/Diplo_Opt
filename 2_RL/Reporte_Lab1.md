# Diplomatura en ciencia de datos, aprendizaje automático y sus aplicaciones - Edición 2023 - FAMAF (UNC)

## Aprendizaje por refuerzos

### Trabajo práctico entregable 1/2 (materia completa)

**Estudiante:**
- [Chevallier-Boutell, Ignacio José.](https://www.linkedin.com/in/nachocheva/)

**Docentes:**
- Palombarini, Jorge (Mercado Libre).
- Barsce, Juan Cruz (Mercado Libre).

---
# Ejercicio: SARSA + $\epsilon$-greedy

> Cantidad de episodios y semilla aleatoria (default)

En la siguiente figura se ve la variación del retorno y la cantidad de pasos temporales en función de la cantidad de episodios (entre 500 y 20000), dejando que la semilla sea aleatoria (izquierda) o fijándola (derecha). Se utilizaron los hiperparámetros *por defecto* (los que están en las consignas): $\alpha=0.5$, $\gamma=1$ y $\epsilon=0.1$.

Se observa que:
* El algoritmo utilizado es determinista.
* Ambos casos alcanzan un *plateau*, a unos 10 puntos de distancia respecto al valor de referencia Camino Seguro.
* No hay ningún early stopping, llegando en todos los casos al objetivo.
* Todas las corridas son sumamente rápidas (1 a 40 s).

Se decide:
* Fijar la semilla del generador de números aleatorios.
* Fijar la cantidad de episodios en 10000.

![](Outputs/Lab1/Determinista/SARSA-epGreedy_its-2000_a-0.5_g-1_e-0.1.png)

***Observación:*** a los fines de que sea reproducible, para el caso aleatorio se usó en realidad el número de episodios correspondiente como semilla del generador de números aleatorios.

> Barrido de $\alpha$

En la siguiente figura se ve la variación del retorno y la cantidad de pasos temporales en función de la tasa de aprendizaje (entre 0.005 y 1), para 10000 episodios y con una semilla fija, teniendo $\gamma=1$ y $\epsilon=0.1$. No se utiliza $\alpha=0$ porque esto sería equivalente a no aprender, ya que en la función de actualización lo único que se haría es sumar 0 al valor de Q.

Se observa que:
* A menor $\alpha$, el aprendizjae es más lento, pero más seguro.
* Desde 0.75 en adelante se introduce una gran cantidad de ruido: el agente comienza aprendiendo, preo a los pocos episodios *comienza a desaprender* (la curva de aprendizaje cae).
* Las curvas son prácticamente suaves para valores iguales o menores a 0.25.
* Salvo $\alpha=0.9$ y $\alpha=1$ que presentan 0.01% y 1.45% de early stopping, los demás llegan siempre al objetivo.
* Las corridas son muy rápidas (15 s a 3 min s).

Entre $\alpha$ igual a 0.1 y 0.05 no hay tanta diferencia de velocidad y el gap a los 10000 episodios es pequeño. Se decide fijar $\alpha=0.05$.

![](Outputs/Lab1/Alpha/SARSA-epGreedy_its-2000_eps-10000_g-1_e-0.1.png)

> Barrido de $\gamma$

En la siguiente figura se ve la variación del retorno y la cantidad de pasos temporales en función del descuento (entre 0.1 y 1), para 10000 episodios y con una semilla fija, teniendo $\alpha=0.05$ y $\epsilon=0.1$. No se utiliza $\gamma=0$ porque esto sería equivalente a no poder ver más allá del retorno inmediato, perdiendo predecibilidad en el horizonte.

Se observa que:
* A menor $\gamma$, necesita más iteraciones para alcanzar el Goal (necesitaría un mayor max_iter). 
* Desde 0.5 para abajo el agente comienza aprendiendo, preo luego la curva de aprendizaje cae. Algo similar se observa para $\gamma=0.6$ alrededor de los 8000 episodios.
* Las curvas son suaves para valores iguales o mayores a 0.65.
* Para $\gamma=0.6$ hay un 0.2% de early stopping, mientras que para $\gamma$ igual a 0.5, 0.25 y 0.1 el early stopping es de 4.4%, 54.22% y 79.43%, respectivamnete. Todos los demás llegan siempre al objetivo.
* Desde $\gamma=1$ hasta $\gamma=0.5$ las corridas son muy rápidas (17 s a 2 min). En cambio, para los peores 2 casos las corridas demoran entre 14 y 19 minutos. 

Se decide fijar $\gamma=0.65$.

![](Outputs/Lab1/Gamma/SARSA-epGreedy_its-2000_eps-10000_a-0.05_e-0.1.png)

> Barrido de $\epsilon$

En la siguiente figura se ve la variación del retorno y la cantidad de pasos temporales en función de la frecuencia de exploración (entre 0 y 1), para 10000 episodios y con una semilla fija, teniendo $\alpha=0.05$ y $\gamma=0.65$. 

Se observa que:
* Para valores mayores o iguales a $\epsilon=0.25$ presenta picos en al curva de aprendizaje que después caen. A mayor $\epsilon$ estos picos tienen retornos promedios cada vez peores. Además necesitan muchos más pasos temporales.
* Como era de esperarse, el caso extremo en el que sólo nos dedicamos a tirar la moneda constantemente ($\epsilon=1$, pura exploración) es el peor de todos, ya que nunca aprovechamos lo que ya sabemos.
* El otro extremo donde sólo aprovechamos lo que sabemos ($\epsilon=0$, pura explotación) es el más rápido de todos, superando la barrera del camino seguro y tendiendo al óptimo. Sin embargo, estamos muy sesgados y nunca damos lugar a aprender algo diferente.
* Las curvas son suaves para valores iguales o menores a 0.1, salvo para $\epsilon=0.001$ que tiene un salto alrededor de 4000 episodios.
* Para $epsilon\in[0.25, 1]$ hay casos de early stopping (entre 7% y el 74%). Los demás siempre llegan al objetivo.
* Para $epsilon\in[0, 0.1]$ la corrida tarda entre 14 y 16 segundos, mientras que en los demás casos tarda entre 4 min y 37 min.

Se decide fijar $\epsilon=0.005$.

![](Outputs/Lab1/Epsilon/SARSA-epGreedy_its-2000_eps-10000_a-0.05_g-0.65.png)

> Cantidad de episodios y semilla aleatoria (óptimos)

Se decide:
* Fijar la semilla del generador de números aleatorios.
* Fijar la cantidad de episodios en 10000.



***Observación:*** a los fines de que sea reproducible, se hizo lo mismo que antes y para el caso aleatorio se usó en realidad el número de episodios correspondiente como semilla del generador de números aleatorios.

> Consluiones generales de SARSA + $\epsilon$-greedy

En la siguiente figura se ve la variación del retorno y la cantidad de pasos temporales en función de la cantidad de episodios (entre 10000 y 200000), dejando que la semilla sea aleatoria (izquierda) o fijándola (derecha). Se utilizaron los hiperparámetros óptimos que se fueron encontrando: $\alpha=0.05$, $\gamma=0.65$ y $\epsilon=0.005$.

Se observa que:
* Hasta ahora casi ningún caso había alcanzado llegar a la barrera del Camino Seguro, ya que se alcanzaba un *plateau* antes. Sin embargo, utilizando los valores óptimos vemos que con unos 20000 episodios nos aseguramos de cruzar este límite, tendiendo a una asíntota horizontal alrededor de $\mp15$ según sea el retorno o la cantidad de pasos.
* Con 20000 episodios aún estamos en el codo de la curva, asentándose más alrededor de los 100000. Entre 20000 y 100000 hay un punto de diferencia, mientras que entre 100000 y 200000 hay 0.25 puntos.
* No hay ningún early stopping, llegando en todos los casos al objetivo.
* A mayor cantidad de episodios, más demora el cálculo. Sin embargo, sigue siendo muy rápido: en menos de 6 minutos corren los 200000 episodios.
* A pesar de la aleatoriedad en las condiciones iniciales, el comportamiento es menos dispar que al comienzo, convergiendo la mayoría de las curvas a la misma situación. Esto puede deberse a que se están utilizando los hiperparámetros ya finetuneados.

![](Outputs/Lab1/Optimos/SARSA-epGreedy_its-2000_a-0.05_g-0.65_e-0.005.png)

Esta ruta intermedia a la que se llega entre el camino óptimo y el seguro queda reflejada en la siguiente figura para el caso de semilla fija y 100000 episodios.

![](Outputs/Lab1/Optimos/SARSA-epGreedy_its-2000_eps-100000_a-0.05_g-0.65_e-0.005_fixedSeed.png)

Se concluye entonces que:
* El algoritmo SARSA con una política $\epsilon$-greedy es determinista.
* Cuanto más lento el aprendizaje, más seguro el avance. Para que no sea demasiado lento, tomar $\alpha\in[0.05, 0.25]$.
* Si queremos sesgar el horizonte, tomar $\gamma\in[0.65, 1]$.
* Al dejar fija la frecuencia de exploración, conviene tomar $\gamma\in[0.001, 0.05]$.

---
# Ejercicio: Q-learning + $\epsilon$-greedy


---
# Acá hay notas

Dado que el descuento $\gamma$ es iguala 1, en teoría deberíamos eventualmente alcanzar el retorno óptimo al aumentar la cantidad de episodios, siempre y cuando la tasa de aprendizaje $\alpha$ sea lo suficientemente pequeña.

El hiperparámetro $\alpha$ me determina la velocidad de convergencia. Cuando $\alpha=1$, la convergencia es muy brusca, pudiendo llegar a quedar oscilando. Al bajar el valor de $\alpha$, nos aseguramos de que eventualmente converja. Supongamos que el objetivo es juntar 50 puntos. Puede ocurrir que con $\alpha=1$ nos movamos muy rápido y terminemos oscilando en torno a un punto o puede que rápidamente llegemos a 50 puntos. Cuanto menor es el $\alpha$, más lenta será la evolución, pero eventualmente llegamos a 50 puntos.

Por otro lado, $\gamma$ nos limita el horizonte. Cuando  $\gamma=1$, dependemos exclusivamente del $\alpha$ para saber qué tan rápido o lento alcanzamos los 50 puntos. En cambio, si $0<\gamma<1$, no importa qué tan rápido o lento aprendamos, siempre habrá un techo para el valor al que convergemos, siendo menor a 50 puntos. Cuanto menor sea $\gamma$, más por debajo de 50 puntos nos vamos a encontrar.

# Sarsa greedy

> Mostrar la grilla q para los casos extremos: se inclina por el camino seguro más que por el óptimo. (esto lo saque antes del 1, pero aplicar en general).

# Q-learning greedy

1) Hacer lo mismo que en el de greedy. Comparar intra e inter. ¿Cómo converge con respecto a SARSA? ¿A qué se debe? Comentar.

> Hasta acá ya tendría las 3 primeras actividades hechas. Las dos que siguen son opcionales: la de SoftMax y la de Dyna-Q

Nunca hubo un drop.

