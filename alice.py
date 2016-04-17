import commands

#commands.getstatusoutput("rm c.txt")
def alice(response):
# Here write the Alice response, send in response, get out line.
        cmd = '''curl -b c.txt -c c.txt -e sheepridge.pandorabots.com --data "input=hello" 'http://sheepridge.pandorabots.com/pandora/talk?botid=b69b8d517e345aba&skin=custom_input' 2>/dev/null | tail -n 1 '''.replace('hello',response)
        output_all = commands.getstatusoutput(cmd)
        output = output_all[1]
        print output
        sentence = output.split('<br>')
        print 'sentence'
        print sentence
        line = sentence[-1][10:]
        print 'line'
        print line
        return line

