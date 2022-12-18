import networkx as nx
import numpy as np
import random as rnd
import math
# матрица смежности
matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
      [0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
      [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      [3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def stock_source_search(matrix):
  """Функция поиска стока и истока графа по матрице смежности"""
  stock = []; source = []
  for i in range(len(matrix)):
    if sum(matrix[i])==0: 
      stock.append(i)
  for i in range(len(matrix)):
    sum_j = 0
    for j in range(len(matrix[i])):
      sum_j += matrix[j][i]
    if sum_j ==0:
      source.append(i)
  return stock, source

def GetInputNodesArray(nodes, count):
    """Вспомогательная функция для TopologicSort"""
    array = []
    for i in count: 
        step=0
        for j in count:
            if nodes[i][j]==1:step+=1
        array.insert(i,step)
    return array;

def TopologicSort(nodes_input, count):
    """Функция получения вершин графа к упорядоченном порядке"""
    nodes = []
    for i in count:
      nodes.append([])
      for j in count:
        if nodes_input[i][j] != 0: nodes[i].append(1)
        else: nodes[i].append(0)
    levels =[];
    workArray = GetInputNodesArray(nodes, count);
    completedCounter = 0;
    currentLevel = 0;
    while (completedCounter != len(nodes)):
        for i in count:
            if (workArray[i] == 0):
                ind=0
                #добавляем обработанную вершину
                levels.insert(completedCounter,i);
                for node in nodes:
                    if node[i]==1:
                        workArray[ind]-=1
                    ind+=1
    
                workArray[i] = -1; # Помечаем вершину как обработанную
                completedCounter+=1;
        currentLevel+=1;
    levels.reverse()
    return levels#осталось выбрать в обратном порядке

def ordered_graph(matrix):
    """Формирование упорядоченного графа по входной матрице смежности
    Возвращает ord_matrix - упорядоченную матрицу и ord_index - словарь {старый индекс: значение - новый индекс}
    adjacency_set - словарь: ключ - начальный индекс, значение - список начальных индексов смежности"""
    # проверка того, что граф можно упорядочить. т.е. проверка отсутствия цикла
    G = nx.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph)
    try:
        cycle = nx.find_cycle(G)
        if len(cycle) != 0:
          cycle_i_1 = []
          for tup in cycle:
            cycle_i_1 += [(tup[0]+1, tup[1]+1)]

          return -1, -1, -1, cycle_i_1
    except:
        pass
    stock, source = stock_source_search(matrix)
    ord_matrix = []   # Упорядоченная матрица смежности
    adjacency_set = {}  # словарь: ключ - начальный индекс, значение - список начальных индексов смежности
    for i in range(len(matrix)):
        ord_matrix.append([0]*len(matrix))
        visitors = []   # список смежностей с элементом
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                visitors.append(j)
        adjacency_set.update({i: visitors})
    # формирование упорядоченного графа
    j = 0
    ord_index = {} # словарь ключ - старый индекс, значение - новый индекс
    temp_ord_index = TopologicSort(matrix, range(len(matrix)))
    for i in range(len(temp_ord_index)):
      ord_index.update({temp_ord_index[i]: i})
    
    for i in ord_index.keys():
      for j in range(len(adjacency_set[i])):
        ord_matrix[ord_index[i]][ord_index[adjacency_set[i][j]]] = matrix[i][adjacency_set[i][j]]

    return ord_matrix, ord_index, adjacency_set


def levels(ord_matrix, ord_index):
    """Уровни графа по матрице упорядоченной матрице смежности"""
    for i in range(len(ord_matrix)):
        for j in range(len(ord_matrix)):
            if ord_matrix[i][j] == 0:
                ord_matrix[i][j] = math.inf

    digs = []
    temp = []
    for i in range(len(ord_matrix)):
        for j in range(len(ord_matrix)):
            if ord_matrix[j][i] != math.inf:
                temp.append(j + 1)

        digs.append(temp)
        temp = []

    lvl = []
    for i in range(len(digs)):
        for j in range(len(digs)):
            if len(digs[i]) == j:
                lvl.append(digs)
    del lvl[1:]
    lvl = lvl[0]
    ind = []
    temp_ind = []
    lvl_check = lvl.copy()
    min_len = min(lvl_check, key=len)
    for i in range(len(lvl_check)):
        if lvl_check[i] == min_len:
            ind.append(i + 1)

    temp_ind.append(ind)
    for j in range(1, len(lvl)):
        flat_list = [item for sublist in temp_ind for item in sublist]
        ind = [i + 1 for i, q in enumerate(lvl) if q and not set(q) - set(flat_list)]
        for k in range(len(ind)):
            if ind[k] in flat_list:
                ind[k] -= 999
        temp_ind.append(ind)
    final_ind = [[] * i for i in range(len(temp_ind))]
    for i in range(len(temp_ind)):
        for j in range(len(temp_ind[i])):
            if temp_ind[i][j] > 0:
                final_ind[i].append(temp_ind[i][j])
    result = []
    for i in final_ind:
        if i:
            result.append(i)
    
    ord_index_revers = dict(zip(ord_index.values(), ord_index.keys()))
    for i in range(len(result)):
      for j in range(len(result[i])):
        result[i][j] = ord_index_revers[result[i][j]-1] + 1

    return result


def min_path(matrix, inital_inx, final_inx):
    """Поиск минимального расстояния
    return optimal_way - список индексов представляющих собой оптимальный путь, min_dist - расстояние пройденное по оптимальному пути"""
    ord_A = ordered_graph(matrix)[0]
    G = nx.from_numpy_matrix(np.matrix(ord_A), create_using=nx.DiGraph)
    summa = 0
    try:
        path = nx.dijkstra_path(G, int(inital_inx) - 1, int(final_inx) - 1)
        if path != None:
            for i in range(len(path) - 1):
                summa += G[path[i]][path[i + 1]]['weight']

        path = [i + 1 for i in path]
        return path, summa

    except:
        # нет пути
        return -1, -1


def graph_generation_without_loop(matrix_size):
    """Генерация графа без цикла"""
    matrix = []
    source, stock = rnd.randint(0, matrix_size-1), rnd.randint(0, matrix_size-1)
    for i in range(matrix_size):
      matrix.append([])
      for j in range(matrix_size):
        var = int()
        if i == stock or j == source or i == j:
            var = 0
        else:
            for v in range(15):
                var = rnd.randint(0, 10)
                if var == 0: break
        matrix[i].append(var)
    # проверка того, что граф можно упорядочить. т.е. проверка отсутствия цикла
    while True:
      G = nx.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph)
      try:
          cycle = nx.find_cycle(G)
          # if len(cycle) == 0: break
          matrix[cycle[0][0]][cycle[0][1]] = 0
      except:
          break

    return matrix
