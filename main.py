import json

with open('operators_info.json', 'r', encoding='utf-8') as ops_data_file:
    ops_data = json.load(ops_data_file)

for i in range(10):
    print(list(ops_data.keys())[i])


class Infrastructure:
    def __init__(self):
        self.codename = 'codename'


class DayTotal:
    total_production = 0


# 以设施为单位进行计算

# 以贸易站为例
class Facility:
    renjianyanhuo = 0
    siweilianhuan = 0

    def __init__(self):
        # 干员，精英等级，心情，工作时长，前任干员，心情消耗，技能名称
        self.pit = [['n', 0, 0, 0, 'n', 0, 'n'], ['x', 0, 0, 0, 'n', 0, 'n'], ['x', 0, 0, 0, 'n', 0, 'n']]

        self.type = 'none'
        self.lvl = 1


class TradeStation(Facility):
    # 全局变量
    totalNum = 0

    # 产能输出
    total_LMD = 0
    total_originium = 0

    # 消耗
    puregold = 0
    yuanshisuipian = 0

    def __init__(self):
        super().__init__()
        TradeStation.totalNum += 1

        # 干员判定区
        self.char_Lappland = 0
        self.char_Texas = 0
        self.char_Exusiai = 0


        # 阵营判定区
        self.camp_SeaHunter = 0
        self.camp_RainbowSix = 0
        self.camp_qiewuliu = 0

        # 基础信息
        # self.category = 'trade'
        # self.product = 'LMD'
        self.initEfficiency = 1
        self.initOrderPrefer = 0
        # self.consumption = 'puregold'
        # self.consumptionEfficiency = 0
        self.level = 3
        # self.moodConsumption = 1
        self.orderLimit = 6
        self.workerNum = 0

        # 坑位区
        self.operator_1 = 'none'
        self.operator_1_mood = 0

    def operator_load(self, operator, elite, position, mood=24):
        self.pit[position][4] = self.pit[position][0]
        self.pit[position][0] = operator
        self.pit[position][1] = elite
        self.pit[position][2] = mood
        # 重置工作时长
        if self.pit[position][4] != self.pit[position][0]:
            self.pit[position][3] = 0
        self.pit[position][5] = 1

    # 效率计算
    def cal_efficiency(self):
        # 设施初始化
        self.efficiency = self.initEfficiency
        self.orderPrefer = self.initOrderPrefer

        for i in range(3):
            # 干员状态初始化
            self.pit[i][5] = 1

        for i in range(3):

            # 拉普兰德
            if self.pit[i][0] == 'Lappland':
                self.pit[i][6] = '醉翁之意·α'
                if 'Texas' in self.pit[0][0] or 'Texas' in self.pit[1][0] or 'Texas' in self.pit[2][0]:
                    self.pit[i][5] -= 0.1
                    self.orderLimit += 2
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '醉翁之意·β'
                    if 'Texas' in self.pit[0][0] or 'Texas' in self.pit[1][0] or 'Texas' in self.pit[2][0]:
                        self.pit[i][5] = 0.8
                        self.orderLimit -= 4

            # 德克萨斯
            if self.pit[i][0] == 'Texas':
                self.pit[i][6] = '恩怨'
                if 'Lappland' in self.pit[0][0] or 'Lappland' in self.pit[1][0] or 'Lappland' in self.pit[2][0]:
                    self.pit[i][5] += 0.3
                    self.efficiency += 0.65
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '恩怨 默契'
                    if 'Exusiai' in self.pit[0][0] or 'Exusiai' in self.pit[1][0] or 'Exusiai' in self.pit[2][0]:
                        self.pit[i][5] -= 0.3

            # 巫恋
            if self.pit[i][0] == 'Shamare':
                self.pit[i][6] = '裁缝·α'
                self.orderPrefer += 1
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '裁缝·α 低语'
                    self.efficiency = 0.45 * self.workerNum - 0.45
                    for j in range(3):
                        self.pit[j][5] += 0.25

            # 能天使
            if self.pit[i][0] == 'Exusiai':
                self.pit[i][6] = '企鹅物流·α'
                self.efficiency += 0.20
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '物流专家'
                    self.efficiency += 0.15

    def show_station_info(self):
        for i in range(3):
            print('干员' + self.pit[i][0] + str(self.pit[i][6]))

        print('总效率' + str(self.efficiency))


    def cal_moodConsumption(self):
        pass


class Position:
    def __init__(self, operator, mood):
        self.operator = 'none'
        self.mood = 24


class operator:
    def __init__(self):
        self.name = 'name'


class room:
    def __init__(self, type, level):
        self.type = 'none'
        self.level = 1


def print_hi(name):
    print(f'Hi, {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


print(ops_data['char_4077_palico']['name'])

trade1 = TradeStation()
f1 = Facility()

print (trade1.pit)

trade1.operator_load('Texas', 2, 0)
trade1.operator_load('Lappland', 2, 1)
trade1.operator_load('Exusiai', 2, 2)

trade1.cal_efficiency()
trade1.show_station_info()