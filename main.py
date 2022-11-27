import tkinter as tk
from tkinter import Entry, StringVar, PhotoImage, Tk
from tkinter import ttk, messagebox
import random as rnd
from functional import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def del_all_obj(reload=False):
    """Функция удаления всех виджетов"""
    try: frame_A_matrix.destroy()
    except: pass
    try: matrix_numbering_labels.destroy()
    except: pass
    try: frame_button.destroy()
    except: pass
    try: frame_A_orderedMatrix.destroy()
    except: pass
    try:
        for widget in matrix_numbering_labels:
            widget.destroy()
    except: pass
    try:
        for widget in ordMatrix_numbering_labels:
            widget.destroy()
    except: pass
    try:
        stockSource_label.destroy()
    except: pass
    try:
        for widget in graph_levels_labels:
            widget.destroy()
    except: pass
    try:
        for widget in ord_vertex_labels:
            widget.destroy()
    except: pass



def get_rgb(rgb):
    return "#%02x%02x%02x" % rgb 

def matrix_painting():
    """Выделение цветом ненулевых значений
    """
    for i in range(matrix_size):
        for j in range(matrix_size):
            try:
                if int(A_matrix[i][j].get()) != 0:
                    A_matrix[i][j].config({"background": get_rgb((128, 203, 196))})
            except:
                pass

    
def is_valid():
    matrix_painting()
    

def set_matrix(set_random=False):
    """Создание матрицы"""
    del_all_obj()
    global matrix_size
    while True:
        try:
            matrix_size = int(str(matrix_size_Entery.get()))    # кол-во столбцов и строк
        except:
            messagebox.showerror(title="Ошибка ввода", 
                message="Размерность матрицы должна иметь целые положительные значения.\n")
            return
        if matrix_size > 1 and matrix_size <= 20:
            break
        else:
            messagebox.showerror(title="Ошибка ввода", 
                message="Размерность матрицы должна быть в диапазоне между отчаянием и надеждой\nОт 2 до 20 включительно.")
            return

    global matrix_numbering_labels
    label_matrix = ttk.Label(root, text="Матрица смежности"); label_matrix.place(x=30, y=150+25)
    matrix_numbering_labels = [label_matrix]
    for i in range(matrix_size):
        temp = ttk.Label(root, text=str(i+1)); temp.place(x=30+i*20, y=175+25)
        matrix_numbering_labels.append(temp)
        temp = ttk.Label(root, text=str(i+1)); temp.place(x=10, y=220+i*20)
        matrix_numbering_labels.append(temp)

    global frame_A_matrix
    frame_A_matrix = tk.Frame(root, width=20*matrix_size, height=20*matrix_size)#, background="#b22222")
    frame_A_matrix.place(x=30, y=220)

    global A_matrix
    A_matrix = []   # матрица содержащая виджеты элементов исходной матрицы смежности

    if set_random:
        source, stock = rnd.randint(0, matrix_size-1), rnd.randint(0, matrix_size-1)
        for i in range(matrix_size):
            A_matrix.append([])
            for j in range(matrix_size):
                var = int()
                if i == stock or j == source or i == j:
                    var = 0
                else:
                    for v in range(10):
                        var = rnd.randint(0, 10)
                        if var == 0: break
                strVar = StringVar()
                strVar.set(str(var))
                temp_A_matrix = Entry(frame_A_matrix, width=3, textvariable=strVar, validate="all", validatecommand=matrix_painting); temp_A_matrix.place(x=20*j, y=20*i)
                A_matrix[i].append(temp_A_matrix)
        set_random = False
    else:
        if matrix_size == 17:
            for i in range(matrix_size):
                A_matrix.append([])
                for j in range(matrix_size):
                    strVar = StringVar()
                    strVar.set(str(matrix[i][j]))
                    temp_A_matrix = Entry(frame_A_matrix, width=3, textvariable=strVar, validate="all", validatecommand=matrix_painting); temp_A_matrix.place(x=20*j, y=20*i)
                    A_matrix[i].append(temp_A_matrix)
        else:
            for i in range(matrix_size):
                A_matrix.append([])
                for j in range(matrix_size):
                    temp_A_matrix = tk.Entry(frame_A_matrix, width=3, validate="all", validatecommand=matrix_painting); temp_A_matrix.place(x=20*j, y=20*i)
                    A_matrix[i].append(temp_A_matrix)
    matrix_painting()

    global frame_button
    frame_button = tk.Frame(root, width=360, height=150)#, background="#b22222")
    frame_button.place(x=640, y=10)
    tk.Button(frame_button, text="Показать уровни графа", command=output_graphLevels, width=50).place(x=0, y=0)
    tk.Button(frame_button, text="Показать стоки/истоки", command=output_sourceStock, width=50).place(x=0, y=25)
    tk.Button(frame_button, text="Показать упорядочивание вершин", command=output_orderedVertex, width=50).place(x=0, y=50)
    tk.Button(frame_button, text="Построить матрицу смежности упорядоченного графа", command=output_orderedMatrix, width=50).place(x=0, y=75)
    tk.Button(frame_button, text="Показать исходный граф", command=source_graph, width=50).place(x=0, y=100)
    tk.Button(frame_button, text="Показать упорядоченный граф", command=ordered_graph_plt     , width=50).place(x=0, y=125)

    
