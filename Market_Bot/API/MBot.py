class MBOT:
    def __init__(self, buyBehaviors=None, sellBehaviors=None):
        # initialize constructors
        self.BuyBehaviors = buyBehaviors
        self.SellBehaviors = sellBehaviors

    def run(self, token, asset, cycles=1):
        # run the bot (cycles) times
        if(self.BuyBehaviors.get_result()):
            # execute market buy
            pass
        elif(self.SellBehaviors.get_result()):
            # execute market sell
            pass
        pass

    def test_run(self, input_array, token, asset):
        exchange_fee = 0.001
        risk_coeff = 50/100

        funds = input_array[0]
        funds_list = [funds]
        tokens = 0
        tokens_list = [(funds+tokens*input_array[0])]
        value_list = [(funds, True)]

        exchange_price = []

        buy_val = 0
        sell_val = 0

        good_exchange_counter = 0
        bad_exchange_counter = 0

        self.BuyBehaviors.set_data(input_array)
        self.SellBehaviors.set_data(input_array)

        for x in range(1, len(input_array)):
            current_price = input_array[x]

            fund_check = int(funds*risk_coeff*100)/100
            token_sell = int(tokens*risk_coeff*100)/100

            token_buy = int((funds/current_price)*risk_coeff*100)/100
            value_check = int(risk_coeff*current_price*tokens*100)/100

            if((self.BuyBehaviors.get_result(x, current_price)) and (fund_check > 10)):
                # execute market buy
                buybool = True
                tokens = tokens + (1-exchange_fee)*token_buy
                funds = funds - current_price*token_buy
            elif((self.SellBehaviors.get_result(x, current_price)) and (value_check > 10)):
                # execute market sell
                buybool = False
                funds = funds + (1-exchange_fee)*current_price*token_sell
                tokens = tokens - risk_coeff*tokens
            else:
                funds_list.append(funds)
                tokens_list.append(tokens)
            if((funds+tokens*current_price)/value_list[x-1][0] == 1):
                value_list.append((funds+tokens*current_price, True))
            else:
                value_list.append((funds+tokens*current_price, False))
        return [[x[0] for x in value_list], input_array]

    def getBuyBehaviors(self):
        # get bot buy behaviors list
        return self.BuyBehaviors

    def setBuyBehaviors(self, buyBehaviors):
        # set bot buy behaviors list
        self.BuyBehaviors = buyBehaviors

    def getSellBehaviors(self):
        # get bot sell behaviors list
        return self.SellBehaviors

    def setSellBehaviors(self, sellBehaviors):
        # set bot sell behaviors list
        self.SellBehaviors = sellBehaviors
