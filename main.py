from flask import *
import json
from markupsafe import escape
from hashlib import md5

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World2!</p>"








@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


class Player():                             #κλάση παίκτη για τη δημιουργία και τη διαχείρηση των παικτών
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0
        


    def create_new_profile(self):           #μέθοδος της κλάσης Player οπου αποθηκεύει τα νεουδρυθέντα προφίλ στο αρχείο
        f = open("data.json",'r+')          #το αρχείο με τα σκόρ είναι τύπου json 
        database = json.load(f)

        hashed_password = md5(self.password.encode()).hexdigest() #ο κωδικός αποθηκεύεται σε κατακερματισμένη (hashed) μορφή md5
        userprofile = [hashed_password, self.score]
        nickname = self.username               
        database.update({nickname: userprofile}) #το νέο προφίλ μπαίνει στη βιβλιοθήκη 
        f.seek(0)
        json.dump(database, f, indent = 4)       #το προφίλ αποθηκεύεται στη βάση δεδομένων  
        f.close()
        
    def login(self):
        '''Μέθοδος της κλάσης Player που διαχειρίζεται την επαλήθευση του κωδικού και το login'''
        f = open("data.json",'r+')
        database = json.load(f)
        hashed_password = md5(self.password.encode()).hexdigest() #υπολογίζεται το hash του κωδικού που υπέβαλε ο χρήστης
        

        


        if self.lookup_player() == True:
            if hashed_password == database[self.username][0]:
                self.score = database[self.username][1]         #οταν επαληθευτεί και το όνομα χρήστη και ο κωδικός, δίνεται στον παίκτη το προηγούμενο του σκόρ
                return self
            else:
                return 1
        else: return 2

    
        

    def lookup_player(self):      #Μέθοδος της κλάσης Player που αναζητά αν υπάρχει το προφιλ στο αρχείο
        f = open("data.json",'r+')
        database = json.load(f)
        profile_found = False
        for profile in database:
            if self.username == profile:
                profile_found = True
                break





        f.close()
        return profile_found


        

    
        

def gameloop():
    username = input("Give username:")
    password = input("GIve password:")
    
    player1 = Player(username, password)
    player1.create_new_profile()
    player1.lookup_player()
    player1.login()
    
    print(player1.password)
    pass


if __name__ == "__main__":
    gameloop()






app.run(debug=True)