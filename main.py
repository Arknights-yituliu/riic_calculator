import json

#加载基建布局方案
with open('plan_243.json', 'r', encoding='utf-8') as riic_plan:
    riic_plan_data = json.load(riic_plan)
#加载排班方案
with open('schedule_243_a.json', 'r', encoding='utf-8') as operator_plan:
    operator_plan_data = json.load(operator_plan)

# 导入一份干员基本信息以备不时之需
with open('operators_info.json', 'r', encoding='utf-8') as ops_data_file:
    ops_data = json.load(ops_data_file)

# 输出测试信息
for i in range(10):
    print(list(ops_data.keys())[i])


class Infrastructure:
    def __init__(self):
        self.codename = 'codename'


class DayTotal:
    total_production = 0


# 以设施为单位进行计算
class Facility:
    # 组合计算
    combo_MengJing = 0
    combo_JiYiSuiPian = 0
    combo_XiaoJie = 0
    combo_GanZhiXinXi = 0
    combo_RenJianYanHuo = 0
    combo_SiWeiLianHuan = 0
    combo_WuShengGongMing = 0
    combo_WuShuJieJing = 0

    combo_QingBaoChuBei = 0
    combo_WuSaSiTeYin = 0

    combo_MuTianLiao = 0

    # 站点
    num_TradeStation = 0
    num_Factory = 0


    def __init__(self):
        # 干员，精英等级，心情，工作时长，前任干员，心情消耗，技能名称
        self.pit = [['n', 0, 0, 0, 'n', 0, 'n'], ['x', 0, 0, 0, 'n', 0, 'n'], ['x', 0, 0, 0, 'n', 0, 'n']]

        self.type = 'none'
        self.lvl = 1

    # 干员进驻
    def operator_load(self, operator, elite, position, mood=24):
        self.pit[position][4] = self.pit[position][0]
        self.pit[position][0] = operator
        self.pit[position][1] = elite
        self.pit[position][2] = mood
        # 换干员则重置工作时长
        if self.pit[position][4] != self.pit[position][0]:
            self.pit[position][3] = 0
        self.pit[position][5] = 1


