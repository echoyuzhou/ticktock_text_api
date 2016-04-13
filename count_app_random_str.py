import readall
rating_logs = readall.readall("/home/ubuntu/zhou/Backend/rating_log/v4")
writelist = readall.get_log(rating_logs)
strategy_scan = ['init','end','more','switch','joke']
table_strategy_app = [0,0,0]
table = {'init':[0,0,0],'end':[0,0,0],'more':[0,0,0],'switch':[0,0,0],'joke':[0,0,0]}
for rate in rating_logs:
    for tmpdict in writelist:
        stra =[]
        #print tmpdict
        strategy = tmpdict["strategy"]
        for stra in strategy_scan:
            if stra in strategy:
                strategy_real = stra
        if strategy_scan[0] in strategy or strategy_scan[1] in strategy or strategy_scan[2] in strategy or strategy_scan[3] in strategy or strategy_scan[4] in strategy:
                #print strategy
                print tmpdict["strategy"]
                index = int(tmpdict["app_value"])-1
                table_strategy_app[index] = table_strategy_app[index] +1
                table[strategy_real][index] = table[strategy_real][index] +1
print table_strategy_app
print table

