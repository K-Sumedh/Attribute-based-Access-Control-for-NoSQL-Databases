import pymongo as pm
import algorithm

def Create_User_Roles():
    UA = algorithm.Derive_User_Assignment()
    Roles = UA.columns
    Roles = Roles[1:]
    Users = UA["Users"]

    client = pm.MongoClient('localhost',
                         username='myUserAdmin',
                         password='admin',
                         authSource='admin')
    for role in Roles:
        obj = role.split("-")[0]
        action = role.split("-")[1]
        db = client[obj]
        roleName =  role+"_role"
        # coll = db.list_collection_names()
        # print(coll)
        present_roles = []
        for p_role in db.command("rolesInfo")["roles"]:
            present_roles.append(p_role["role"])

        if roleName not in present_roles:
            db.command("createRole", roleName,
                       privileges=[{"resource": {"db": obj, "collection": ""},
                                    "actions": [action]}],
                       roles=[])

    print("\n*** All ROLES CREATED SUCCESSFULLY ***")

    #now create users and assign appropriate roles to them
    present_users = []
    for i, row in UA.iterrows():
        for role in Roles:
            if row[role] == 1:
                #print(row["Users"]+"-"+str(role))
                obj = role.split("-")[0]
                db = client[obj]
                for u in db.command("usersInfo")["users"]:
                    present_users.append(u["user"])
                if row["Users"] not in present_users:
                    #print("creating user")
                    db.command(
                        'createUser', row["Users"],
                        pwd=row["Users"],
                        roles=[{'role': role+"_role", 'db': obj}]
                    )
                else:
                    print("granting role to exisiting user")
                    db.command({"grantRolesToUser": row["Users"],
                                   "roles": [
                                       {'role': role+"_role", 'db': obj}
                                   ],
                                   'writeConcern': {'w': "majority", 'wtimeout': 2000}
                                   })

    print("*** ALL USERS CREATED SUCCESSFULLY AND ROLES ARE ASSIGNED ***")




Create_User_Roles()


