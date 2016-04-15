import commands

def get_sentiment(response):
    response_processed= response.replace('"','')
    print response_processed
    cmd = '''curl -d "text=great" http://text-processing.com/api/sentiment/'''.replace('great', response_processed)
    output_all = commands.getstatusoutput(cmd)
    output = output_all[1]
    value = output.split(':')
    label = value[-1]
    return label[2:-2]
'''
label = get_sentiment(' the rose is red')
print label
'''
