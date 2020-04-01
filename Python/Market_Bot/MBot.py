class MBOT:
    def __init__(self, buyBehaviors = None, sellBehaviors = None):
        #initialize constructors
        self.BuyBehaviors = buyBehaviors
        self.SellBehaviors = sellBehaviors

    def run(self, token, asset, cycles = 1):
        #run the bot (cycles) times
        if(self.BuyBehaviors.get_result()):
            #execute market buy
            pass
        elif(self.SellBehaviors.get_result()):
            #execute market sell
            pass
        pass

    def test_run(self, token, asset, cycles = 1):
        #run the bot (cycles) times
        if(self.BuyBehaviors.get_result()):
            #execute market buy
            pass
        elif(self.SellBehaviors.get_result()):
            #execute market sell
            pass
        pass    
    
    def getBuyBehaviors(self):
        #get bot buy behaviors list
        return self.BuyBehaviors 

    def setBuyBehaviors(self, buyBehaviors):
        #set bot buy behaviors list
        self.BuyBehaviors = buyBehaviors

    def getSellBehaviors(self):
        #get bot sell behaviors list
        return self.SellBehaviors

    def setSellBehaviors(self, sellBehaviors):
        #set bot sell behaviors list
        self.SellBehaviors = sellBehaviors