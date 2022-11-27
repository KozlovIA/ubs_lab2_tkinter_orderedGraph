
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



def ordered_graph(matrix):
    """Формирование упорядоченного графа по входной матрице смежности
    Возвращает ord_matrix - упорядоченную матрицу и ord_index - словарь {старый индекс: значение - новый индекс}
    adjacency_set - словарь: ключ - начальный индекс, значение - список начальных индексов смежности"""
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
    current_V_list = source
    for i in range(len(matrix)):
      next_inx = []
      for V in current_V_list:
        for val in adjacency_set[V]:
          next_inx.append(val)
        if not (V in ord_index):
          ord_index.update({V: j})
          j+=1
      current_V_list = next_inx
    
    for i in ord_index.keys():
      for j in range(len(adjacency_set[i])):
        ord_matrix[ord_index[i]][ord_index[adjacency_set[i][j]]] = matrix[i][adjacency_set[i][j]]
    
    return ord_matrix, ord_index, adjacency_set


def road_search(matrix, inital_inx, final_inx):
    """Поиск минимального расстояния
    return optimal_way - список индексов представляющих собой оптимальный путь, min_dist - расстояние пройденное по оптимальному пути"""
    # поиск индексов смежности
    adjacency_set = {}  # словарь: ключ - начальный индекс, значение - список индексов смежности
    for i in range(len(matrix)):
        visitors = []   # список смежностей с элементом
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                visitors.append(j)
        adjacency_set.update({i: visitors})
    
    print(adjacency_set)


    ways = []
    visitors = adjacency_set[inital_inx]
    for v in visitors:
      ways.append([inital_inx, v]) # сформировали пути [i -> v]
    
    previous_visitors = visitors
    next_vis = []
    for way in ways:
      next_vis = adjacency_set[way[-1]]
      for next in next_vis:
        visitors.append(next)

    flag = 0
    while True:
      if flag > inital_inx: break
      temp_ways = []
      for pre_v in previous_visitors:
         for way in ways:
            next_vis = adjacency_set[pre_v] # Если путь закончивет одним из предыдущих знач, то добавлем следующее
            if pre_v in way:
               for v in next_vis:
                temp_ways.append(way + [v])
      ways = temp_ways
      
      leave_count = 0 # Если это число равно числу путей, то выходим из цикла
      for way in ways:
         if way[-1] >= final_inx:
            leave_count += 1
      if leave_count == len(ways):
          # расчет минимального пути, когда уже все пути посчитаны
          all_SUMM = []
          for way in ways:
              temp_sum = 0
              for i in range(len(way)-1):
                temp_sum += matrix[way[i]][way[i+1]]
              all_SUMM.append(temp_sum)
          min_dist = min(all_SUMM)
          optimal_way = ways[all_SUMM.index(min_dist)]
          return optimal_way, min_dist                      # RETURN

      previous_visitors = visitors
      visitors = []

      next_vis = []
      for way in ways:
        next_vis = adjacency_set[way[-1]]
        for next in next_vis:
          visitors.append(next)

      visitors = set(visitors)
      visitors = list(visitors)
      
      flag += 1

    
      




if __name__ == "__main__":

  stock, source = stock_source_search(matrix)
  ord_A, vertex_redefinition = ordered_graph(matrix) 

  ways = road_search(ord_A, 0, 16)

  print(ways)

  for i in range(17):
    print(ord_A[i])
  
  print(vertex_redefinition)