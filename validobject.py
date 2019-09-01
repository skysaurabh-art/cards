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

def validclientobject(clientobject):
    if "client_name" in clientobject and "client_acct_no" in clientobject  and "branch_id" in clientobject and "curr_clos_bal" in clientobject and "cred_hist_len" in clientobject and "has_card" in clientobject and "has_acct" in clientobject: 
        return True
    else:
        return False
