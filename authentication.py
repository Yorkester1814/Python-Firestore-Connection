import firebase_admin
from firebase_admin import credentials, firestore

API_key = "config.json"
cred = credentials.Certificate(API_key)
firebase_admin.initialize_app(cred)
fbt = firestore.client()
DOCS = fbt.collection("User")
docr_stream = DOCS.stream()

def invalid_name(strg):
    if " " in strg:
        return True
    
def not_Unique(strg):
    if invalid_name(strg) != True:
        for doc in docr_stream:
            DOC = doc.to_dict()
            if strg == DOC["Username"]: 
                return True

class User:
    def __init__(self):
        self.UN = None
        self.PW = None
        self.FN = None
        self.LN = None
    
    def remove(self):
        print("\nDeleting option enabled")
        acc = DOCS.document(self.UN)
        acc.delete()
        print(f"account {acc.id} successfully deleted\n")

                
    def edit_account(self):
        print("\nEditing option enabled")
        while True:
            dr = DOCS.document(self.UN)
            data = dr.get().to_dict()
            try:            
                print("1. username")
                print("2. password")
                print("3. first name")
                print("4. last name")
                E = int(input(f"What do you want to edit in your account: ")) 

                if E == 1:
                    new_un = str(input("Enter new username: "))
                    if invalid_name(new_un): 
                        print("username you provided is of wrong format, provide single-word username")
                    else:
                        if not_Unique(new_un):
                            if new_un == self.UN: 
                                print("no change in username will occur")
                            else:
                                print("username you provided already exist, provide another username")
                        else:
                            new_dr = DOCS.document(new_un)
                            new_dr.set(data)
                            new_dr.update({"Username": new_un})
                            dr.delete()
                            print(f"username & account name renamed to {new_dr.id}")

                elif E == 2:
                    new_pw = str(input("Enter new password: "))
                    dr.update({"Password": new_pw})
                    print(f"password of account '{dr.id}' changed to {new_pw}")
                
                elif E == 3:
                    new_fn = str(input("Enter new first name: "))
                    if invalid_name(new_fn):
                        print("first name you provided is of wrong format, provide correct first name")
                    else:
                        dr.update({"First_name": new_fn})
                        print(f"first name of account '{dr.id}' changed to {new_fn}")

                elif E == 4:
                    new_ln = str(input("Enter new last name: "))
                    if invalid_name(new_ln):
                            print("last name you provided is of wrong format, provide correct last name")
                    else:
                        dr.update({"Last_name": new_ln})
                        print(f"last name of account '{dr.id}' changed to {new_ln}")
                else:
                    print("editing is completed\n")
                    break
            
                self.UN = new_dr
            
            except ValueError:
                print("Invalid input! Please enter integer")         

    def sign_in(self):
        print("\nSign-in option enabled")
        self.UN = str(input("Username: "))
        self.PW = str(input("Password: "))
        self.FN = str(input("First name: "))
        self.LN = str(input("Last name: "))

        if invalid_name(self.UN) or invalid_name(self.FN) or invalid_name(self.LN):
            print("provide single word input. multiple words aren't allowed\n")
        else:
            if not_Unique(self.UN):
                print("username already exist. provide unique username\n")
            else:
                doc_ref = DOCS.document(self.UN)
                data = {"Username": self.UN, "Password": self.PW, "First_name": self.FN, "Last_name": self.LN}
                doc_ref.set(data)
                print(f"Account successfully created with ID: {doc_ref.id}\n")

    def login(self):
        print("\nLog-in option enabled")
        self.UN = str(input("Enter username you want to log-in: "))
        self.PW = str(input("Enter password for the account: "))
        flag = False

        for doc in docr_stream:
            DOC = doc.to_dict()
            if (DOC["Username"] == self.UN) and (DOC["Password"] == self.PW):
                print(f"Access to your account {self.UN} is granted\n")
                flag = True
                break

        if flag == True: 
            modify = str(input("What do you want to do in your account: "))
            if modify == "edit": self.edit_account()
            elif modify == "remove": self.remove()
            else: print("No modification occurs\n")

        else:
            if (DOC["Username"] == self.UN) and (DOC["Password"] != self.PW):
                print("account exist but your password for it is wrong\n")
            elif invalid_name(self.UN):
                print("user-input contain multiple words, so the account you try to log-in doesn't exist at all\n")
            else:
                print("account you want to access doesn't exist\n")

def main():
    obj = User()
    while True:
        preg = str(input("What do you want: "))
        if preg == "login": obj.login()
        else: obj.sign_in()

main()

""" 1. API-key: unique identifier that allows user to interact with database via API (Application Programming Interface). """
