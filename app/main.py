from flask import *
import json
import random
from hashlib import md5


# import os #debugging purposes

app = Flask(__name__, template_folder='html')


class Player():                             #κλάση παίκτη για τη δημιουργία και τη διαχείρηση των παικτών
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0
        


    def create_new_profile(self):           #μέθοδος της κλάσης Player οπου αποθηκεύει τα νεουδρυθέντα προφίλ στο αρχείο
        f = open("app/data.json",'r+')          #το αρχείο με τα σκόρ είναι τύπου json 
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
        f = open("app/data.json",'r+')
        database = json.load(f)
        print("has for ",self.password)
        hashed_password = md5(self.password.encode()).hexdigest() #υπολογίζεται το hash του κωδικού που υπέβαλε ο χρήστης
        print("is: ",hashed_password)

        


        if self.lookup_player() == True:
            if hashed_password == database[self.username][0]:
                self.score = database[self.username][1]         #οταν επαληθευτεί και το όνομα χρήστη και ο κωδικός, δίνεται στον παίκτη το προηγούμενο του σκόρ
                return self
            else:
                return 1
        else: return 2

    
        

    def lookup_player(self):      #Μέθοδος της κλάσης Player που αναζητά αν υπάρχει το προφιλ στο αρχείο
        f = open("app/data.json",'r+')
        database = json.load(f)
        profile_found = False
        for profile in database:
            if self.username == profile:
                profile_found = True
                break





        f.close()
        return profile_found

class Game():
    def __init__(self, player, highscore, difficulty):
        self.player = player
        self.current_highscore = highscore
        self.difficulty = difficulty

    
    def generate_number(self):            #TODO: tune the difficulty parameters 
        if self.difficulty == 1:
            number = random.randint(1,10)
            return number
        elif self.difficulty == 2:
            number = random.randint(1,50)
            return number
        elif self.difficulty == 3:
            number = random.randint(1,100)
            return number
        else :
            return -1   #error
            
    def test_number(self, player_number, game_number):
        if player_number == game_number:
            return 0
        elif player_number < game_number:
            return -1
        elif player_number > game_number:
            return 1
        else:
            return 9999 #error
            

        
        

    
        

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
    



    @app.route("/")
    def initialize():
        app.static_folder = 'static'
    
        return render_template("index.html")
    
    @app.route("/login", methods=['POST'])
    def login():
        user =Player(request.form['Username'], request.form['Password'])
        result = user.login()
        print(result)
        show_highscore = False
        show_greeting = False

        while type(result) == int:
            if result == 1:
                print("wrong password")
            elif result == 2:
                user.create_new_profile()
                result = user
                print("user didmt exist, created account")
                
        if type(result) != int:
            show_highscore = True
            show_greeting = True
            


        print(show_highscore, show_greeting)
        return render_template("index.html", show_highscore=show_highscore, show_greeting=show_greeting)
        
'''TODO
        fix the classes system for the visibility of the highscore and the greeting
        now the highscore is wokring but the greeting is not
''' 
        






app.run(debug=True)