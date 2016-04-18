def space_eliminate(output):
    punc_list = [".",",","?","'","!"]
    for punc in punc_list:
            if punc in output:
                output = output.replace(' '+punc,punc)
    return output
