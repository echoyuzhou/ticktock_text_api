#!/usr/bin/etc python

##Zhou: Use it to get the similar answer and the related question
if __name__ == "__main__":
    import galbackend
    import json
    #target = galbackend.GalInterface()
    #print(target)
    #gt = galbackend.Thread(target=galbackend.GalInterface)
    galbackend.InitLogging()
    galbackend.InitResource()
    #galbackend.LaunchQueryDebug('i love movies')
    #print(galbackend.get_response('i hate being cute lala'))
    #print(galbackend.get_response('i hate being cute lala'))
    #print(galbackend.get_response('i love movies'))
    with open('final-eval-batch.json') as json_data:
        data = json.load(json_data)
        json_data.close()

    for question in data:
        print(galbackend.get_response(question['question']))