import numpy as np # Подключим библиотеку NumPy
import matplotlib.pyplot as plt  # Подключим библиотеку Matplotlib с коллекцией функций pyplot
from scipy.stats import chi2_contingency # Подключим библиотеку SciPy
import datetime # Подключим библиотеку Datetime

polynomial_degree = 3 # Задаём степень полинома

path_file = "/content/DataPrV7.csv" # Задаём путь к файлу

delim = "," # Указываем разделитель

alpha = 0.05 # Задаём уровень достоверности

x_title = "Время" # Задаём заголовок оси x

y_title = "Цена за 1 кв.м." # Задаём заголовок оси y

graphic_title = "Динамика изменения стоимости жилья на первичном рынке (Россия)" # Задаём заголовок графику

data = np.genfromtxt(path_file, delimiter=delim, dtype= None, encoding = 'utf-8') # читаем данные

lenght_data = len(data) # Рассчитываем длину входного массива данных

data_divided_time = []  # Создаём массив для хранения даты: года, месяца и дня
data_number = [] # Создаём массив для хранения целых чисел, соответствующих датам по оси x
data_y = [] # Создаём массив для хранения значений по оси y
data_time = [] # Создаём массив для хранения даты типа datetime

for i in range(lenght_data):   # наполняем массивы данными
     data_divided_time.append(data[i][0].split('.'))
     data_number.append(i)
     data_y.append(data[i][1])
     data_time.append(datetime.datetime( int(data_divided_time[i][2]),int(data_divided_time[i][1]), int(data_divided_time[i][0]) ))

lenght_data_graduate = int(lenght_data*0.7) # Вычисляем длину обучающего множества

lenght_data_test = lenght_data - lenght_data_graduate  # Вычисляем длину тестового множества

x_graduate = data_number[:lenght_data_graduate] # Вставляем в переменную первую колонку. Обучающее множество

y_graduate = data_y[:lenght_data_graduate] # Вставляем в переменную вторую колонку. Обучающее множество

x_test = data_number[lenght_data_graduate:] # Вставляем в переменную первую колонку. Тестовое множество

y_test= data_y[lenght_data_graduate:] # Вставляем в переменную вторую колонку. Тестовое множество

fx = np.polyfit(x_graduate, y_graduate, polynomial_degree) # Рассчитываем коэффициенты полинома
print('Коэффициенты полинома:', fx) # Печатаем коэффициенты полинома

fp = np.linspace(data_number[0], int(data_number[0]+lenght_data), int(data_number[0]+lenght_data)) # Начальная точка, конечная, количество точек между ними
z = np.poly1d(fx) # Превращаем fx в функцию z
bd_new_f = z(fp) # Рассчитываем значения полнима и заносим их в массив bd_new_f
plt.figure(figsize = (20,10)) # Задаём размеры прорисовки окна
plt.xlabel(x_title, fontsize=16)
plt.ylabel(y_title, fontsize=16)
plt.title(label = graphic_title, fontsize = 18)
plt.autoscale(tight=True) # Чтобы на графике не было лишних полей
plt.scatter(data_time[:lenght_data_graduate] ,y_graduate)  # Рисуем исходные точки
plt.scatter(data_time[lenght_data_graduate:] ,y_test, c = 'deeppink')  # Рисуем тестовые точки
plt.grid() # Рисуем сетку
plt.plot(data_time, bd_new_f , linewidth = 2) # Рисуем график получившейся функции
plt.show() # Показываем график

y_bd_new_f= bd_new_f[lenght_data_graduate:] # Вставляем в переменную вторую колонку. Значения по оси Y полинома. Это теоретическая величина.

y_bd_new_f_int = [] # Формируем массив-дублер y_bd_new_f только он будет типа int для корректной интерпретации далее

for i in y_bd_new_f:
     y_bd_new_f_int.append(int(i))

data2 = [y_test, y_bd_new_f] # Формируем входной массив данных для проверки на адекватность модели

stat, p, dof, expected = chi2_contingency(data2) # Рассчитываем p-значение

if p <= alpha:
     print( 'Распределение не соответствует Хи-квадрат, при уровне значимости', str(100*alpha)+ '% и p = '+ str (p))
else:
     print( 'Распределение соответствует Хи-квадрат, при уровне значимости', str(100*alpha)+ '% и p = '+ str (p))
