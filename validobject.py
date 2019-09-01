def validcardobject(cardobject):
    if "name" in cardobject and "type" in cardobject and "limit" in cardobject and  "region" in cardobject:
        return True
    else:
        return False

def validloanobject(loanobject):
    if "type" in loanobject and "term" in loanobject and "l_limit" in loanobject and "u_limit" in loanobject and  "facility" in loanobject:
        return True
    else:
        return False
