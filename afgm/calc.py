from sympy import Symbol, diff, lambdify
import re, os, sys
import numpy as np
from math import pi, degrees, atan
import matplotlib.pyplot as scatter

gen_path = input("Enter the path: ")
define_file = open(gen_path , "r")
line = define_file.readline()
llist = re.split(r'\t+', line)
check_func = False
check_h = False

def upper_bupper(ub, l, u):
    if ub == 'd':
        return  l, u 
    else:
        diff = abs(a-b)
        return diff/l, diff/u

def turn_length(tl, value ,delta):
    if tl == 't':
        return 2*pi*value, pi/delta   
    else:    
        return value, delta

val_funct = llist[0]
a = float(llist[1])
b = float(llist[2])
n = float(llist[3])
limit, inc_calc = turn_length(llist[4],float(llist[5]),float(llist[6]))
lower_bound, upper_bound = upper_bupper(val_funct,float(llist[7]),float(llist[8]))
delta_limit = limit/float(llist[9])
upper_limit = limit

add_x = 0
count = 0
if val_funct == 'f':
    check_func = True
elif val_funct == 'h':
    upper_limit *= 0.5
    count = -limit/2
    add_x = 1/2
    check_h = True

check_d = not(check_func or check_h)
print("a b n upper_limit delta lower_bound upper_bound")
print(str(a) + " " + str(b)+ " " + str(n) + " " + str(upper_limit)+ " " +str(inc_calc) + " " +str(lower_bound) + " " +str(upper_bound))

phi = Symbol('phi')

def define_funct(a,b):
    y = (a-b)*(((phi/limit) + add_x)**n) + b
    f = lambdify(phi, y, 'numpy')
    return y, f

y, f = define_funct(a,b)

yprime = y.diff(phi)
fprime = lambdify(phi, yprime, 'numpy')

def conv_deg(slope):
    return degrees(atan(slope))

def calc_norm(count, increment, funct):
    square = funct(count)
    count += increment
    circle = funct(count)
    if check_d:
        square = conv_deg(square)
        circle = conv_deg(circle)
    diff = abs(square-circle)
    if diff < 0.0001:
        return 0
    return float(diff)

def found_angle(count, increment):
    if not check_d:
        norm = calc_norm(count, increment, f)
    else:
        norm = calc_norm(count, increment, fprime)
    if lower_bound <= norm and norm <= upper_bound:
        return inc_calc
    elif lower_bound > norm :
        return found_angle(count,increment*2) * 2
    elif upper_bound < norm:
        return found_angle(count, increment/3) / 3

angle_list = list()
increment = inc_calc

inc_list = list()
while count < upper_limit:
    angle_list.append(count)
    inc = found_angle(count,increment)
    if inc > delta_limit:
        inc = delta_limit
    inc_list.append(inc)
    count += inc

angle_list.append(upper_limit)

length = len(angle_list)-1

funct_list = [f(a) for a in angle_list]
norm_list= [abs(funct_list[i+1] - funct_list[i]) for i in range(length)]
norm_list_x = [abs(angle_list[i+1] - angle_list[i]) for i in range(length)]

def write_title(title_list, file):
    for title in title_list:
        file.write(title + "\t")
    file.write("\n\n")    

def write_list(data_list, file_title, title_list, dlength):
    file = open(file_title,'w') 
    write_title(title_list, file)
    length = int(len(data_list)/2)
    for i in range(dlength):
        for j in range(length):
            for k in range(data_list[2*j+1]):
                file.write("{0:0.10f}".format(data_list[j*2][i+k])+ "\t\t")
        file.write("\n")        

file = open('testfile.txt','w') 
title_list = ["point", "difference y", "nod1", "nod2", "increment"]
index_list = [i+1 for i in range(length)]
test_title = "testfile.txt"
last_title = "auto_mesh.txt"
if not check_h:
    data_list = [index_list, 1, norm_list, 1, angle_list, 2, inc_list, 1]
    write_list(data_list, test_title, title_list, length)

    data_list = [angle_list, 1]
    write_list(data_list, last_title, ["nod"], length+1)
else:
    add_title = ["difference x", "e1", "e2", "g1", "g2"]

    c = float(llist[10])
    d = float(llist[11])
    z, fz = define_funct(c,d)

    flist = [fz(a) for a in angle_list]
    data_list = [index_list,1,norm_list,1,angle_list,2, inc_list,1 ,norm_list_x,1,funct_list,2 ,flist,2]
    write_list(data_list, test_title, title_list+ add_title, length)

    data_list= [norm_list_x,1, funct_list,2 ,flist,2]
    write_list(data_list, last_title, add_title, length)

    print("sum --> " +str(sum(norm_list_x)))    

scatter.plot(range(length), norm_list, marker = 'x')
scatter.axhline(y=upper_bound, color='r', linestyle='-')
scatter.axhline(y=lower_bound, color='r', linestyle='-')
scatter.title('difference x')
scatter.draw()
scatter.figure()

def plot_graph(xaxis, yaxis, title, funct):
    scatter.plot(xaxis, [funct(x) for x in yaxis], marker = 'x')
    scatter.title(title)
    scatter.draw()

if check_d:
    plot_graph(angle_list, angle_list, 'derivative', fprime)
    scatter.figure()

plot_graph(angle_list, angle_list, 'function', f)
scatter.show()