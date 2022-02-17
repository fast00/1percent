from unittest import TestCase
from main2lib import *


class TestMarketInfo(TestCase):
    listresult = [[20220112, 79500, 79600, 78600, 78900, 11000502, 0.0, 0.51],
                  [20220113, 79300, 79300, 77900, 77900, 13889401, -1.27, 0.26]]

    # ["날짜", "시가", "고가", "저가", "오늘종가", "거래량", "오늘증가율", "다음날고가증가율"]
    def test_getstock_period_info(self):
        result = MarketInfo('A005930').GetstockPeriodInfo(3)
        print(result)
        self.failIf(result != TestMarketInfo.listresult)


class TestFileMethods(TestCase):
    codelist = ['A005930', 'A000660', 'A005935', 'A207940', 'A035420', 'A051910', 'A005380', 'A006400', 'A035720',
                'A000270', 'A005490', 'A105560', 'A096770', 'A012330', 'A066570', 'A068270', 'A323410', 'A028260',
                'A055550', 'A377300', 'A034730', 'A259960', 'A302440', 'A051900', 'A009150', 'A086790', 'A015760',
                'A032830', 'A003550', 'A036570', 'A011200', 'A017670', 'A352820', 'A018260', 'A316140', 'A033780',
                'A361610', 'A010950', 'A034020', 'A000810', 'A010130', 'A003670', 'A003490', 'A251270', 'A329180',
                'A011070', 'A090430', 'A034220', 'A402340', 'A030200', 'A024110', 'A009830', 'A011170', 'A326030',
                'A383220', 'A138040', 'A009540', 'A018880', 'A086280', 'A004020', 'A011790', 'A032640', 'A097950',
                'A069500', 'A088980', 'A000060', 'A006800', 'A035250', 'A021240', 'A011780', 'A020150', 'A137310',
                'A000720', 'A010140', 'A161390', 'A028050', 'A005830', 'A071050', 'A008560', 'A000100', 'A267250',
                'A271560', 'A241560', 'A003410', 'A139480', 'A180640', 'A016360', 'A005387', 'A000990', 'A307950',
                'A078930', 'A006360', 'A029780', 'A005940', 'A047810', 'A036460', 'A002790', 'A008930', 'A002380',
                'A272210', 'A371460', 'A010620', 'A128940', 'A007070', 'A008770', 'A004990', 'A014680', 'A026960',
                'A052690', 'A138930', 'A028670', 'A000120', 'A088350', 'A047050', 'A012750', 'A204320', 'A042660',
                'A336260', 'A012450', 'A039490', 'A112610', 'A030000', 'A285130', 'A336370', 'A051915', 'A282330',
                'A047040', 'A375500', 'A064350', 'A005385', 'A023530', 'A000880', 'A298050', 'A006280', 'A004170',
                'A001040', 'A001450', 'A093370', 'A298020', 'A010060', 'A252670', 'A278540', 'A000080', 'A102110',
                'A111770', 'A011210', 'A009240', 'A081660', 'A012510', 'A003090']
    kospicodelist = 150  # 리스트
    kospibasket = 720  # 리스트
    stockbasket = 150  # 코드 : 바스켓
    kospiremaindaylist = 279  # 리스트
    remaindaylist = 150  # 코드 : 바스켓

    def test_get_daylist2(self):
        result = FileMethods().GetDaylist('코스피150')
        kospicodelist1 = len(result[0])  # 리스트
        kospibasket1 = len(result[1])  # 리스트
        stockbasket1 = len(result[2])  # 코드 : 바스켓
        kospiremaindaylist1 = len(result[3])  # 리스트
        remaindaylist1 = len(result[4])  # 코드 : 바스켓
        self.failIf(TestFileMethods.kospicodelist != 150 and TestFileMethods.kospibasket != 720
                    and TestFileMethods.stockbasket != 150 and TestFileMethods.kospiremaindaylist != 279
                    and TestFileMethods.remaindaylist != 150)

    def test_day_list(self):
        pass

    def test_change_day_list(self):
        pass

    def test_get_list(self):
        result = FileMethods().GetList('코스피150')
        self.failIf(TestFileMethods.codelist != result)


class TestIndicators(TestCase):
    MA = [[20180102, 49848, 51020, 0.12, 3.02]]
    PPO = [[20180102, 102.351, 0.12, 3.02]]

    def test_make_mafrom_file(self):
        basket = [[20171222, 49400, 49960, 49240, 49700, 11199650, 1.14, 0.8],
                  [20171226, 49760, 50100, 48200, 48200, 16039850, -3.02, 2.82],
                  [20171227, 48960, 49560, 48460, 49360, 10743600, 2.41, 3.24],
                  [20171228, 49560, 50960, 49500, 50960, 8985450, 3.24, 0.86],
                  [20180102, 51380, 51400, 50780, 51020, 8474250, 0.12, 3.02]]
        result = Indicators().MakeMAFromFile(5, basket)
        self.failIf(TestIndicators.MA != result)

    def test_make_ppofrom_file(self):
        basket = [[20171222, 49400, 49960, 49240, 49700, 11199650, 1.14, 0.8],
                  [20171226, 49760, 50100, 48200, 48200, 16039850, -3.02, 2.82],
                  [20171227, 48960, 49560, 48460, 49360, 10743600, 2.41, 3.24],
                  [20171228, 49560, 50960, 49500, 50960, 8985450, 3.24, 0.86],
                  [20180102, 51380, 51400, 50780, 51020, 8474250, 0.12, 3.02]]
        result = Indicators().MakePPOFromFile(5, basket)
        self.failIf(TestIndicators.PPO != result)


