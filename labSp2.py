from tkinter import *
from tkinter import messagebox
from itertools import groupby
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

ar = [
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


def set_dim_click():
    global empty_cell_list, fill_cell_list, dim, height, ar
    try:
        empty_cell_list = []
        fill_cell_list = []
        temp = []
        dim = int(dim_box.get())
        if dim == 0 or dim < 0:
            messagebox.showinfo(message='Неверный формат ввода размерности!')
            window.focus()
            return
        if dim > 25:
            messagebox.showinfo(message='Размерность не может быть больше 25!')
            window.focus()
            return
        slaves = window.place_slaves()
        if slaves:
            for el in slaves:
                el.destroy()
        Label(window, text='Матрица смежности исходного графа').place(x=40, y=50)
        for i in range(dim):
            Label(window, text=i+1).place(x=30+i*20, y=80)
            Label(window, text=i+1).place(x=8, y=110+i*20)
        for i in range(dim):
            for j in range(dim):
                if dim == 17:
                    v1 = StringVar()
                    v1.set(ar[i][j])
                    if ar[i][j]!=0:
                        temp.append(Entry(window, width=3, textvariable=v1,bg='mint cream'))
                    else:
                        temp.append(Entry(window, width=3, textvariable=v1))
                else:
                    v1 = StringVar()
                    temp.append(Entry(window, width=3, textvariable=v1))
            empty_cell_list.append(temp)
            temp = []
        for i in range(dim):
            for j in range(dim):
                empty_cell_list[i][j].place(x=33+j*20, y=113+i*20)
        apply_btn = Button(window, text='Задать матрицу', command=apply_click)
        apply_btn.place(x=(33+dim*20)/2-30, y=120+dim*20)
    except ValueError:
        messagebox.showinfo(message='Размерность может быть только числом!')
        window.focus()


def apply_click():
    global empty_cell_list, fill_cell_list, dim, result, fill_cell_list_0, renum_list
    try:
        temp = []
        for i in range(dim):
            for j in range(dim):
                temp.append(int(empty_cell_list[i][j].get()))
                if int(empty_cell_list[i][j].get()) < 0:
                    messagebox.showinfo(message='Значения матрицы не могут быть отрицательными!')
                if i == j and int(empty_cell_list[i][j].get()) != 0:
                    messagebox.showinfo(message='На диагонали должны быть нули!')
                    return
            fill_cell_list.append(temp)
            temp = []
        levels(fill_cell_list)
        stok = []
        istok = []
        fill_cell_list_0 = fill_cell_list.copy()
        for i in range(dim):
            for j in range(dim):
                if fill_cell_list_0[i][j] == math.inf:
                    fill_cell_list_0[i][j] = 0
        for i in range(dim):
            if sum(fill_cell_list_0[i]) == 0:
                stok.append(i+1)
        for i in range(dim):
            summa = 0
            for j in range(dim):
                summa += fill_cell_list_0[j][i]
            if summa == 0:
                istok.append(i+1)
        Button(window, text='Показать упорядочивание вершин', command=renum).place(x=-100+dim*30, y=160,width=400)
        Button(window, text='Показать стоки/истоки', command=stokistok).place(x=-100 + dim * 30, y=130,width=400)
        Button(window, text='Показать уровни графа', command=urovni).place(x=-100 + dim * 30, y=100,width=400)
        Button(window, text='Построить матрицу смежности       \n упорядоченного графа',
               command=new_matrix).place(x=-100+dim*30, y=190,width=400)
        Button(window, text='        Показать исходный граф          ', command=source_graph).place(x=-100 + dim * 30,
                                                                                                    y=230,width=400)
        counter = 0
        renum_list = []
        for i in range(len(result)):
            for j in range(len(result[i])):
                counter += 1
                renum_list.append([counter, result[i][j]])
    except ValueError:
        messagebox.showinfo(message='Элементы матрицы могут быть только числами!')
        window.focus()



def renum():
    global result, renum_list
    window_2 = Tk()
    window_2.geometry('300x500')
    window_2.title('Упорядочивание вершин')
    counter = 0
    renum_list = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            counter += 1
            renum_list.append([counter, result[i][j]])

    Label(window_2, text='Упорядочивание вершин').place(x=10, y=10)
    for i in range(len(renum_list)):
        for j in range(0, len(renum_list[i]), 2):
            Label(window_2, text=f'{renum_list[i][j]} --> {renum_list[i][j+1]}').place(x=10, y=30+i*20)

def levels(fill_cell_list):
    global result
    for i in range(len(fill_cell_list)):
        for j in range(len(fill_cell_list)):
            if fill_cell_list[i][j] == 0:
                fill_cell_list[i][j] = math.inf

    digs = []
    temp = []
    for i in range(len(fill_cell_list)):
        for j in range(len(fill_cell_list)):
            if fill_cell_list[j][i] != math.inf:
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

def urovni():
    global empty_cell_list, fill_cell_list, dim, result, fill_cell_list_0, renum_list
    print(empty_cell_list, fill_cell_list, dim, result, fill_cell_list_0, renum_list, sep='\n||||')
    levels(fill_cell_list)
    window_10 = Tk()
    window_10.geometry('300x500')
    window_10.title('Уровни графа')
    Label(window_10, text='Уровни графа').place(x=10, y=10)
    for i in range(len(result)):
        Label(window_10, text=f'N{i}=').place(x=10, y=30+i*20)
        temp1 = []
        for j in range(len(result[i])):
            temp1.append(result[i][j])
        Label(window_10, text='{ ' + f'{i + 1} ' + f'{temp1}' + ' }').place(x=30, y=30+i*20)

def stokistok():
    global empty_cell_list, fill_cell_list, dim, result, fill_cell_list_0, renum_list
    levels(fill_cell_list)
    window_11 = Tk()
    window_11.geometry('300x500')
    window_11.title('Стоки и истоки')
    stok = []
    istok = []
    fill_cell_list_0 = fill_cell_list.copy()
    for i in range(dim):
        for j in range(dim):
            if fill_cell_list_0[i][j] == math.inf:
                fill_cell_list_0[i][j] = 0
    for i in range(dim):
        if sum(fill_cell_list_0[i]) == 0:
            stok.append(i + 1)
    for i in range(dim):
        summa = 0
        for j in range(dim):
            summa += fill_cell_list_0[j][i]
        if summa == 0:
            istok.append(i + 1)
    Label(window_11, text='Стоки:').place(x=10, y=10)
    for i in range(len(stok)):
        Label(window_11, text=stok[i]).place(x=10 + i * 20, y=30)
    Label(window_11, text='Истоки:').place(x=10, y=50)
    for i in range(len(istok)):
        Label(window_11, text=istok[i]).place(x=10 + i * 20, y=70)


def new_matrix():
    global fill_cell_list_0, dim, renum_list, new_matr, size
    temp_i, temp_j = 0, 0
    new_matr = []
    size = 380 + dim * 30
    Label(window, text='Матрица смежности упорядоченного графа').place(x=size, y=50)
    Button(window, text='Найти путь и его минимальную\n длину', command=min_path).place(
        x=size, y=0 + dim * 30)
    Button(window, text='Показать упорядоченный граф', command=trans_graph).place(x=-100 + dim * 30, y=260,width=400)
    for i in range(dim):
        Label(window, text=i + 1).place(x=size+i*20, y=80)
        Label(window, text=i + 1).place(x=size-25, y=111 + i * 20)
    istok.place(x=size, y=50 + dim * 30)
    Label(window, text='Из:').place(x=size - 30, y=50 + dim * 30)
    stok.place(x=size + 75, y=50 + dim * 30)
    Label(window, text='В:').place(x=size + 50, y=50 + dim * 30)
    for i in range(dim):
        temp = []
        for j in range(dim):
            for k in range(len(renum_list)):
                if i+1 == renum_list[k][0]:
                    temp_i = renum_list[k][1]
                if j+1 == renum_list[k][0]:
                    temp_j = renum_list[k][1]
            v2 = StringVar()
            if fill_cell_list_0[temp_i-1][temp_j-1] == 0:
                v2.set('')
                temp.append(Entry(window, width=3, textvariable=v2))
            else:
                v2.set(fill_cell_list_0[temp_i-1][temp_j-1])
                temp.append(Entry(window, width=3, textvariable=v2,bg='mint cream'))
        new_matr.append(temp)
    for i in range(dim):
        for j in range(dim):
            new_matr[i][j].place(x=size+j*20, y=113+i*20)
    
    
def source_graph():
    global dim, COLORS, fill_cell_list_0
    print(dim)
    print(fill_cell_list_0)
    G = nx.from_numpy_matrix(np.matrix(fill_cell_list_0), create_using=nx.DiGraph)
    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True,node_color='green',width=0.5,arrowstyle='-|>',verticalalignment='bottom',arrowsize=20,node_size=500)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    plt.show()


