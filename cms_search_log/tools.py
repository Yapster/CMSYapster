
def get_params(s_params):
    l = s_params.split("&")
    dict = {}
    for x in l:
        sub_l = x.split("=")
        if sub_l[1]:
            dict[sub_l[0]] = sub_l[1]
    return dict