#!/usr/bin/python3.10

from typing import Callable, Tuple

import numpy as np
import pandas as pd

import gymnasium as gym

import time

################################################################################
#                       Heurísticas
################################################################################

def epGreedy(
    state: int,
    actions: range,
    q: dict,
    hyperparameters: dict,
    random_state: np.random.RandomState
) -> int:

    """
    Elije una acción de acuerdo a una política de exploración-explotación 
    épsilon-greedy.
    Args:
        state: estado actual del agente
        actions: lista de acciones posibles
        q: diccionario de valores de estado-acción
        hyperparameters: hiperparámetros del algoritmo de aprendizaje
        random_state: generador de números aleatorios
    """

    # Lista de valores q asociados a un estado-acción
    q_values = [q.get((state, a)) for a in actions]

    # Toma el valor máximo
    max_q = max(q_values)

    # Puede haber más de un valor máximo
    count = q_values.count(max_q)

    # Sortemaos un número aleatorio y comparamos con épsilon
    if random_state.uniform() < hyperparameters['epsilon']:
        # Exploramos, seleccionando una acción aleatoriamente
        return random_state.choice(actions)

    # Al no cumplirse la condición, explotamos
    elif count > 1:
        # Hay más de un valor máximo. Sorteamos alguno de ellos
        best = [i for i in range(len(actions)) if q_values[i] == max_q]
        i = random_state.choice(best)
    
    else:
        # Hay un único valor máximo, eligiendo el correspondiente estado-acción
        i = q_values.index(max_q)

    return actions[i]


def SoftMax(
    state: int,
    actions: range,
    q: dict,
    hyperparameters: dict,
    random_state: np.random.RandomState
) -> int:

    """
    Elije una acción de acuerdo a una política de exploración-explotación SoftMax.
    Args:
        state: estado actual del agente
        actions: lista de acciones posibles
        q: diccionario de valores de estado-acción
        hyperparameters: hiperparámetros del algoritmo de aprendizaje
        random_state: generador de números aleatorios
    Nota:
        Para facilitar la reutilización de código, se toma a epsilon como tau.
    """

    # Lista de valores q asociados a un estado-acción
    q_values = np.array([q.get((state, a)) for a in actions])

    # Aplico las exponenciales
    exp_qt = np.exp(q_values / hyperparameters['tau'])

    # Constante de normalización
    norm = np.sum(exp_qt)

    # Distribución de probabilidad
    distrib = exp_qt / norm

    # Muestreamos la distribución, obteniendo la acción
    action = random_state.choice(actions, p=distrib)

    return action

################################################################################
################################################################################
################################################################################

################################################################################
#                       Aprendizaje
################################################################################

def SARSA_learning(
    state: int,
    action: int,
    reward: int,
    next_state: int,
    next_action: int,
    hyperparameters: dict,
    q: dict
) -> Tuple[int, int]:

    """
    Realiza una actualización según el algoritmo SARSA, para una transición de 
    estado dada.
    Args:
        state: estado actual del agente
        action: acción actual ejecutada por el agente
        reward: recompensa recibida al ejecutar la acción
        next_state: próximo estado del agente
        next_action: próxima acción del agente
        hyperparameters: hiperparámetros del algoritmo de aprendizaje
        q: diccionario de valores de estado-acción
    """

    # Actualizo el valor del estado-acción
    Target = reward + hyperparameters['gamma'] * q[(next_state, next_action)]
    TD_error = Target - q[(state, action)]
    q[(state, action)] += hyperparameters['alpha'] * TD_error

    # Actualizo el estado
    state = next_state

    # Actualizo la acción
    action = next_action

    return state, action


def Q_learning(
    state: int,
    action: int,
    reward: int,
    next_state: int,
    actions: range,
    hyperparameters: dict,
    q: dict,
    random_state: np.random.RandomState
) -> Tuple[int, int]:

    """
    Realiza una actualización según el algoritmo Q-learning, para una 
    transición de estado dada.
    Args:
        state: estado actual del agente
        action: acción actual ejecutada por el agente
        reward: recompensa recibida al ejecutar la acción
        next_state: próximo estado del agente
        actions: lista de acciones posibles
        hyperparameters: hiperparámetros del algoritmo de aprendizaje
        q: diccionario de valores de estado-acción
        random_state: generador de números aleatorios
    """

    # Lista de valores q asociados a un estado-acción
    q_values = [q.get((state, a)) for a in actions]

    # Toma el valor máximo
    max_q = max(q_values)

    # Puede haber más de un valor máximo
    count = q_values.count(max_q)

    if count > 1:
        # Hay más de un valor máximo. Sorteamos alguno de ellos
        best = [i for i in range(len(actions)) if q_values[i] == max_q]
        i = random_state.choice(best)
    
    else:
        # Hay un único valor máximo, eligiendo el correspondiente estado-acción
        i = q_values.index(max_q)

    # Actualizo el valor del estado-acción
    Target = reward + hyperparameters['gamma']  * q[(next_state, actions[i])]
    TD_error = Target - q[(state, action)]
    q[(state, action)] += hyperparameters['alpha'] * TD_error

    # Actualizo el estado
    state = next_state

    return state