def trans_graph():
    global dim, result, new_matr
    temp=[]
    m=[]
    for i in range(dim):
        for j in range(dim):
            temp.append(new_matr[i][j].get())
        m.append(temp)
        temp=[]
    for i in range(dim):
        for j in range(dim):
            if m[i][j] == '':
                m[i][j] = '0'
            m[i][j] = int(m[i][j])

    print(m)
    G = nx.from_numpy_matrix(np.matrix(m), create_using=nx.DiGraph)
    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True,node_color='yellow',width=0.5,arrowstyle='-|>',verticalalignment='bottom',arrowsize=20,node_size=500)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    try:
        zukl = nx.find_cycle(G)
        messagebox.showinfo(message=f'В графе найден цикл {zukl}')
    except:
        pass
    plt.show()
    



def min_path():
    global new_matr, dim, size, istok, stok, m
    temp = []
    m = []
    for i in range(dim):
        for j in range(dim):
            temp.append(new_matr[i][j].get())
        m.append(temp)
        temp = []
    for i in range(dim):
        for j in range(dim):
            if m[i][j] == '':
                m[i][j] = '0'
            m[i][j] = int(m[i][j])
    G = nx.from_numpy_matrix(np.matrix(m), create_using=nx.DiGraph)
    summa = 0
    try:
        path = nx.dijkstra_path(G, int(istok.get()) - 1, int(stok.get()) - 1)
        if path != None:
            for i in range(len(path) - 1):
                summa += G[path[i]][path[i + 1]]['weight']
        Label(window,
              text='                                                                                        ').place(
            x=size + 40 + i * 40, y=80 + dim * 30)
        Label(window,
              text='                                                                                                ').place(
            x=size, y=110 + dim * 30)
        path = [i + 1 for i in path]
        Label(window, text='Путь: ').place(x=size, y=80 + dim * 30)
        Label(window, text='Длина пути: ').place(x=size, y=110 + dim * 30)
        Label(window, text=summa).place(x=size + 90, y=110 + dim * 30)
        Label(window, text=path).place(x=size + 90, y=80 + dim * 30)
    except:
        messagebox.showinfo(message='Нет пути или неправильно указаны вершины')
        window.focus()
        istok.focus_set()
        return


###main###


result, fill_cell_list_0, new_matr = [], [], []
empty_cell_list, fill_cell_list, renum_list = [], [], []
dim, height, size = 0, 0, 0
window = Tk()
window.geometry('1440x900')
window.title('Упорядочивание графов')
v = StringVar()
v1 = StringVar()
v2 = StringVar()
stok = Entry(window, width=5, textvariable=v1)
istok = Entry(window, width=5, textvariable=v2)
dim_label = Label(window, text='Введите размерность матрицы  ')
dim_box = Entry(window, width=5, textvariable=v)
dim_box.insert(0,17)
dim_label.grid(column=0, row=0)
dim_box.grid(column=1, row=0)
Label(window, text='  ').grid(column=2, row=0)
dim_set_btn = Button(window, text='Применить', command=set_dim_click)
dim_set_btn.grid(column=3, row=0)
window.mainloop()
