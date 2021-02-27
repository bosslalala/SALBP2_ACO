import math
import random
import numpy as np
import copy
class Ant(object):

    #初始化
    def __init__(self,ID,num_work,num_workbench,work,works,work_rely):
        self.id = ID
        self.num_work = num_work  # 工序数
        self.num_workbench = num_workbench #工位数
        self.works = works #工序详情
        self.work = work #工序列表
        self.work_rely = work_rely #紧前关系
        self.cm = self.get_cm()  # 理想平均节拍
        self.matrix = self.get_matrix() #邻接矩阵
        self.succeed = self.get_succeed() #后继列表
        self.alpha = 1  # 信息素因子
        self.beta = 5  # 启发式函数因子
        self.seq = []
        self.clean_param()


    def clean_param(self):

        self.tabu = []  # 禁忌表
        self.allow = self.get_first_allow()  # 候选表
        self.si = 100  # si值
        self.ct = self.cm  # 实际节拍
        self.order = self.get_init_order()  # 作业分配结果

    def get_cm(self):
        cm = 0
        for value in self.works.values():
            cm += value
        cm /= self.num_workbench
        return cm

    def get_ct(self):
        times = []
        for i in range(self.num_workbench):
            time = 0
            for j in self.order[i]:
                time += self.works[j]
            times.append(time)

        times.sort()
        ct = times[self.num_workbench-1]
        return ct

    def get_matrix(self):
        matrix = [[0 for i in range(self.num_work)] for i in range(self.num_work)]
        for each in self.work_rely:
            loc1 = ord(each[0]) - ord('A')
            loc2 = ord(each[1]) - ord('A')
            matrix[loc1][loc2] = 1
        return matrix

    def get_first_allow(self):
        allow = self.work[:]
        for each in self.work_rely:
            if each[1] in allow:
                allow.remove(each[1])
        return allow

    def get_si(self):
        sum = 0
        times = []
        for i in range(self.num_workbench):
            time = 0
            for j in self.order[i]:
                time += self.works[j]
            times.append(time)
        for i in range(self.num_workbench):
            sum += (self.ct-times[i])*(self.ct-times[i])
        sum /= self.num_workbench
        si = math.sqrt(sum)
        return si

    def get_init_order(self):
        self.order = []
        self.allow = self.get_first_allow()

        self.tabu = []
        flag = [0 for i in range(self.num_work)]#每一位的值表示节点的入度
        for i in range(self.num_work):
            for j in range(self.num_work):
                flag[i] += self.matrix[j][i]
        #print(flag)

        #为num_workbench-1个工作站分配任务
        for i in range(self.num_workbench-1):
            sub_order = []
            time = 0
            while time <= self.cm*1.1 and self.allow:
                #print(self.allow)
                #print(self.tabu)
                #print()
                selected = random.choice(self.allow)
                sub_order.append(selected)
                loc = ord(selected)-ord('A')
                self.allow.remove(selected)
                self.tabu.append(selected)
                # 更新节点入度
                if selected in list(self.succeed.keys()):
                    for su in self.succeed[selected]:
                        loc = ord(su) - ord('A')
                        flag[loc] -= 1
                time += self.works[selected]
                #print(flag)
                #print(selected)
                #print(time)
                #更新allow列表
                for j in range(self.num_work):
                    if flag[j] == 0:
                        #print(self.work[j])
                        if self.work[j] not in self.tabu:
                            if self.work[j] not in self.allow:
                                self.allow.append(self.work[j])
            self.order.append(sub_order)
        #为最后一个工作站分配任务
        sub_order = []
        for each in self.work:
            if each not in self.tabu:
                sub_order.append(each)
                self.tabu.append(each)

        self.order.append(sub_order)
        #print(self.order)
        self.si = self.get_si()
        #print(self.si)

    # 生成后继列表
    def get_succeed(self):
        succeed = {}
        for each in self.work_rely:
            if each[0] in list(succeed.keys()):
                succeed[each[0]].append(each[1])
            else:
                succeed[each[0]] = []
                succeed[each[0]].append((each[1]))
        return succeed

    # 轮盘赌选择
    def rand_choose(self, p):
        x = np.random.rand()
        for k in range(len(p)):
            x -= p[k]
            if x <= 0:
                return k

    #执行一次搜索
    def search_order(self,phe,eta):
        self.order = []
        self.allow = self.get_first_allow()
        self.tabu = []

        # 每一位的值表示节点的入度
        flag = [0 for i in range(self.num_work)]
        for i in range(self.num_work):
            for j in range(self.num_work):
                flag[i] += self.matrix[j][i]
        #做初始选择
        selected = random.choice(self.allow)
        sub_order = []
        sub_order.append(selected)
        time = self.works[selected]
        self.allow.remove(selected)
        self.tabu.append(selected)
        #更新节点入度
        if selected in list(self.succeed.keys()):
            for su in self.succeed[selected]:
                loc = ord(su) - ord('A')
                flag[loc] -= 1
        # 更新allow列表
        for j in range(self.num_work):
            if flag[j] == 0:
                if self.work[j] not in self.tabu:
                    if self.work[j] not in self.allow:
                        self.allow.append(self.work[j])
        # 为num_workbench-1个工作站分配任务
        for i in range(self.num_workbench - 1):

            while time <= self.cm * 1.05 and self.allow:
                P = []
                #通过信息素计算转移概率
                for i in self.allow:
                    loc1 = ord(selected)-ord('A')
                    loc2 = ord(i)-ord('A')
                    P.append(phe[loc1][loc2] ** self.alpha * eta[loc1][loc2] ** self.beta)
                P_sum = sum(P)
                P = [x / P_sum for x in P]
                index = self.rand_choose(P)
                selected = self.allow[index]
                sub_order.append(selected)
                loc = ord(selected) - ord('A')
                self.allow.remove(selected)
                self.tabu.append(selected)
                # 更新节点入度
                if selected in list(self.succeed.keys()):
                    for su in self.succeed[selected]:
                        loc = ord(su) - ord('A')
                        flag[loc] -= 1
                time += self.works[selected]
                # 更新allow列表
                for j in range(self.num_work):
                    if flag[j] == 0:
                        #print(self.work[j])
                        if self.work[j] not in self.tabu:
                            if self.work[j] not in self.allow:
                                self.allow.append(self.work[j])
            self.order.append(sub_order)
            sub_order = []
            time = 0
        # 为最后一个工作站分配任务
        sub_order = []
        for each in self.work:
            if each not in self.tabu:
                sub_order.append(each)
                self.tabu.append(each)
        self.order.append(sub_order)
        self.si = self.get_si()
        print(self.si)


    #拓扑排序加快效率
    def get_sequence(self,phe,eta):
        flag = [1 for i in range(self.num_work)]
        for each in self.work_rely:
            loc = ord(each[1])-ord('A')
            flag[loc] = -1
        temp_flag = flag
        temp_matrix = copy.deepcopy(self.matrix)
        seq = []
        selected = self.work[0]
        for i in range(self.num_work):
            # print(temp_matrix)
            # 随机选一个入度为0的结点

            zero_list = []
            for j in range(self.num_work):
                if temp_flag[j] == 1:
                    zero_list.append(self.work[j])
            P = []
            # 通过信息素计算转移概率
            for k in zero_list:
                loc1 = ord(selected) - ord('A')
                loc2 = ord(k) - ord('A')
                P.append(phe[loc1][loc2] ** self.alpha * eta[loc1][loc2] ** self.beta)
            P_sum = sum(P)
            P = [x / P_sum for x in P]
            index = self.rand_choose(P)
            selected = zero_list[index]
            this = selected
            # print(this)
            seq.append(this)
            temp = ord(this) - ord('A')
            temp_flag[temp] = 0
            # 更新flag标志数组
            for k in range(self.num_work):
                if temp_matrix[temp][k] == 1:
                    temp_matrix[temp][k] = 0
                    if temp_flag[k] == -1:
                        s = 0
                        for m in range(self.num_work):
                            s += temp_matrix[m][k]
                        if s == 0:
                            temp_flag[k] = 1
        self.seq = seq
        return seq

    def get_order(self,seq):
        temp_seq = seq[:]
        temp_seq.reverse()
        order = []
        temp_work = temp_seq.pop()
        for i in range(self.num_workbench):
            # print(i)
            # print(temp_work)
            sub_order = []
            time = self.works[temp_work]
            sub_order.append(temp_work)
            temp_work = temp_seq.pop()
            while (time + self.works[temp_work] <= self.cm * 1.1):  # 只有这里和上边不一样
                # print(temp_work)
                time += self.works[temp_work]
                sub_order.append(temp_work)
                if (temp_seq):
                    temp_work = temp_seq.pop()
            order.append(sub_order)
        if (temp_work not in order[-1]):
            order[-1].append(temp_work)
        while (temp_seq):
            order[-1].append(temp_seq.pop())
        return order

    def search(self,phe,eta):
        seq = self.get_sequence(phe,eta)
        self.order = self.get_order(seq)
        self.si = self.get_si()




