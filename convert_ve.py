f= open('user_input_v2_out.txt')
lines = f.readlines()
for line in lines:
    line.find('oov')
    prev = line
    print

