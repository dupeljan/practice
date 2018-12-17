#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
from math import *

x_centre = 50
y_centre = 900
grid_div = 700
x_len = 1050
y_len = 950
width = 2
exact_solution= lambda x: pow( cos(x) , - 1/3 )

def f( x0 , y0 ):
    return y0 * tan( x0 ) - (2/3) * pow( y0 , 4 ) * sin (x0)

def DrawSolution( canvas  ,  dx , color= 'red'): # из ценра вправо на 1
    x0 = 0
    y0 = 1
    while ( x0 < 1 ):
        if (x0 + dx > 1): # Если линия выходит за границу области определения
            dx= 1 - x0
        x1 = x0 + dx
        y1 = y0 + dx *f( x0 , y0 )
        canvas.create_line( x_centre + x0 * grid_div , y_centre - y0 * grid_div , x_centre + x1 * grid_div , y_centre - y1 * grid_div , fill= color, width= width)
        x0 = x1
        y0 = y1

def DrawCoordGrid(canvas , width= 1 , color= "black"):
    d_grid = 10   #  len of grid_div
    value_of_division= 8
    canvas.create_line( 0 , y_centre , x_len, y_centre, width= width , fill= color ) #x
    canvas.create_line( x_centre, 0 , x_centre , y_len, width= width , fill= color ) #y

    #Рисуем стрелочку х
    canvas.create_text(x_len- d_grid, y_centre + 2 * d_grid , text="X")
    canvas.create_line(x_len - 2 * d_grid, y_centre -  d_grid, x_len, y_centre, width= width , fill= color  )
    canvas.create_line(x_len - 2 * d_grid, y_centre +  d_grid, x_len, y_centre, width=width, fill=color)

    #Рисуем стрелочку Y
    canvas.create_text(x_centre- d_grid,   d_grid , text="Y")
    canvas.create_line(x_centre -  d_grid,   2 * d_grid, x_centre, 0, width= width , fill= color  )
    canvas.create_line(x_centre +  d_grid,   2 * d_grid, x_centre, 0, width=width, fill=color)

    for i in range(0,  value_of_division *  round( x_len / grid_div  + 0.5 ) ):
        canvas.create_line(x_centre + (i/value_of_division) * grid_div, y_centre - d_grid , x_centre + (i/value_of_division) * grid_div , y_centre + d_grid )
        canvas.create_text(x_centre + (i/value_of_division) * grid_div, y_centre + 2*d_grid, text= (i/value_of_division))

    for j in range(0, value_of_division * round(y_len / grid_div  + 0.5) ):
        canvas.create_line(x_centre + d_grid, y_centre - ( j / value_of_division) * grid_div , x_centre - d_grid , y_centre -  (j / value_of_division) * grid_div )
        canvas.create_text(x_centre - 2*d_grid, y_centre - (j / value_of_division) * grid_div, text=(j / value_of_division))

def DrawFun(canvas, function  ,  lim , color = 'red'  ):
    x = 0
    while ( x <=  abs(lim) * grid_div ):
        canvas.create_line(  x_centre + x , y_centre  - grid_div * function( x / grid_div ) , x_centre + ( x + 1 ) , y_centre  - grid_div * function( ( x + 1 ) / grid_div ), fill= color , width= width )
        x+=1



def max_range_discrepancy(fun1,fun2,x0,len,dx):# len - протяженность по  х
    max= 0
    x_max= 0
    for x in range(0,grid_div*len + 1):
        dis= discrepancy(fun1,fun2,x/grid_div,x0,dx)
        if( dis> max):
            max= dis
            x_max= x
    return {"max val" : max, "max x" : x_max/grid_div}



