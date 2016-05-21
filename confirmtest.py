def confirm(prompt=None, resp=False):
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s|%s]: ' % (prompt, 'y ', ' n')
    else:
        prompt = '%s [%s|%s]: ' % (prompt, 'n ', ' y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

confirm(prompt="Make player?")
#print confirm(prompt="Make player?")


if(confirm(prompt="Make player?")): 
    print "Relative success."
