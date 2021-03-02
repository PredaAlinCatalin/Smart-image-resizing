import sys
import numpy as np
import pdb

from parameters import *
def select_random_path(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    line = 0
    col = np.random.randint(low=0, high=E.shape[1], size=1)[0]
    path = [(line, col)]
    for i in range(E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if path[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif path[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        col = path[-1][1] + opt
        path.append((line, col))

    return path


def select_greedy_path(E):
    line = 0
    col = np.argmin(E, axis=1)[0]
    path = [(line, col)]

    for i in range(1, E.shape[0]):
        line = i
        if path[-1][1] == 0:
            arr_posibilities = [E[i][path[-1][1]], E[i][path[-1][1] + 1]]
            opt = np.argmin(arr_posibilities)

        elif path[-1][1] == E.shape[1] - 1:
            arr_posibilities = [E[i][path[-1][1] - 1], E[i][path[-1][1]]]
            opt = np.argmin(arr_posibilities) - 1

        else:
            arr_posibilities = [E[i][path[-1][1] - 1], E[i][path[-1][1]], E[i][path[-1][1] + 1]]
            opt = np.argmin(arr_posibilities) - 1

        col = path[-1][1] + opt
        path.append((line, col))

    return path


def select_dynamic_programming_path(E):
    M = np.zeros(E.shape)
    M[0, :] = E[0, :]
    for i in range(1, M.shape[0]):
        for j in range(0, M.shape[1]):
            if j == 0:
                M[i, j] = E[i, j] + min(M[i - 1][j], M[i - 1][j + 1])
            elif j == M.shape[1] - 1:
                M[i, j] = E[i, j] + min(M[i - 1][j], M[i - 1][j - 1])
            else:
                M[i, j] = E[i, j] + min(M[i - 1][j - 1], min(M[i - 1][j], M[i - 1][j + 1]))
    pos = np.argmin(M, axis=1)[-1]
    path = [(M.shape[0] - 1, pos)]

    for i in range(M.shape[0] - 2, -1, -1):
        if M[i][path[-1][1]] == M[i + 1][path[-1][1]] - E[i + 1][path[-1][1]]:
            path.append((i, path[-1][1]))
        elif M[i][path[-1][1] - 1] == M[i + 1][path[-1][1]] - E[i + 1][path[-1][1]]:
            path.append((i, path[-1][1] - 1))
        else:
            path.append((i, path[-1][1] + 1))
    path.reverse()
    return path


def select_path(E, method):
    if method == 'aleator':
        return select_random_path(E)
    elif method == 'greedy':
        return select_greedy_path(E)
    elif method == 'programareDinamica':
        return select_dynamic_programming_path(E)
    else:
        print('The selected method %s is invalid.' % method)
        sys.exit(-1)