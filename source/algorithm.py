import json
import pandas as pd
import numpy as np
from collections import OrderedDict

users = ['Alice', 'Bob', 'Mitch', 'sumedh']
cols = ['EastCoast', 'Manager', 'WestCoast', 'Associate']
obj = ['sales', 'reports']
attr = ['WestCoast', 'EastCoast', 'Customer']


def Create_UAR():
    users = ['Alice', 'Bob', 'Mitch', 'sumedh']
    cols = ['EastCoast', 'Manager', 'WestCoast', 'Associate']
    # f = open('user_attributes.json')
    # data = json.load(f)
    UAR = np.zeros(shape=[len(users), len(cols)])
    UAR[0][1]=1
    UAR[0][2]=1

    UAR[1][2]=1
    UAR[1][3]=1

    UAR[2][0]=1
    UAR[2][1]=1

    UAR[3][0]=1
    UAR[3][3]=1


    return UAR

def Create_OAR():

    OAR = np.zeros(shape=[len(obj), len(attr)])
    OAR[0][0]=1
    OAR[0][2]=1

    OAR[1][1]=1
    OAR[1][2]=1
    ##print(OAR)
    return OAR

def Create_Policy():
    attributes = [
        "Manager,WestCoast|WestCoast,Customer",
        "WestCoast,Associate|WestCoast,Customer",
        "EastCoast,Manager|EastCoast,Customer",
        "EastCoast,Associate|EastCoast,Customer"
    ]
    permission = [
        "find",
        "find",
        "find",
        "insert"
    ]

    policy = pd.DataFrame(attributes, columns=['attributes'])
    policy['permission'] = permission

    return policy

def Create_Authorizations():
    uar = Create_UAR()
    oar = Create_OAR()
    policy = Create_Policy()
    superset_attr = []


    for u in range(0, len(users)):
        temp_attr = ""
        for c in range(0, len(cols)):
            if uar[u][c] == 1:
                temp_attr = temp_attr+cols[c]+","
        temp_attr = temp_attr[:-1]
        temp_attr = temp_attr + "|"
        #print(temp_attr)

        for o in range(0, len(obj)):
            t2 = ""
            for a in range(0, len(attr)):
                if oar[o][a] == 1:
                    t2=t2+attr[a]+","
            t2 = t2[:-1]
            #print(t2)
            search_attr = temp_attr+t2
            #print(search_attr)
            superset_attr.append(search_attr)

    #print(superset_attr)

    #seaarch each policy in superset
    satisfied_pol = []
    satisfied_perms = []
    for pol in policy['attributes']:
        #print(pol)
        if superset_attr.index(pol) != -1:
            satisfied_pol.append(pol)
            #policy[policy["attributes"]==pol].index.values)
    #print(satisfied_perms)

    #get user and object that satisfied policy
    satisfied_user_attr = []
    satisfied_object_attr = []
    for i in range(0, len(satisfied_pol)):
        satisfied_user_attr.append(satisfied_pol[i].split("|")[0])
        satisfied_object_attr.append(satisfied_pol[i].split("|")[1])
    #print(satisfied_object_attr)

    #find user in UAR
    final_user_list = []
    for u in range(0, len(users)):
        temp_attr = ""
        for c in range(0, len(cols)):
            if uar[u][c] == 1:
                temp_attr = temp_attr+cols[c]+","
        temp_attr = temp_attr[:-1]
        #print(temp_attr)
        for i in range(0, len(satisfied_user_attr)):
            if satisfied_user_attr[i] == temp_attr:
                final_user_list.append(users[u])
                #print(users[u])

    print(final_user_list)

    #find object from OAR
    final_object_list = []
    for o in range(0, len(obj)):
        t2 = ""
        for a in range(0, len(attr)):
            if oar[o][a] == 1:
                t2 = t2 + attr[a] + ","
        t2 = t2[:-1]
        #print(t2)
        for i in range(0, len(satisfied_object_attr)):
            if satisfied_object_attr[i] == t2:
                final_object_list.append(obj[o])

    print(final_object_list)

    #find permissions on these each policy
    final_perm_list = []
    t1=[]
    t2=[]

    for i, rows in policy.iterrows():
        for p in satisfied_pol:
            if rows["attributes"] == p :#and (p not in t1 or rows["permission"] not in final_perm_list):
                t1.append(p)
                final_perm_list.append(rows["permission"])
    perms = pd.DataFrame()
    perms["attr"]=t1
    perms["permissions"]=final_perm_list
    perms = perms.drop_duplicates(ignore_index=True)
    final_perm_list = perms["permissions"]

    print(final_perm_list)

    Auth_Matrix = pd.DataFrame(columns=['Users','Objects','Permissions'])
    Auth_Matrix['Users'] = final_user_list
    Auth_Matrix['Objects'] = final_object_list
    Auth_Matrix['Permissions'] = final_perm_list
    print("Authorization MAtrix:")
    print(Auth_Matrix)

    return Auth_Matrix

def Derive_User_Permission_Assignment():
    # us = []
    # o_op = []
    auth_matrix = Create_Authorizations()
    # for i,rows in auth_matrix.iterrows():
    #     o_op_t = rows["Objects"]+"-"+rows["Permissions"]
    #     if o_op_t not in o_op:
    #         o_op.append(o_op_t)
    #
    # UPA = pd.DataFrame(columns=o_op)
    # for u in auth_matrix["Users"]:
    #     if u not in us:
    #         us.append(u)
    # UPA["Users"] = us
    # UPA = UPA.fillna(0)
    # #UPA.set_index("Users", inplace=True)

    UPA = pd.DataFrame().astype(int)
    UPA = UPA.fillna(0)
    for i, rows in auth_matrix.iterrows():
        obj_perm = rows["Objects"]+"-"+str(rows["Permissions"])
        df = pd.DataFrame({"Users":rows["Users"], obj_perm:1}, index=[0])
        UPA = UPA.append(df)
        UPA = UPA.fillna(0)
        UPA = UPA.drop_duplicates()

    #fill the UPA matrix
    print(UPA)

    return UPA

def Derive_User_Assignment():

    UPA = Derive_User_Permission_Assignment()

    Roles = UPA.columns
    Roles = Roles[1:]
    print("\nRoles generated:")
    print(Roles)
    return UPA