def check_source_stock(matr):
    stock, source = stock_source_search(matr)
    if stock == [] and source == []:
        messagebox.showerror(title="Ошибка ввода", 
                        message="Граф не имеет истока и стока")
        return -1
    if source == []:
        messagebox.showerror(title="Ошибка ввода", 
                        message="Граф не имеет истока")
        return -1
    if stock == []:
        messagebox.showerror(title="Ошибка ввода", 
                        message="Граф не имеет стока")
        return -1
    return 0

def readMatrix():
    """Чтение матрицы в глобальную переменную и проверка значений матрицы"""
    global A_matrix_value
    A_matrix_value = []
    for i in range(len(A_matrix)):
        A_matrix_value.append([])
        for j in range(len(A_matrix[i])):
            try:
                A_matrix_value[i].append(str(A_matrix[i][j].get()))
            except:
                A_matrix_value[i].append(str(A_matrix[i][j].cget('text')))
    for i in range(len(A_matrix)):
        for j in range(len(A_matrix[i])):
            try:
                A_matrix_value[i][j] = int(A_matrix_value[i][j])
                if A_matrix_value[i][j] < 0:
                    messagebox.showerror(title="Ошибка ввода", 
                        message="Значения элементов матриц должны иметь целые не отрицательные значения")
                    return -1
                if A_matrix_value[i][j] >= 1000000:
                    messagebox.showerror(title="Ошибка ввода", 
                        message="Значения элементов матриц должны быть меньше 1.000.000")
                    return -1
                if (i == j) and (A_matrix_value[i][j] != 0):
                    messagebox.showerror(title="Ошибка ввода", 
                        message="На главной диагонали должны быть нули!")
                    return -1
            except:
                messagebox.showerror(title="Ошибка ввода", 
                    message="Значения элементов матриц должны иметь целые не отрицательные значения")
                return -1

    if check_source_stock(A_matrix_value) != 0: return -1

    return 0


def output_orderedMatrix():
    """Функция для вывода упорядоченной матрицы"""

    global frame_A_orderedMatrix
    global ordMatrix_numbering_labels
    try:
        for widget in ordMatrix_numbering_labels:
            widget.destroy()
    except: pass
    try: frame_A_orderedMatrix.destroy()
    except: pass
    
    if readMatrix() != 0: return
    
    ord_A_matrix = ordered_graph(A_matrix_value)[0]     # упорядочивание матрицы смежности

    # вывод упорядоченной матрицы
    label_ordMatrix = ttk.Label(root, text="Матрица смежности упорядоченного графа")
    label_ordMatrix.place(x=len(A_matrix_value[0])*30-45+300, y=150+25)
    ordMatrix_numbering_labels = [label_ordMatrix]
    for i in range(matrix_size):
        temp = ttk.Label(root, text=str(i+1)); temp.place(x=len(A_matrix_value[0])*30+i*20-20+300, y=175+25)
        ordMatrix_numbering_labels.append(temp)
        temp = ttk.Label(root, text=str(i+1)); temp.place(x=len(A_matrix_value[0])*30-25-20+300, y=220+i*20)
        ordMatrix_numbering_labels.append(temp)
    
    
    frame_A_orderedMatrix = tk.Frame(root, width=25*len(A_matrix_value[0]), height=20*len(A_matrix_value[0]))#, background="#b22222")
    frame_A_orderedMatrix.place(x=30*len(A_matrix_value)-25+300, y=220)

    A_ordMatrix_output_lb = []
    for i in range(len(A_matrix_value)):
        A_ordMatrix_output_lb.append([])
        for j in range(len(A_matrix_value[i])):
            # Первое преобразование
            if ord_A_matrix[i][j] != 0: color = get_rgb((128, 203, 196))
            else: color = "White"
            temp = tk.Label(frame_A_orderedMatrix, width=3, text=ord_A_matrix[i][j], background=color); temp.place(x=20*j, y=20*i)
            A_ordMatrix_output_lb[i].append(temp)


def output_sourceStock():
    """Вывод стока и истока на экран"""
    global stockSource_label
    try: stockSource_label.destroy()
    except: pass
    if readMatrix() != 0: return
    stock, source = stock_source_search(A_matrix_value)
    labelsText = "Стоки: "
    for st in stock:
        labelsText += str(st+1)

    labelsText += "\nИстоки: "
    for sr in source:
        labelsText += str(sr+1)

    stockSource_label = ttk.Label(root, text=labelsText)
    stockSource_label.place(x=20, y=20*len(A_matrix_value)+195+45)

    