# 以贸易站为例
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
        Facility.num_TradeStation += 1

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




    # 预先计算组合
    # def cal_combo(self):
    #     for i in range(3):
    #         # 铎铃
    #         if self.pit[i][0] == 'Wind Chimes':
    #             self.pit[i][6] = '跋山涉水'
    #
    #
    #             if 'Texas' in self.pit[0][0] or 'Texas' in self.pit[1][0] or 'Texas' in self.pit[2][0]:
    #                 self.pit[i][5] -= 0.1
    #                 self.orderLimit += 2
    #             # 精二
    #             if self.pit[i][1] == 2:
    #                 self.pit[i][6] = '醉翁之意·β'
    #                 if 'Texas' in self.pit[0][0] or 'Texas' in self.pit[1][0] or 'Texas' in self.pit[2][0]:
    #                     self.pit[i][5] = 0.8
    #                     self.orderLimit -= 4
    #             continue


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
                continue

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
                continue

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
                continue

            # 能天使
            if self.pit[i][0] == 'Exusiai':
                self.pit[i][6] = '企鹅物流·α'
                self.efficiency += 0.20
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '物流专家'
                    self.efficiency += 0.15
                continue

            # 海蒂
            if self.pit[i][0] == 'Heidi':
                self.pit[i][6] = '订单分发·α'
                self.efficiency += 0.20
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '名流欢会'
                    self.efficiency += 0.15
                continue

            # 雪雉
            if self.pit[i][0] == 'Snowsant':
                self.pit[i][6] = '天道酬勤·α'
                self.efficiency += 0.25
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '天道酬勤·β'
                    self.efficiency += 0.1
                continue

            # 谷米
            if self.pit[i][0] == 'Gumi':
                self.pit[i][6] = '交际'
                self.efficiency += 0.3
                self.pit[i][5] -= 0.25
                continue
            # 月见夜
            if self.pit[i][0] == 'Midnight':
                self.pit[i][6] = '交际'
                self.efficiency += 0.3
                self.pit[i][5] -= 0.25
                continue
            # 空爆
            if self.pit[i][0] == 'Catapult':
                self.pit[i][6] = '交际'
                self.efficiency += 0.3
                self.pit[i][5] -= 0.25
                continue

            # 火哨
            if self.pit[i][0] == 'Firewhistle':
                self.pit[i][6] = '暖场'
                for j in range(3):
                    self.pit[j][5] -= 0.1
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '暖场 代为说项'
                    self.efficiency += 0.15 * self.workerNum - 0.15
                continue

            # 铎铃
            if self.pit[i][0] == 'Wind Chimes':
                self.pit[i][6] = '跋山涉水'
                for j in range(3):
                    self.pit[j][5] -= (0.1 + 0.01 * Facility.combo_RenJianYanHuo)
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '万里传书'
                    for j in range(3):
                        self.pit[j][5] -= 0.01 * Facility.combo_RenJianYanHuo
                continue

            # 可颂
            if self.pit[i][0] == 'Croissant':
                self.pit[i][6] = '企鹅物流·α'
                self.efficiency += 0.20
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '使命必达'
                    self.efficiency += 0.1
                    self.orderLimit += 1
                continue

            # 拜松
            if self.pit[i][0] == 'Bison':
                self.pit[i][6] = '峯驰物流'
                self.efficiency += 0.20
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '少当家'
                    self.efficiency += 0.1
                    self.orderLimit += 1
                continue

            # 空
            if self.pit[i][0] == 'Sora':
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '企鹅物流·β'
                    self.efficiency += 0.3
                continue

            # 夜刀、夜烟、安比尔、慕斯、缠丸、芬
            if self.pit[i][0] == 'Yato':
                self.pit[i][6] = '订单分发·β'
                self.efficiency += 0.3
                continue
            if self.pit[i][0] == 'Haze':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单分发·β'
                    self.efficiency += 0.3
                continue
            if self.pit[i][0] == 'Ambriel':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单分发·β'
                    self.efficiency += 0.3
                continue
            if self.pit[i][0] == 'Muse':
                self.pit[i][6] = '订单分发·β'
                self.efficiency += 0.3
                continue
            if self.pit[i][0] == 'Matoimaru':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单分发·β'
                    self.efficiency += 0.3
                continue
            if self.pit[i][0] == 'Fang':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单分发·β'
                    self.efficiency += 0.3
                continue

            # 梓兰、玫兰莎、远山
            if self.pit[i][0] == 'Orchid':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '供应管理'
                    self.efficiency += 0.25
                    self.orderLimit += 1
                continue
            if self.pit[i][0] == 'Melantha':
                self.pit[i][6] = '供应管理'
                self.efficiency += 0.25
                self.orderLimit += 1
                continue
            if self.pit[i][0] == 'Gitano':
                self.pit[i][6] = '供应管理'
                self.efficiency += 0.25
                self.orderLimit += 1
                continue

            # 银灰
            if self.pit[i][0] == 'SliverAsh':
                self.pit[i][6] = '喀兰贸易·α'
                self.efficiency += 0.15
                self.orderLimit += 2
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '喀兰之主'
                    self.efficiency += 0.05
                    self.orderLimit += 2
                continue

            # 安德切尔、深海色、蛇屠箱、香草
            if self.pit[i][0] == 'Adnachiel':
                self.pit[i][6] = '订单分发·α'
                self.efficiency += 0.20
                continue
            if self.pit[i][0] == 'Deepcolor':
                self.pit[i][6] = '订单分发·α'
                self.efficiency += 0.20
                continue
            if self.pit[i][0] == 'Cuora':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单分发·α'
                    self.efficiency += 0.20
                continue
            if self.pit[i][0] == 'Vanilla':
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单分发·α'
                    self.efficiency += 0.20
                continue

            # 崖心
            if self.pit[i][0] == 'Cliffheart':
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '喀兰贸易·β'
                    self.efficiency += 0.15
                    self.orderLimit += 4
                continue

            # 角峰、讯使
            if self.pit[i][0] == 'Matterhorn':
                self.pit[i][6] = '喀兰贸易·α'
                self.efficiency += 0.15
                self.orderLimit += 2
                continue
            if self.pit[i][0] == 'Courier':
                self.pit[i][6] = '喀兰贸易·α'
                self.efficiency += 0.15
                self.orderLimit += 2
                continue

            # 尤里卡
            if self.pit[i][0] == 'U-Official':
                self.pit[i][6] = '天真的谈判者'
                self.efficiency += 0.1
                self.orderPrefer = 0
                continue

            # 四月
            if self.pit[i][0] == 'April':
                self.pit[i][6] = '订单管理·α'
                self.efficiency += 0.1
                self.orderLimit += 2
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '订单管理·β'
                    self.orderLimit += 2
                continue

            # 翎羽
            if self.pit[i][0] == 'Plume':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单管理·α'
                    self.efficiency += 0.1
                    self.orderLimit += 2
                continue

            # 黑角
            if self.pit[i][0] == 'Noir Corne':
                # 精一，这个比较特殊
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '订单管理·α'
                    self.efficiency += 0.1
                    self.orderLimit += 2
                continue

            # 泰拉大陆调查团
            if self.pit[i][0] == 'Terra Research Commission':
                self.pit[i][6] = '可爱的艾露猫'
                self.efficiency += 0.05 + Facility.combo_MuTianLiao * 0.03
                self.orderLimit += 2
                continue

            # 石英
            if self.pit[i][0] == 'Quartz':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '精准排期'
                    self.efficiency += 0.3
                    # 后人的智慧
                continue

            # 鸿雪
            # 图耶
            # 伺夜
            # 凄凉
            # 孑
            # 空弦
            # 黑键
            # 乌有
            # 明椒
            # 柏喙
            # 卡夫卡
            # 但书
            # 贝娜
            # 龙舌兰
            # 史都华德
            # 暗索
            # 桃金娘


    # 信息输出
    def show_station_info(self):
        for i in range(3):
            print('干员' + self.pit[i][0] + str(self.pit[i][6]))

        print('总效率' + str(self.efficiency))

    # 心情验算，这些以后再说
    def cal_moodConsumption(self):
        pass


