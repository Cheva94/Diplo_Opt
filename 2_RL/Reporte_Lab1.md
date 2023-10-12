Ejecutamos una corrida de SARSA con $\epsilon$-greedy, utilizando los parámetros *por defecto* (los definidos en las consignas), tanto para los hiperparámetros como para la cantidad de episodios y de iteraciones. Lo primero que notamos es que ambas curvas, sobre todo la de retorno, aún no se logran estabilizar con 500 episodios, por lo cual deberíamos aumentar esta cantidad. Además, cada episodio demora menos de 600 iteraciones, por lo que podríamos bajar el límite de 2000. Por este motivo es que no hay ningún early stopping y todos llegan a cumplir el objetivo. Dado que el descuento $\gamma$ es iguala 1, en teoría deberíamos eventualmente alcanzar el retorno óptimo al aumentar la cantidad de episodios, siempre y cuando la tasa de aprendizaje $\alpha$ sea lo suficientemente pequeña.



El hiperparámetro $\alpha$ me determina la velocidad de convergencia. Cuando $\alpha=1$, la convergencia es muy brusca, pudiendo llegar a quedar oscilando. Al bajar el valor de $\alpha$, nos aseguramos de que eventualmente converja. Supongamos que el objetivo es juntar 50 puntos. Puede ocurrir que con $\alpha=1$ nos movamos muy rápido y terminemos oscilando en torno a un punto o puede que rápidamente llegemos a 50 puntos. Cuanto menor es el $\alpha$, más lenta será la evolución, pero eventualmente llegamos a 50 puntos.

Por otro lado, $\gamma$ nos limita el horizonte. Cuando  $\gamma=1$, dependemos exclusivamente del $\alpha$ para saber qué tan rápido o lento alcanzamos los 50 puntos. En cambio, si $0<\gamma<1$, no importa qué tan rápido o lento aprendamos, siempre habrá un techo para el valor al que convergemos, siendo menor a 50 puntos. Cuanto menor sea $\gamma$, más por debajo de 50 puntos nos vamos a encontrar.

# Sarsa greedy


max_iter se puede bajar, pero quedó en 2000.

eps de base eran 500

1) Comparar aleatorio con semilla fija. Decir que es determinista. Decir cómo se acerca asintóticamente al valor deseado. Mostrar la grilla q para los casos extremos: se inclina por el camino seguro más que por el óptimo. Acá se varía solamente el número de episodios (y también max_iter pero we) y se fija o no la semilla aleatoria.

2) Barrer alfa, gamma y epsilon, fijando la semilla, el max_iter y la cantidad de episodios. 

Alfa = 0 es esquivalente a no aprender porque en la función de actualización lo único que hace es sumar 0. Barrido de alfa: cuanto más chico es, más lento, pero mas seguro (se pierde ruido). Entre 0.1 y 0.05 no hay tanta diferencia de velocidad y el gapa los 10k eps es chico. Elegir entre estos dos. Probar con 0.05 primero. Ver que en tiempo no es tan diferete. No olvidar el nuevo: 0.01.

Barrido de gamma con eps = 10k y alpha = 0.05. Ver qué implica un gamma nulo. A menor gamma, necesita más iteraciones para alcanzar el Goal (necesitaría un mayor max_iter). Por eso la proporción de Earlies aumenta. Consume mucho más tiempo y no está cumpliendo encima. Ya con 0.25 tarda unos 14 minutos. Cortar en 0.1. Me quedo con gamma=0.65.

--hasta acá hice en mi compu--
-- todo lo que sigue lo hice con la compu del lab (cuidado con la comparación de wall time) --

Epsilon sí puede valer 0 y 1 por explotar o explorar a full. Cuidado que en el sorteo de exploración se incluyen los máximos. Usar el rango que venímos viendo más estos dos extremos.

3) Con la combinación óptima, barrer episodios de nuevo?

# Q-learning greedy

1) Hacer lo mismo que en el de greedy. Comparar intra e inter. ¿Cómo converge con respecto a SARSA? ¿A qué se debe? Comentar.

> Hasta acá ya tendría las 3 primeras actividades hechas. Las dos que siguen son opcionales: la de SoftMax y la de Dyna-Q

Nunca hubo un drop.