def ReDrawSolution(canvas,dx, label_dx, label_dis, label_point_dis, label_n):
    if not hasattr(ReDrawSolution, '_state'):  # инициализация значения
        ReDrawSolution._state = 1
    #Закрашиваем предыдущую приближенную
    DrawSolution(canvas,ReDrawSolution._state,"white")
    ReDrawSolution._state = dx
    #Рисуем новую приближенную
    DrawSolution(canvas, ReDrawSolution._state,"blue")
    #При необходимости отрисывываем исходную функцию заново
    if(dx < 1/9):
        DrawFun(canvas, exact_solution , 1, 'red')
    #Изменяем label
    label_dx['text']= dx
    res= max_range_discrepancy(exact_solution, f, x0=0, len=1, dx=dx)
    label_dis['text']= res['max val']
    label_point_dis['text']= res['max x']
    label_n['text']=  round(1/dx - 0.5)

def discrepancy(fun1,fun2,x,x0,dx): # Неувязка в точке
    #Вычислим номер ближайшей точки
    n= round(x/dx -0.5)
    y0= fun1(x0)
    #Вычислим значение ломаной в этой точке
    for i in range(0,n):
        x1= x0 + dx
        y1= y0 + dx*fun2(x0,y0)
        x0 = x1
        y0 = y1
    #Добавим к нему линейное приращение
    val2_fun2= fun2(x0,y0)*(x-x0) + y0
    #c.create_line(x_centre + x*grid_div, y_centre - val2_fun2 * grid_div, x_centre + x*grid_div + 1, y_centre - val2_fun2*grid_div +1,fill="green",width= width)
    return abs( fun1(x) - val2_fun2 )

root = Tk()

root.title("Summer PRCT")
mainFrame = ttk.Frame(root, padding='10 10 10 10')

mainFrame.grid( column= 0 , row= 0 , sticky=(N,W,E,S))
# draw Fun
c = Canvas( mainFrame , width= x_len, height= y_len )
c.configure(background= 'white')
#Рисуем сетку
c.grid(column= 0 , row= 0 ,  sticky=( N, W, E, S), rowspan= 10,padx= 5 , pady= 5)
DrawCoordGrid( c )

DrawFun(c, exact_solution ,1, 'red' )
label_legend = Canvas( mainFrame )
label_legend.configure(background=root.cget("bg"))
label_legend.grid(column=1, row=0)
label_legend.create_text(150,100,text= "Точное решение y=cos(x)^(-1/3)", fill= "red",font= ("Helvetica", 14))


label_legend.create_text(125,150,text= "Приближенное решение", fill= "blue",font= ("Helvetica", 14))
ttk.Label(mainFrame, text='Неувязка',font= ("Helvetica", 14)).grid(column=1, row= 1,sticky=(S))
label_dis = ttk.Label(mainFrame,font= ("Helvetica", 14))

label_dis.grid(column=1, row= 2,sticky=(N))
ttk.Label(mainFrame, text='Точка макс неувязки',font= ("Helvetica", 14)).grid(column=1, row= 3,sticky=(S))
label_point_dis =ttk.Label(mainFrame,font= ("Helvetica", 14))
label_point_dis.grid(column=1, row= 4,sticky=(N))

ttk.Label(mainFrame, text='Кол-во разбиений',font= ("Helvetica", 14)).grid(column=1, row= 5,sticky=(S))
label_n = ttk.Label(mainFrame,font= ("Helvetica", 14))
label_n.grid(column= 1, row= 6,sticky=(N))

ttk.Label(mainFrame, text='dx',font= ("Helvetica", 14)).grid(column=1, row= 7,sticky=(S))
label_dx_val= ttk.Label(mainFrame,font= ("Helvetica", 14))
label_dx_val.grid(column=1, row= 8,sticky=(N))


scale = ttk.Scale(mainFrame ,orient = HORIZONTAL, length= 400, from_ = 1.0 , to_ = 1/100.0 ,
                  command= lambda x: ReDrawSolution(c, scale.get(),label_dx= label_dx_val,label_dis= label_dis, label_point_dis= label_point_dis, label_n= label_n) )

scale.grid(column = 1, row = 9 )

root.mainloop()


