#!/usr/bin/etc python

import galbackend_cnn
#target = galbackend.GalInterface()
#print(target)
#gt = galbackend.Thread(target=galbackend.GalInterface)
galbackend_cnn.InitLogging()
galbackend_cnn.InitResource()
#while(1):
    #galbackend.LaunchQueryDebug('can you say that again')
while True:
    print(galbackend_cnn.get_response('how are you doing today'))

print(galbackend_cnn.get_response('i hate being cute lala'))
print(galbackend_cnn.get_response('i hate being cute lala'))
print(galbackend_cnn.get_response('i love movies'))
