import xml.dom.minidom

import itertools

import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt


def main():
    """
    train_id - TrainId - Идентификатор поезда
    departure_station_id - DepartureStationId - Идентификатор станции отправления
    arrival_station_id - ArrivalStationId - Идентификатор станции прибытия
    price - Price - Цена
    :return:
    train_id
    departure_station_id
    arrival_station_id
    price
    """
    doc = xml.dom.minidom.parse("data.xml")

    train_id, departure_station_id, arrival_station_id, price = [], [], [], []

    for skill in doc.getElementsByTagName("TrainLeg"):
        train_id.append(skill.getAttribute("TrainId"))

    for skill in doc.getElementsByTagName("TrainLeg"):
        departure_station_id.append(skill.getAttribute("DepartureStationId"))

    for skill in doc.getElementsByTagName("TrainLeg"):
        arrival_station_id.append(skill.getAttribute("ArrivalStationId"))

    for skill in doc.getElementsByTagName("TrainLeg"):
        price.append(skill.getAttribute("Price"))

    return train_id, departure_station_id, arrival_station_id, price


def graph(train_id, departure_station_id, arrival_station_id, price):
    """
    :param train_id:
    :param departure_station_id:
    :param arrival_station_id:
    :param price:
    :return:
    matrix
    """
    matrix = [[0] * len(set(arrival_station_id)) for _ in range(len(set(arrival_station_id)))]
    index = []
    count_index = 0
    for i in set(arrival_station_id):
        index.append((count_index, i))
        count_index += 1

    trip_data = []
    for i in set(departure_station_id):
        data_all, data_ = [], []
        iter = 0
        for j in departure_station_id:
            if i == j:
                data_all.append((train_id[iter], i, arrival_station_id[iter], price[iter]))
            iter += 1

        for arrival in set(arrival_station_id):
            j = 0
            data = []
            while j < len(data_all):
                if arrival == data_all[j][2]:
                    data.append(data_all[j])
                j += 1
            k = 0
            if len(data) != 0:
                minimum = data[0]
                while k < len(data):
                    if minimum[3] > data[k][3]:
                        minimum = data[k]
                    k += 1
                data_.append(minimum)
        trip_data.append(data_)
    print(trip_data)
    arrival = []
    for i in set(arrival_station_id):
        arrival.append(i)

    i = 0
    while i < len(trip_data):
        j = 0
        while j < len(trip_data[i]):
            count_y, count_x = 0, 0
            for k in range(len(index)):
                if index[k][1] == trip_data[i][j][1]:
                    count_x = k
            for k in range(len(index)):
                if index[k][1] == trip_data[i][j][2]:
                    count_y = k
            matrix[count_x][count_y] = float(trip_data[i][j][3])
            j += 1
        i += 1
    for i in range(len(matrix)):
        matrix[i][i] = float('inf')

    for row in matrix:
        for elem in row:
            print(elem, end='   ')
        print()

    return matrix, index, trip_data