class Factory(Facility):
    def __init__(self):
        super().__init__()
        Facility.num_Factory += 1

        # 阵营判定区
        self.camp_SeaHunter = 0
        self.camp_RainbowSix = 0
        self.camp_qiewuliu = 0

        # 基础信息
        # self.category = 'trade'
        self.product_EXP = 1
        self.product_Puregold = 1
        self.initEfficiency = 1
        # self.initOrderPrefer = 0
        # self.consumption = 'puregold'
        # self.consumptionEfficiency = 0
        self.level = 3
        # self.moodConsumption = 1
        self.stockpile = 100
        self.workerNum = 0

    def cal_efficiency(self):
        # 设施初始化
        self.product_EXP = self.initEfficiency
        self.product_Puregold = self.initEfficiency

        for i in range(3):
            # 干员状态初始化
            self.pit[i][5] = 1

        for i in range(3):
            # 截云

            # 断罪者
            if self.pit[i][0] == 'Confiction':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '拳术指导录像'
                    self.product_EXP += 0.35
                continue

            # 食铁兽
            if self.pit[i][0] == 'Feater':
                self.pit[i][6] = '作战指导录像'
                self.product_EXP += 0.3
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '拳术指导录像'
                    self.product_EXP += 0.05
                continue

            # C3
            if self.pit[i][0] == 'Castle-3':
                # 精一 特殊
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '作战指导录像'
                    self.product_EXP += 0.3
                continue
            # 白雪
            if self.pit[i][0] == 'ShiraYuki':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '作战指导录像'
                    self.product_EXP += 0.3
                continue
            # 霜叶
            if self.pit[i][0] == 'FrostLeaf':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '作战指导录像'
                    self.product_EXP += 0.3
                continue
            # 红豆
            if self.pit[i][0] == 'Vigna':
                self.pit[i][6] = '作战指导录像'
                self.product_EXP += 0.3
                continue

            # 帕拉斯
            if self.pit[i][0] == 'Pallas':
                self.pit[i][6] = '智慧之境'
                self.stockpile += 8
                self.pit[i][5] -= 0.25
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '胜利之计'
                    self.product_EXP += 0.25
                continue

            #截云

            #至简

            #砾
            if self.pit[i][0] == 'Gravel':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '金属工艺·β'
                    self.product_Puregold += 0.35
                continue

            #夜烟
            if self.pit[i][0] == 'Haze':
                self.pit[i][6] = '金属工艺·α'
                self.product_Puregold += 0.3
                continue
            #斑点
            if self.pit[i][0] == 'Spot':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '金属工艺·α'
                    self.product_Puregold += 0.3
                continue

            #清流
            if self.pit[i][0] == 'Purestream':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '再生能源'
                    self.product_Puregold += 0.2 * Facility.num_TradeStation
                continue

            #迷迭香

            #槐琥
            #梅尔
            if self.pit[i][0] == 'Mayer':
                # 精二
                if self.pit[i][1] == 2:
                    self.pit[i][6] = '咪波·制造型'
                    self.product_EXP += 0.3
                    self.product_Puregold += 0.3
                continue

            # 灰豪
            # 远牙
            # 野鬃

            # 多萝西
            # 星源
            # 白面鸮
            # 赫默

            # 调香师
            if self.pit[i][0] == 'Perfumer':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '标准化·β'
                    self.product_EXP += 0.25
                    self.product_Puregold += 0.25
                continue

            # 史都华德
            if self.pit[i][0] == 'Steward':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '标准化·β'
                    self.product_EXP += 0.25
                    self.product_Puregold += 0.25
                continue

            # 罗比菈塔
            if self.pit[i][0] == 'Roberta':
                # 精一
                if self.pit[i][1] == 1:
                    self.pit[i][6] = '标准化·β'
                    self.product_EXP += 0.25
                    self.product_Puregold += 0.25
                continue


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
                continue



