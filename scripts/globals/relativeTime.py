from datetime import datetime,timedelta
def relative2(compare:datetime):
    """
    Python function using the `maya` library to get relative time.

    Arguments:
    * datetime object `compare` - The time with which you wish to get relative time to.

    Outputs a string in the following format: `x unit(s) ago` or `in x unit(s)`, with `x` representing a number and unit representing the unit of time.
    """
    import maya
    now = datetime.now()
    silly = maya.relativedelta(now,compare)
    def formatn(n,s):
        if n == 1:
            return '1 %s' % s
        else: # the original gist has `n>1` here, but idk if that's *really* necessary.
            return '%d %ss' % (n,s)
    for thing in ['year','month','week','day','hour','minute','second']:
        sex:int=getattr(silly,thing+'s')
        if sex:
            if sex>0:
                return '{0} ago'.format(formatn(sex,thing))
            elif sex<0:
                return 'in {0}'.format(formatn(-sex,thing))
        else:
            continue