reg_flag = False
reg_ind = 0
login_id = ""


def regis_chek(flag=False, ind=0, login=""):
    if flag is True:
        global reg_flag, reg_ind, login_id
        reg_flag = True
        reg_ind = ind
        login_id = login
    return