class TestPPOMethod(TestCase):
    PPO = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
    PPO2 = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
    PPOrange = [2, 4]
    PPOrangecount = {2.0: 0, 2.1: 0, 2.2: 0, 2.3: 0, 2.4: 0, 2.5: 0, 2.6: 0, 2.7: 0, 2.8: 0, 2.9: 0, 3.0: 0, 3.1: 0,
                     3.2: 0, 3.3: 0, 3.4: 0, 3.5: 0, 3.6: 0, 3.7: 0, 3.8: 0, 3.9: 0, 4.0: 0}
    PPOrangePaticularcount = {2.0: 0, 2.1: 0, 2.2: 0, 2.3: 0, 2.4: 0, 2.5: 0, 2.6: 0, 2.7: 0, 2.8: 0, 2.9: 0, 3.0: 0,
                              3.1: 0, 3.2: 0, 3.3: 0, 3.4: 0, 3.5: 0, 3.6: 0, 3.7: 0, 3.8: 0, 3.9: 0, 4.0: 0}
    PPOrangePercent = {2.0: 0, 2.1: 0, 2.2: 0, 2.3: 0, 2.4: 0, 2.5: 0, 2.6: 0, 2.7: 0, 2.8: 0, 2.9: 0, 3.0: 0, 3.1: 0,
                       3.2: 0, 3.3: 0, 3.4: 0, 3.5: 0, 3.6: 0, 3.7: 0, 3.8: 0, 3.9: 0, 4.0: 0}
    daylist = {2.0: [], 2.1: [], 2.2: [], 2.3: [], 2.4: [], 2.5: [], 2.6: [], 2.7: [], 2.8: [], 2.9: [], 3.0: [],
               3.1: [], 3.2: [], 3.3: [], 3.4: [], 3.5: [], 3.6: [], 3.7: [], 3.8: [], 3.9: [], 4.0: []}
    PPOrangepercent = {2.0: 100.0, 2.1: 0, 2.2: 0, 2.3: 0, 2.4: 0, 2.5: 0, 2.6: 0, 2.7: 0, 2.8: 0, 2.9: 0, 3.0: 0.0,
                       3.1: 0, 3.2: 0, 3.3: 0, 3.4: 0, 3.5: 0, 3.6: 0, 3.7: 0, 3.8: 0, 3.9: 0, 4.0: 0.0}
    result_formarket = [2.0]
    PPOrangepercent2 = {2: 100.0, 3: 100.0, 4: 100.0}

    def test_sort_list(self):
        PPO = TestPPOMethod().PPO
        result = PPOMethod().SortList(PPO)
        self.failIf(TestPPOMethod.PPOrange != result)

    def test_dic_initialize(self):
        pass

    def test_dic_initialize_for_market(self):
        PPO = TestPPOMethod().PPO
        result = PPOMethod()
        result.DicInitialize_forMarket(PPO)
        if result.PPOrangecount != TestPPOMethod.PPOrangecount and \
                result.PPOrangePaticularcount != TestPPOMethod.PPOrangePaticularcount and \
                result.PPOrangePercent != TestPPOMethod.PPOrangePercent and \
                result.daylist != TestPPOMethod.daylist:
            self.fail()

    def test_condition_setting(self):
        PPO = TestPPOMethod().PPO
        result = PPOMethod().Condition_Setting(PPO, 4)
        self.failIf(TestPPOMethod().PPOrangepercent2 != result)

    def test_get_result(self):
        method = PPOMethod()
        PPO = TestPPOMethod().PPO2
        method.Condition_Setting(PPO, 4)
        result = method.Get_result()
        self.failIf(TestPPOMethod().result_formarket != result)

    def test_condition_setting_for_market(self):
        PPO = TestPPOMethod().PPO
        result = PPOMethod().Condition_Setting_forMarket(PPO, 4)
        self.failIf(TestPPOMethod().PPOrangepercent != result)

    def test_get_result_for_market(self):
        method = PPOMethod()
        PPO = TestPPOMethod().PPO2
        method.Condition_Setting_forMarket(PPO, 4)
        result = method.Get_result_forMarket()
        self.failIf(TestPPOMethod().result_formarket != result)


class TestTotalResult(TestCase):
    PPO = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
    totalresult = [2.0]

    def test_marketresult_from_file(self):
        PPO = TestTotalResult().PPO
        result = TotalResult().MARKETOverlapppoListFromFile(PPO, 4)
        self.failIf(TestTotalResult().totalresult != result)

    def test_stock_overlapppo_list_from_file(self):  # PPOrangePaticularcount를 5 이상으로 설정해야 맞음
        PPO = TestTotalResult().PPO
        result = TotalResult().StockOverlapppoListFromFile(PPO, 4)
        self.failIf(TestTotalResult().totalresult != result)


class TestCheckToday(TestCase):
    def test_check_today_stock_from_file(self):
        pass

    def test_check_today_market_from_file(self):
        pass


class TestAccount(TestCase):
    # money = money
    # stockcount = 0
    # stockmoney = 0

    def test_buy(self):
        account = Account(100000).buy(1000)
        print(account)
        self.failIf(account == 1)

    def test_sell(self):
        self.fail()