def output_graphLevels():
    """Вывод на экран уровней графа"""
    global graph_levels_labels
    try:
        for widget in graph_levels_labels:
            widget.destroy()
    except: pass

    if readMatrix() != 0: return

    graph_levelsDict = ordered_graph(A_matrix_value)[2]

    headerLabel = ttk.Label(root, text="Уровни графа")
    headerLabel.place(x=25*len(A_matrix_value)-25, y=195)
    graph_levels_labels = [headerLabel]
    i=0
    for key in graph_levelsDict.keys():
        adj = graph_levelsDict[key]
        labelText = "N" + str(i+1) + ": {" + str(key+1) + ": ["
        i+=1
        for v in adj:
            labelText += str(v) + ", "
        labelText = labelText[0:len(labelText)-2] + "]}"
        temp = ttk.Label(root, text=labelText)
        temp.place(x=25*len(A_matrix_value)-20, y=195+20*i)
        graph_levels_labels.append(temp)


def output_orderedVertex():
    """Вывод на экран упорядочивание вершин"""
    global ord_vertex_labels
    try:
        for widget in ord_vertex_labels:
            widget.destroy()
    except: pass

    if readMatrix() != 0: return

    ord_vertex = ordered_graph(A_matrix_value)[1]   # словарь ключ - старый индекс, значение - новый индекс

    headerLabel = ttk.Label(root, text="Упорядочивание вершин")
    headerLabel.place(x=25*len(A_matrix_value)+150-25, y=195)
    ord_vertex_labels = [headerLabel]

    i=0
    for key in ord_vertex.keys():
        i+=1
        vertext_new = ord_vertex[key]
        labelText = str(vertext_new+1) + "-->" + str(key+1)
        temp = ttk.Label(root, text=labelText)
        temp.place(x=25*len(A_matrix_value)+125, y=195+20*i)
        ord_vertex_labels.append(temp)


def source_graph():
    """График исходного графа"""
    if readMatrix() != 0: return
    matrix = A_matrix_value
    fig = plt.figure()
    G = nx.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph)
    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True,node_color='green',width=0.5,arrowstyle='-|>',verticalalignment='bottom',arrowsize=20,node_size=500)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    fig.savefig("sourceGraph.png")
    image = Image.open("sourceGraph.png")
    image.show()


def ordered_graph_plt():
    """График упорядоченного графа"""
    if readMatrix() != 0: return
    ord_A_matrix = ordered_graph(A_matrix_value)[0]

    fig = plt.figure()
    G = nx.from_numpy_matrix(np.matrix(ord_A_matrix), create_using=nx.DiGraph)
    layout= nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True,node_color='yellow',width=0.5,arrowstyle='-|>',verticalalignment='bottom',arrowsize=20,node_size=500)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    try:
        zukl = nx.find_cycle(G)
        messagebox.showinfo(message=f'В графе найден цикл {zukl}')
    except:
        pass
    fig.savefig("orderedGraph.png")
    image = Image.open("orderedGraph.png")
    image.show()



# def graph_window(ord=False):
#     """Отдельное окно для визуализации графа"""
#     window = Tk()
#     window.geometry('1366x786+0+0')    # ширина на высоту и сколько пикселей от верхнего левого угла

#     if not ord:
#         source_graph()
#         title_ = "Визуализация исходного графа"
#         file = "sourceGraph.png"
        
#     else:
#         ordered_graph_plt()
#         title_ = "Визуализация упорядоченного графа"
#         file = "orderedGraph.png"

#     window.title(title_)
#     img = PhotoImage(file=file)
#     graph = ttk.Label(window, image=img)
#     graph.image_ref = img
#     graph.place(x=0, y=0)

#     window.mainloop()

    

root = Tk()
root.geometry('1366x786+0+0')    # ширина на высоту и сколько пикселей от верхнего левого угла
root.title("Упорядочиванеи графа. Оценки времени подготовки документов.")
frm = ttk.Frame(root, padding=10)   # основная рамка
frm.grid(column=10, row=10)



ttk.Label(frm, text="Введите размерность матрицы смежности").grid(column=0, row=0)
matrix_size_Entery_text = StringVar()
matrix_size_Entery = tk.Entry(frm, textvariable=matrix_size_Entery_text); matrix_size_Entery.grid(column=1, row=0)
matrix_size_Entery.insert(0, 17)



tk.Button(root, text="Задать матрицу", command=set_matrix, width=35).place(x=380, y=10)
tk.Button(root, text="Задать матрицу со случайными числами", command=lambda: set_matrix(set_random=True), width=35).place(x=380, y=35)
root.mainloop()