################################################################################
################################################################################
################################################################################

################################################################################
#                       Iteraciones
################################################################################

def run_SARSA(
    policy: Callable,
    hyperparameters: dict,
    episodes_to_run: int,
    env: gym.Env,
    actions: range,
    random_state: np.random.RandomState,
    max_iter: int
) -> Tuple[np.ndarray, np.ndarray, int, int, int, dict]:

    """
    Corre el algoritmo de RL, basado en SARSA.
    Args:
        policy: huerística de selección de acciones
        hyperparameters: hiperparámetros del algoritmo de aprendizaje
        episodes_to_run: cantidad de episodios a ejecutar
        env: entorno de Gymnasium
        actions: lista de acciones posibles
        random_state: generador de números aleatorios
        max_iter: cantidad máxima de pasos temporales
    """

    # Inicialización del diccionario de valores de estado-acción
    q = {}
    for s in range(37):
        for a in range(4):
            q[(s, a)] = 0.0

    # Registra la cantidad de pasos de cada episodio
    timesteps_of_episode = []

    # Registra el retorno de cada episodio
    return_of_episode = []

    # Casuísticas de finalización
    goal, drop, early = 0, 0, 0

    # Loop sobre los episodios
    for _ in range(episodes_to_run):
        # Instancea un nuevo agente en cada episodio
        # Fin del episodio: llegar a la salida o superar max_iter

        # Reinicia el entorno, obteniendo el estado inicial del mismo
        state, _ = env.reset()

        # Retorno del episodio
        episode_return = 0

        # Contador de pasos temporales
        t = 0

        # Flag de finalización de iteración actual
        done = False

        # Elige la primera acción a ejecutar
        action = policy(
            state, actions, q, hyperparameters, random_state)

        while not done:
            # El agente ejecuta la acción elegida y obtiene los resultados
            next_state, reward, terminated, truncated, _ = env.step(action)

            # Acumulamos recompensa
            episode_return += reward

            # Elige la nueva acción a ejecutar partiendo desde el nuevo estado
            next_action = policy(
                next_state, actions, q, hyperparameters, random_state)

            # Mecanismo de aprendizaje por TD con SARSA
            state, action = SARSA_learning(
                state, action, reward, next_state, next_action, hyperparameters, q)

            # Análisis de convergencia
            if terminated:
                # El agente alcanzó el objetivo
                goal += 1
                timesteps_of_episode = np.append(
                    timesteps_of_episode, [int(t + 1)])
                return_of_episode = np.append(return_of_episode, episode_return)
                done = True

            elif truncated:
                # El agente ejecutó una acción inválida
                drop += 1
                timesteps_of_episode = np.append(
                    timesteps_of_episode, [int(t + 1)])
                return_of_episode = np.append(return_of_episode, episode_return)
                done = True

            elif t >= max_iter:
                # Early stopping
                early += 1
                timesteps_of_episode = np.append(
                    timesteps_of_episode, [int(t + 1)])
                return_of_episode = np.append(return_of_episode, episode_return)
                done = True

            t += 1

    return timesteps_of_episode, return_of_episode, goal, drop, early, q