def print_hi(name):
    print(f'Hi, {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


print(ops_data['char_4077_palico']['name'])

trade1 = TradeStation()
f1 = Facility()

print (trade1.pit)


# riic = []
#
# def riic_init():
#     for room in riic_plan_data:
#         if room["type"] == "trade":
#             trade = TradeStation()
#             riic.append(trade)
#         if room["type"] == "factory":
#             factory = Factory()
#             riic.append(factory)
#     for room in riic:
#         print(room.pit)
#
# def riic_load():
#     for room in riic:
#         room.operator_load
#         print(room)
#     pass

trade_0 = TradeStation()
trade_1 = TradeStation()
trade_2 = TradeStation()
trade_3 = TradeStation()
trade_4 = TradeStation()
factory_0 = Factory()
factory_1 = Factory()
factory_2 = Factory()
factory_3 = Factory()
factory_4 = Factory()


def riic_load():
    trade_0.operator_load(operator_plan_data["trade"][1]["operator_list"][0]["name"], 2, 0)
    trade_0.operator_load(operator_plan_data["trade"][1]["operator_list"][1]["name"], 2, 1)
    trade_0.operator_load(operator_plan_data["trade"][1]["operator_list"][2]["name"], 2, 2)
    trade_0.cal_efficiency()
    trade_0.show_station_info()

trade1.operator_load('Texas', 2, 0)
trade1.operator_load('Lappland', 2, 1)
trade1.operator_load('Exusiai', 2, 2)

trade1.cal_efficiency()
trade1.show_station_info()

trade1.cal_efficiency()
trade1.show_station_info()

print(operator_plan_data["trade"][0]["operator_list"][0]["name"])

print('------')
# riic_init()
print('------')

riic_load()