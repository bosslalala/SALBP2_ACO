from ant import Ant
import copy
import math

#输入
#工序详情
works = {'A':45, 'B':11, 'C':9, 'D':50, 'E':15, 'F':12, 'G':12, 'H':12, 'I':12, 'J':8, 'K':9}
#工序名称
work = ['A','B','C','D','E','F','G','H','I','J','K']
#紧前关系
work_rely = [['A','B'],['B','C'],['C','F'],['C','G'],['F','J'],['G','J'],['D','E'],['E','H'],['E','I'],['H','J'],['I','J'],['J','K']]
num_work = 11#工序数
num_workbench = 4#工位数

#参数
num_ant = 50#蚂蚁的数量
best_ant = None

class Aco(object):

    #初始化
    def __init__(self,num_ant,num_work,num_workbench,work,works,work_rely):
        self.num_ant = num_ant
        self.num_work = num_work  # 工序数
        self.num_workbench = num_workbench  # 工位数
        self.works = works  # 工序详情
        self.work = work  # 工序列表
        self.work_rely = work_rely  # 紧前关系
        self.mc = 100 #最大迭代次数
        self.alpha = 1 #信息素因子
        self.beta = 5 #启发式函数因子
        self.rho = 0.1 #信息素挥发因子
        self.best_ant = None #最佳蚂蚁
        self.succeed = self.get_succeed()  # 获得后继列表
        self.pwi = self.get_pwi()  # 获得位置权重
        self.pheromone_matrix = self.init_pheromone()#信息素矩阵
        self.eta = self.init_eta() #启发式函数
        self.best_order = None
        self.min_si = 100

    #算法初始化
    def init_aco(self):
        #生成蚁群
        ants = []
        for i in range(self.num_ant):
            new_ant = Ant(i,self.num_work,self.num_workbench,self.work,self.works,self.work_rely)
            ants.append(new_ant)
        #开始迭代
        self.best_ant = copy.deepcopy(ants[0])
        for i in range(self.mc):
            #依次运行所有的蚂蚁
            for j in range(self.num_ant):
                ants[j].search(self.pheromone_matrix,self.eta)
            #保存最好结果
            best_ant = self.get_bestant(ants)
            if best_ant.si < self.best_ant.si:
                self.best_ant = copy.deepcopy(best_ant)
                self.best_order = best_ant.order[:]
                self.min_si = best_ant.si
            #print(best_ant.order)
            #print(best_ant.si)

            #更新信息素
            for k in range(self.num_work):
                for j in range(self.num_work):
                    self.pheromone_matrix[k][j] *= 0.5
            for j in range(self.num_work-1):
                loc1 = ord(best_ant.seq[j])-ord('A')
                loc2 = ord(best_ant.seq[j+1])-ord('A')
                self.pheromone_matrix[loc1][loc2] += 5/(self.num_work*self.num_workbench)
        print(str(self.mc)+"次迭代后：")
        #迭代结束，输出最佳解
        print("最佳排序")
        print(self.best_order)

        print("si:" +str(self.get_si(self.best_order)))

    #初始化信息素矩阵
    def init_pheromone(self):
        #初始信息素值为10/(num_work*num_workbench)
        phe0 = 10/(self.num_work*self.num_workbench)
        matrix = [[phe0 for i in range(self.num_work)] for j in range(self.num_work)]
        return matrix

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

    # 计算位置权重
    def get_pwi(self):
        pwi = []
        for each in self.work:
            pw = self.works[each]
            if pw in list(self.succeed.keys()):
                for i in self.succeed[each]:
                    pw += self.works[i]
            pw = pw/pw*10
            pwi.append(pw)
        return pwi

    #初始化启发式函数矩阵
    def init_eta(self):
        matrix = [[0.5 for i in range(self.num_work)] for j in range(self.num_work)]
        return matrix

    #保存最好的解
    def get_bestant(self, ant):
        min_si = 100
        index = 0
        for i in range(self.num_ant):
            if ant[i].si < min_si:
                min_si = ant[i].si
                index = i
        return ant[index]

    # 计算si
    def get_si(self,order):
        times = []
        for i in range(num_workbench):
            time = 0
            for j in order[i]:
                time += works[j]
            times.append(time)
        print(times)
        times.sort()
        ct = times[num_workbench - 1]
        print("节拍："+str(ct))
        s = 0
        for i in range(num_workbench):
            s += (ct - times[i]) * (ct - times[i])
        s = s / num_workbench
        si = math.sqrt(s)
        return si

aco = Aco(num_ant,num_work,num_workbench,work,works,work_rely)
aco.init_aco()
