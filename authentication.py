import firebase_admin
from firebase_admin import credentials, firestore

API_key = "C:\\Users\\priya\\Downloads\\fbt1-957b5-firebase-adminsdk-j232s-53ef972615.json"
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
                data = {"Username": self.UN, "Password": self.PW, "First_name": self.FN, "Last_name": self.LN}
                account = DOCS.document()
                account.set(data)
                print(f"Account successfully created with ID: {account.id}\n")

    def login(self):
        print("\nLog-in option enabled")
        self.UN = str(input("Enter username you want to log-in: "))
        self.PW = str(input("Enter password for the account: "))

        flag = False
        for doc in docr_stream:
            DOC = doc.to_dict()
            if (DOC["Username"] == self.UN) and (DOC["Password"] == self.PW):
                print(f"Access to your account {doc.id} is granted\n")
                flag = True
                break

        if flag == True: 
            modify = str(input("What do you want to do in your account: "))

            if modify == "edit": 
                print("\nEditing option enabled")
                while True:
                    try: 
                        account = DOCS.document(doc.id) 
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
                                    if new_un == self.UN: print("no change in username will occur")
                                    else: print("username you provided already exist, provide another username")
                                else:
                                    self.UN = new_un
                                    account.update({"Username": new_un})
                                    print(f"username renamed to {self.UN}")

                        elif E == 2:
                            new_pw = str(input("Enter new password: "))
                            self.PW = new_pw
                            account.update({"Password": self.PW})
                            print(f"password changed to {self.PW}")
                
                        elif E == 3:
                            new_fn = str(input("Enter new first name: "))
                            if invalid_name(new_fn):
                                print("first name you provided is of wrong format, provide correct first name")
                            else:
                                self.FN = new_fn
                                account.update({"First_name": self.FN})
                                print(f"first name changed to {self.FN}")

                        elif E == 4:
                            new_ln = str(input("Enter new last name: "))
                            if invalid_name(new_ln):
                                print("last name you provided is of wrong format, provide correct last name")
                            else:
                                self.LN = new_ln
                                account.update({"Last_name": self.LN})
                                print(f"last name changed to {self.LN}")
                        else:
                            print("editing is completed\n")
                            break
            
                    except ValueError:
                        print("Invalid input! Please enter integer")

            elif modify == "remove":
                print("\nDeleting option enabled") 
                doc.reference.delete()
# We've used doc.reference because it provide actual path of document as doc is an object of our data & it can't be used with delete()
                print(f"account {doc.id} successfully deleted\n")

            else: 
                print("No modification occurs\n")

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

""" 1. API-key: unique identifier that allows user to interact with database via API (Application Programming Interface) """