def run_DynaQ(
    policy: Callable,
    hyperparameters: dict,
    episodes_to_run: int,
    env: gym.Env,
    actions: range,
    random_state: np.random.RandomState,
    max_iter: int
) -> Tuple[np.ndarray, np.ndarray, int, int, int, dict]:

    """
    Corre el algoritmo de RL, basado en Dyna-Q.
    Args:
        policy: huerística de selección de acciones
        hyperparameters: hiperparámetros del algoritmo de aprendizaje
        episodes_to_run: cantidad de episodios a ejecutar
        env: entorno de Gymnasium
        actions: lista de acciones posibles
        random_state: generador de números aleatorios
        max_iter: cantidad máxima de pasos temporales
    """

    # Pasos de planificación
    plan = hyperparameters['steps']

    # Inicialización del diccionario de valores de estado-acción
    q = {}
    for s in range(37):
        for a in range(4):
            q[(s, a)] = 0.0

    # Inicialización del diccionario del modelo
    Mod = {}

    # Registra la cantidad de pasos de cada episodio
    timesteps_of_episode = []

    # Registra el retorno de cada episodio
    return_of_episode = []

    # Casuísticas de finalización
    goal, drop, early = 0, 0, 0

    start = time.time()
    # Loop sobre los episodios
    for eps in range(episodes_to_run):
        # Instancea un nuevo agente en cada episodio
        # Fin del episodio: llegar a la salida o superar max_iter

        # Reinicia el entorno, obteniendo el estado inicial del mismo
        state, _ = env.reset()

        # Retorno del episodio
        episode_return = 0

        # Contador de pasos temporales
        t = 0

        # Flag de finalización de iteración actual
        done = False

        while not done:
            # Elige la acción a ejecutar
            action = policy(
                state, actions, q, hyperparameters, random_state)
        
            # El agente ejecuta la acción elegida y obtiene los resultados
            next_state, reward, terminated, truncated, _ = env.step(action)

            # Acumulamos recompensa
            episode_return += reward

            # Actualizamos el modelo
            if state not in Mod.keys():
                Mod[state] = {}
            Mod[state][action] = (reward, next_state)

            # Mecanismo de aprendizaje con Q-learning
            state = Q_learning(
                state, action, reward, next_state, actions, hyperparameters, q, random_state)

            # Planificación
            for _plan in range(plan):
                # Muestreamos un estado-acción ya conocido por el modelo
                plan_S = random_state.choice(list(Mod.keys()))
                plan_A = random_state.choice(list(Mod[plan_S].keys()))

                # Obtenemos recompensa y próximo estado asociados
                plan_R, plan_nextS = Mod[plan_S][plan_A]

                # Actualizamos Q
                _qs = Q_learning(
                    plan_S, plan_A, plan_R, plan_nextS, actions, hyperparameters, q, random_state)

            # Análisis de convergencia
            if terminated:
                # El agente alcanzó el objetivo
                goal += 1
                timesteps_of_episode = np.append(
                    timesteps_of_episode, [int(t + 1)])
                return_of_episode = np.append(return_of_episode, episode_return)
                done = True

            elif truncated:
                # El agente ejecutó una acción inválida
                drop += 1
                timesteps_of_episode = np.append(
                    timesteps_of_episode, [int(t + 1)])
                return_of_episode = np.append(return_of_episode, episode_return)
                done = True

            elif t >= max_iter:
                # Early stopping
                early += 1
                timesteps_of_episode = np.append(
                    timesteps_of_episode, [int(t + 1)])
                return_of_episode = np.append(return_of_episode, episode_return)
                done = True

            t += 1

        # Chequeo el progreso
        if (eps+1) % 1000 == 0:
            WallTime = time.time() - start
            print(f'\t# Episodios = {eps} >>> Retorno = {episode_return} | Tiempo = {WallTime/60:.2f} min')

            with open(f'Outputs/Lab2/tmp_s-{plan}.csv', 'w') as f:
                f.write('Goal\tDrop\tEarly\tCorridos\n')
                f.write(f'{goal}\t{drop}\t{early}\t{eps}\n')

                f.write(f'Wall Time[s]\t{WallTime}\n')
                
                f.write('State\tAction\tQ-value\n')
                for s in range(37):
                    for a in range(4):
                        f.write(f'{s}\t{a}\t{q[(s,a)]:.6f}\n')

                f.write('Return\tTimeSteps\n')
                for i in range(eps):
                    f.write(f'{return_of_episode[i]:.0f}\t{timesteps_of_episode[i]:.0f}\n')

    return timesteps_of_episode, return_of_episode, goal, drop, early, q

################################################################################
################################################################################
################################################################################

################################################################################
#                       Plots
################################################################################

def mean_evol(Arr: np.ndarray) -> np.ndarray:
    """
    Suaviza la curva de aprendizaje o de recompensa.
    Args:
        Arr: array a suavizar
    """

    eps_val = np.linspace(1, len(Arr) + 1, len(Arr) + 1)
    cum_vals = np.cumsum(Arr)

    val_per_eps = [cum_vals[i] / eps_val[i] for i in range(len(cum_vals))]

    return np.array(val_per_eps)


def draw_map(File: str):
    '''
    Grafica el mapa con el mejor camino encontrado por el agente.
    Args:
        q: diccionario de valores de estado-acción
    '''

    data = pd.read_csv(File, header=None, sep='\t').iloc[4:152, 2].to_numpy().astype(float)
    walk = []

    for s in range(37):
        # Lista de valores q asociados a un estado-acción
        s_data = data[4*s:4*(1+s)]
        
        # Toma el valor máximo
        max_q = np.max(s_data)

        # Puede haber más de un valor máximo
        count = np.count_nonzero(s_data == max_q)

        if count > 1:
            # Hay más de un valor máximo
            walk.append(str(count))

        else:
            # Hay un único valor máximo
            arg = np.argwhere(s_data == max_q)[0][0]
            if arg == 0:
                walk.append('U')
            elif arg == 1:
                walk.append('R')
            elif arg == 2:
                walk.append('D')
            else:
                walk.append('L')

    walk = np.array(walk)
    walk[2] = '~'
    for k in range(6):
        print(walk[6*k:6*(1+k)])

################################################################################
################################################################################
################################################################################