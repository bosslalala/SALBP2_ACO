import random
import numpy as np
import math
import copy

#全局参数定义
num_work = 11#工序数
num_workbench = 3#工位数
num_total = 1000#随机生成的初始解个数
copy_num = 70 #保留的解的个数
var_num=10 #变异的解的个数
best_order = []
min_si = 0
#工序详情
works = {'A':45, 'B':11, 'C':9, 'D':50, 'E':15, 'F':12, 'G':12, 'H':12, 'I':12, 'J':8, 'K':9}
#邻接矩阵表示作业循序图
matrix = [[0,1,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,1,0,0,0,0],
          [0,0,0,0,1,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,1,1,0,0],
          [0,0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0,0,0,1],
          [0,0,0,0,0,0,0,0,0,0,0]]
#拓扑排序用到的标志数组
flag = [1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1] #1可选，0已选，-1不可选
#工序名称
work = ['A','B','C','D','E','F','G','H','I','J','K']
#理想最优解
theory_best = 0
for value in works.values():
    theory_best += value
theory_best /= num_workbench

#拓扑排序,待优化可以生成随机拓扑排序
#拓扑排序,待优化可以生成随机拓扑排序
def get_sequence():
    temp_flag = flag[:]
    temp_matrix = copy.deepcopy(matrix)
    seq = []
    for i in range(num_work):
        #print(temp_matrix)
        #随机选一个入度为0的结点
        zero_list = []
        for j in range(num_work):
            if temp_flag[j]==1:
                zero_list.append(work[j])
        this = random.choice(zero_list)
        #print(this)
        seq.append(this)
        temp = ord(this)-ord('A')
        temp_flag[temp] = 0
        #更新flag标志数组
        for k in range(num_work):
            if temp_matrix[temp][k]==1:
                temp_matrix[temp][k] = 0
                if temp_flag[k]==-1:
                    sum = 0
                    for m in range(num_work):
                        sum += temp_matrix[m][k]
                    if sum==0:
                        temp_flag[k]=1
    return seq

#获得所有拓扑排序结果
def get_order(seq):
    temp_seq = seq[:]
    temp_seq.reverse()
    order = []
    temp_work = temp_seq.pop()
    for i in range(num_workbench):
        #print(i)
        #print(temp_work)
        sub_order = []
        time = works[temp_work]
        sub_order.append(temp_work)
        temp_work = temp_seq.pop()
        while(time + works[temp_work] <= theory_best):
            #print(temp_work)
            time += works[temp_work]
            sub_order.append(temp_work)
            if(temp_seq):
                temp_work = temp_seq.pop()
        order.append(sub_order)
    while(temp_seq):
        order[num_workbench-1].append(temp_seq.pop())
    while(work[-1] in order[-1]):
        order[-1].remove(work[-1])
    order[-1].append(work[-1])
    return order

def get_order_2(seq):
    temp_seq = seq[:]
    temp_seq.reverse()
    order = []
    temp_work = temp_seq.pop()
    for i in range(num_workbench):
        #print(i)
        #print(temp_work)
        sub_order = []
        time = works[temp_work]
        sub_order.append(temp_work)
        temp_work = temp_seq.pop()
        while(time + works[temp_work] <= theory_best*1.1):
            #print(temp_work)
            time += works[temp_work]
            sub_order.append(temp_work)
            if(temp_seq):
                temp_work = temp_seq.pop()
        order.append(sub_order)
    while(temp_seq):
        order[num_workbench-1].append(temp_seq.pop())
    while (work[-1] in order[-1]):
        order[-1].remove(work[-1])
    order[-1].append(work[-1])
    return order
#计算si
def get_si(order):
    times = []
    for i in range(num_workbench):
        time = 0
        for j in order[i]:
            time += works[j]
        times.append(time)
    times.sort()
    ct = times[num_workbench-1]
    sum = 0
    for i in range(num_workbench):
        sum += (ct-times[i])*(ct-times[i])
    sum = sum / num_workbench
    si = math.sqrt(sum)
    return si

#生成初始种群
def generate_initial():
    initial = []
    for i in range(num_total):
        p = get_sequence()
        initial.append(p)
    return initial
#计算适应度，即si值
#计算适应度，即si值
def get_all_si(population):
    sis = []
    for i in population:
        order = get_order(i)
        sis.append(get_si(order))
    return sis
def get_all_si_2(population):
    sis = []
    for i in population:
        order = get_order_2(i)
        sis.append(get_si(order))
    return sis
initial = generate_initial()
sis = get_all_si(initial)
sis_2 = get_all_si_2(initial)
min_si = sis[0]
best = 0
for i in range(len(sis)):
    if sis[i]<min_si:
        best = i
        min_si = sis[i]
print(initial[best])
print(get_order(initial[best]))
print(min_si)

sis_2 = get_all_si_2(initial)
min_si = sis_2[0]
best = 0
for i in range(len(sis_2)):
    if sis[i]<min_si:
        best = i
        min_si = sis_2[i]
print(initial[best])
print(get_order(initial[best]))
print(min_si)