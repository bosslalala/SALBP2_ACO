import random
import numpy as np
import math
import copy


#修改注释
'''
程序使用暴力求解，随机生成一万随机解，选择一个最优的
简单问题可以直接求解
复杂问题可以在此基础上使用启发式算法优化，如遗传算法，蚁群算法
没有处理输入，输入这部分把老师给的字符串转换成下边对应的参数就行
'''
#全局参数定义

num_work = 11#工序数
num_workbench = 4#工位数
num_total = 10000#随机生成的初始解个数
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


#输入
stations = [3,4,5]
work_seq = [['A','B'],['B','C'],['C','F'],['C','G'],['F','J'],['G','J'],['D','E'],['E','H'],['E','I'],['H','J'],['I','J'],['J','K']]
#获取老师给的输入，转换成对应的参数，这部分简单你自己写，加深印象

#拓扑排序,生成随机拓扑排序
#把此排序改成求拓扑排序的所有序列，即为暴力搜索算法
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

#生成排序对应的划分
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
    if(temp_work not in order[-1]):
        order[-1].append(temp_work)
    while(temp_seq):
        order[-1].append(temp_seq.pop())
    return order
#另一种生成排序对应的划分
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
        while(time + works[temp_work] <= theory_best*1.1):#只有这里和上边不一样
            #print(temp_work)
            time += works[temp_work]
            sub_order.append(temp_work)
            if(temp_seq):
                temp_work = temp_seq.pop()
        order.append(sub_order)
    if (temp_work not in order[-1]):
        order[-1].append(temp_work)
    while (temp_seq):
        order[-1].append(temp_seq.pop())
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
for work_bench in stations:
    best_order = []
    min_si = 0
    num_workbench = work_bench
    num_work = len(work)
    matrix = [[0 for i in range(num_work)] for i in range(num_work)]
    flag = [1 for i in range(num_work)]
    theory_best = 0
    for value in works.values():
        theory_best += value
    theory_best /= num_workbench
    for ab in work_seq:
        loc1 = ord(ab[0]) - ord('A')
        loc2 = ord(ab[1]) - ord('A')
        flag[loc2] = -1
        matrix[loc1][loc2] = 1

    flag_2 = 0  # 0是sis，1是sis_2
    initial = generate_initial()
    sis = get_all_si(initial)
    sis_2 = get_all_si_2(initial)

    min_si = sis[0]
    best = 0
    for i in range(len(sis)):
        if sis[i] < min_si:
            best = i
            min_si = sis[i]

    for i in range(len(sis_2)):
        if sis_2[i] < min_si:
            best = i
            min_si = sis_2[i]
            flag_2 = 1
    print("工位数：" + str(work_bench))
    if (flag_2 == 0):
        print(get_order(initial[best]))
        print(min_si)
    else:
        print(get_order_2(initial[best]))
        print(min_si)