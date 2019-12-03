class Trade:
    def __init__(self, ori=None):
        if (ori is None):
            self.non_copy_constructor()
        else:
            self.copy_constructor(ori)

    def non_copy_constructor(self):
        self.uuid_ = 0
        self.entryPrice_ = 0
        self.exitPrice_ = 0
        self.stoplessPrice_ = 0
        self.profitPrice_ = 0
        self.commissionrate_ = 0
        self.commission_ = 0
        self.coinNum_ = 1
        self.position_ = 0
        self.direction_ = "non-direction"
        self.entryTimeStamp_ = 0
        self.exitTimeStamp_ = 0

    def copy_constructor(self, ori):
        self.uuid_ = ori.uuid_
        self.entryPrice_ = ori.entryPrice_
        self.exitPrice_ = ori.exitPrice_
        self.stoplessPrice_ = ori.stoplessPrice_
        self.profitPrice_ = ori.profitPrice_
        self.commissionrate_ = ori.commissionrate_
        self.commission_ = ori.commission_
        self.coinNum_ = ori.coinNum_
        self.position_ = ori.position_
        self.direction_ = ori.direction_
        self.entryTimeStamp_ = ori.entryTimeStamp_
        self.exitTimeStamp_ = ori.exitTimeStamp_
