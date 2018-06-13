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
def upper_bupper(ub, l, u):
    if ub == 'f':
        diff = abs(a-b)
        return diff/l, diff/u
    else:
        return  l, u    

if llist[0] == 'f':
    check_func = True

def turn_length(tl, value ,delta):
    if tl == 't':
        return 2*pi*value, pi/delta   
    else:    
        return value, 1/delta

a = float(llist[1])
b = float(llist[2])
n = float(llist[3])
limit, inc_calc = turn_length(llist[4],float(llist[5]),float(llist[6]))
lower_bound, upper_bound = upper_bupper(llist[0],float(llist[7]),float(llist[8]))
delta_limit = limit/float(llist[9])

print(str(a) + " " + str(b)+ " " + str(n) + " " + str(limit)+ " " +str(inc_calc) + " " +str(lower_bound) + " " +str(upper_bound))
#sys.exit()
phi = Symbol('phi')
y = (a-b)*((phi/limit)**n) + b
yprime = y.diff(phi)



f = lambdify(phi, y, 'numpy')
fprime = lambdify(phi, yprime, 'numpy')

def conv_deg(slope):
    return degrees(atan(slope))

def calc_norm(count, increment, funct):
    square = funct(count)
    count += increment
    circle = funct(count)
    if not check_func:
        square = conv_deg(square)
        circle = conv_deg(circle)
    diff = abs(square-circle)
    if diff < 0.0001:
        return 0
    return float(diff)

def found_angle(count, increment):
    if check_func:
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
count = 0
#count = 0.0001
inc_list = list()
while count < limit:
    angle_list.append(count)
    inc = found_angle(count,increment)
    if inc > delta_limit:
        inc = delta_limit
    inc_list.append(inc)
    count += inc

angle_list.append(limit)

length = len(angle_list)-1
#norm_list= [(float((f(angle_list[i+1])-f(angle_list[i]))/f(angle_list[i+1])))*100 for i in range(length)]

norm_list= [abs(f(angle_list[i+1]) - f(angle_list[i])) for i in range(length)]

file = open('testfile.txt','w') 
file.write("point \t"+" difference y\t"+"nod1\t"+"nod2\t"+"increment\n\n")
for i in range(length):
    file.write(str(i+1) + " \t" + str(round(norm_list[i], 5)) +  str(i) + " \t" + str(angle_list[i]) +  " \t" + str(angle_list[i+1]) + " \t" + str(inc_list[i]) +"\n")
file.close()

file = open('auto_mesh.txt','w')
for a in angle_list:
    file.write(str(a) + "\n")
file.close()

#scatter.plot(angle_list, [f(x) for x in angle_list], marker = 'o')
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


if not check_func:
    plot_graph(angle_list, angle_list, 'derivative', fprime)
    scatter.figure()

plot_graph(angle_list, angle_list, 'function', f)
scatter.show()