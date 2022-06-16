from module.huodong.base_huodong import BaseHuoDong


class ChenYingYuYin(BaseHuoDong):
    @property
    def huodong_name(self):
        return "chenyingyuyin"

    @property
    def huodong_click(self):
        return 1099, 558, 1150, 570

    @property
    def huodongmain(self):
        return 1063, 547, 1089, 580, "夕"

    @property
    def enter_huodong(self):
        return self.enter_huodong_template["center_one"]

    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)


if __name__ == '__main__':
    task = ChenYingYuYin(1, "LE-5")
    task.cycleFight()