# Функция нахождения минимального элемента, исключая текущий элемент
def minimum(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


# функция удаления нужной строки и столбцах
def delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


# Функция вывода матрицы
def print_matrix(matrix):
    print("---------------")
    for i in range(len(matrix)):
        print(matrix[i])
    print("---------------")


def branches_and_borders(matrix):
    h, path_lenght = 0, 0
    strr, stb, res, result, start_matrix = [], [], [], [], []
    n = len(matrix)
    # n = 4
    # matrix = [[0, 5, 11, 9],[10, 0, 8, 7],[7, 14, 0,8],[12, 6, 15, 0]]
    # n = 5
    # matrix = [[0, 20, 18, 12, 8], [5, 0, 14, 7, 11], [12, 18, 0, 6, 11], [11, 17, 11, 0, 12], [5, 5, 5, 5, 0]]

    # Инициализируем массивы для сохранения индексов
    for i in range(n):
        strr.append(i)
        stb.append(i)
    # #
    # # # Вводим матрицу
    # # for i in range(n):
    # #     matrix.append(list(map(int, input().split())))
    #
    # Сохраняем изначальную матрицу
    for i in range(n):
        start_matrix.append(matrix[i].copy())

    # # Присваеваем главной диагонали float(inf)
    for i in range(n):
        matrix[i][i] = float('inf')
    # print(matrix)
    while True:
        # Редуцируем
        # --------------------------------------
        # Вычитаем минимальный элемент в строках
        for i in range(len(matrix)):
            temp = min(matrix[i])
            h += temp
            for j in range(len(matrix)):
                matrix[i][j] -= temp
        # Вычитаем минимальный элемент в столбцах
        for i in range(len(matrix)):
            temp = min(row[i] for row in matrix)
            h += temp
            for j in range(len(matrix)):
                matrix[j][i] -= temp

        # --------------------------------------

        # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
        # --------------------------------------
        null_max = 0
        index1 = 0
        index2 = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:
                    tmp = minimum(matrix[i], j) + minimum((row[j] for row in matrix), i)
                    if tmp >= null_max:
                        null_max = tmp
                        index1 = i
                        index2 = j
        # --------------------------------------

        # Находим нужный нам путь, записываем его в res и удаляем все ненужное
        res.append(strr[index1] + 1)
        res.append(stb[index2] + 1)

        old_index1 = strr[index1]
        old_index2 = stb[index2]
        if old_index2 in strr and old_index1 in stb:
            new_index1 = strr.index(old_index2)
            new_index2 = stb.index(old_index1)
            matrix[new_index1][new_index2] = float('inf')
        del strr[index1]
        del stb[index2]
        matrix = delete(matrix, index1, index2)
        if len(matrix) == 1:
            break

    # Формируем порядок пути
    for i in range(0, len(res) - 1, 2):
        if res.count(res[i]) < 2:
            result.append(res[i])
            result.append(res[i + 1])
    for i in range(0, len(res) - 1, 2):
        for j in range(0, len(res) - 1, 2):
            if result[len(result) - 1] == res[j]:
                result.append(res[j])
                result.append(res[j + 1])

    print("----------------------------------")
    # print('res =', result)

    # Считаем длину пути
    for i in range(0, len(result) - 1, 2):
        if i == len(result) - 2:
            path_lenght += start_matrix[result[i] - 1][result[i + 1] - 1]
            path_lenght += start_matrix[result[i + 1] - 1][result[0] - 1]
            print(start_matrix[result[i] - 1][result[i + 1] - 1])
            print(start_matrix[result[i + 1] - 1][result[0] - 1])
        else:
            path_lenght += start_matrix[result[i] - 1][result[i + 1] - 1]
            print(start_matrix[result[i] - 1][result[i + 1] - 1])

    print('price = ', path_lenght)
    return result


def print_id_triens(res, index, trip_data):
    data = []
    print(res)
    for i in res:
        j = 0
        while j < len(index):
            if i - 1 == index[j][0]:
                data.append(index[j][1])
            j += 1
    print(data)

    count_res = 0
    k = 0
    # print(trip_data)
    while k < len(res) - 1:
        i = 0
        while i < len(trip_data) - 1:
            j = 0
            while j < len(trip_data[i]):
                # print(data[count_res], data[count_res+1])
                if trip_data[i][j][1] == data[k] and trip_data[i][j][2] == data[k + 1]:
                    print(trip_data[i][j])
                    print(k)

                j += 1

            i += 1

        k += 1



if __name__ == "__main__":
    train_id, departure_station_id, arrival_station_id, price = main()
    matrix, index, trip_data = graph(train_id, departure_station_id, arrival_station_id, price)

    res = branches_and_borders(matrix)



    # print(Dijkstra(6, 1, matrix))
    graph = nx.Graph()

    kilometres = set()
    i = 0
    while i < len(departure_station_id):
        kilometres.add((departure_station_id[i], arrival_station_id[i], price[i]))
        i += 1

    graph.add_weighted_edges_from(kilometres)
    nx.draw_circular(graph,
                     node_color='red',
                     node_size=1000,
                     with_labels=True)
    plt.show()
