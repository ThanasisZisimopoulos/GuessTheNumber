from flask import *
import json
import random
from hashlib import md5
import secrets


# import os #debugging purposes

app = Flask(__name__, template_folder='html')


class Player():                             #κλάση παίκτη για τη δημιουργία και τη διαχείρηση των παικτών
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0
        


    def create_new_profile(self):           
        '''μέθοδος της κλάσης Player οπου αποθηκεύει τα νεουδρυθέντα προφίλ στο αρχείο'''
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
        
        

        hashed_password = md5(self.password.encode()).hexdigest() #υπολογίζεται το hash του κωδικού που υπέβαλε ο χρήστης
                
        if self.username == "":  #η περιπτωση οπου ο χρήστης πατησε το login χωρις να βαλει ονομα
            return 0
        
        if len(self.password)<8:
            print("too small password")
            return -1

        if self.lookup_player() == True:
            if hashed_password == database[self.username][0]:
                self.score = database[self.username][1]         #οταν επαληθευτεί και το όνομα χρήστη και ο κωδικός, δίνεται στον παίκτη το προηγούμενο του σκόρ
                return self
            else:
                return 1
        else: 
            return 2
    
    def find_highscore(self):
        '''μέθοδος της κλάσης Player οπου επιστρέφει το μεγαλύτερο score που εχει επιτευγθεί'''
        f = open("app/data.json",'r+')          #το αρχείο με τα σκόρ είναι τύπου json 
        database = json.load(f)
        highscore = 0
        for user in database:
            if database[user][1] > highscore:
                highscore = database[user][1]



        print(highscore)
        session['best_score'] = highscore
        
        
        f.close()
        return highscore

        

    
        

    def lookup_player(self):     
        '''Μέθοδος της κλάσης Player που αναζητά αν υπάρχει το προφιλ στο αρχείο και επιστρέφει boolean'''
        f = open("app/data.json",'r+')
        database = json.load(f)
        profile_found = False

        if self.username == '':
            print("User didnt enter username")
            profile_found = False

        else:
            for profile in database:
                if self.username == profile:
                    profile_found = True
                    break
       
        f.close()
        return profile_found



class Game():
    def __init__(self, player, highscore):
        self.player = player
        self.current_highscore = highscore
        self.difficulty = 0

    
    def generate_number(self):            #TODO: tune the difficulty parameters 
        "μέθοδος της κλάσης game που επιστρέφει τυχαίο αριθμό ανάλογα με τη δυσκολία"
        if self.difficulty == 'easy':
            number = random.randint(1,10)
            return number
        elif self.difficulty == 'medium':
            number = random.randint(1,50)
            return number
        elif self.difficulty == 'hard':
            number = random.randint(1,100)
            return number
        else :
            return -1   #error
            
    def test_number(self, player_number, game_number):
        '''μέθοδος της κλάσης game που ελέγχει αν ο παίκτης βρήκε τον αριθμό'''
        if player_number == game_number:
            return 0
        elif player_number < game_number:
            return -1
        elif player_number > game_number:
            return 1
        else:
            return 9999 #error
        
    def round(self)
            

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
    app = Flask(__name__, template_folder='html')
    key = secrets.token_hex()
    key = md5(key.encode()).hexdigest()
    app.secret_key = key
    



    @app.route("/")
    def initialize():
        app.static_folder = 'static'
    
        return render_template("index.html")
    
    @app.route("/login", methods=['POST'])
    def login():
        user =Player(request.form['Username'], request.form['Password'])
        result = user.login()
        print(result)
        

        if type(result) == int:
            
            if result == 0:
                print("user didnt enter username")
                info_text = "Please enter a username"
                return render_template("index.html", info_text=info_text)
            if result == -1:
                print("too small password")
                info_text = "Please enter a password at least 8 characters long"
                return render_template("index.html", info_text=info_text)
            if result == 1:
                print("wrong password")
                info_text = "Wrong password"
                return render_template("index.html", info_text=info_text)
            if result == 2:
                user.create_new_profile()
                result = user
                info_text = "Account sucessfully created, login again to play"
                return render_template("index.html", info_text=info_text)
                
        else:# type(result) != int:
            
            
            session['username'] = result.username
            session['userscore'] = result.score
            
            return redirect("main_menu")
            

        return render_template("index.html")
    
    @app.route("/main_menu")
    def main_menu():
        user =Player(session['username'], None) #δημιουργω ενα αντικέιμενο player για να τρέξω την find_highdcore 
        best_score = user.find_highscore()
        best_score = 'Best score ever: '+ f"{best_score}"
        
        pressed = 'medium'
        session['difficulty'] = pressed
        greeting = "Welocome "+session['username']+"!"
        Player_highscore = 'Your highscore: ' + f"{session['userscore']}"
        return render_template("main_menu.html", greeting=greeting, pressed=pressed, Player_highscore=Player_highscore, best_highscore=best_score )
    
    @app.route('/button_pressed', methods=['POST'])
    def button_pressed():
        '''συνάρτηση που δειαχειρίζεται ποιο κουμπί πατήθηκε'''     
        action = request.form.get('action')
        
        if action == 'logout': #ο χρήστης πατησε logout
            session['username'] = None
            return redirect("/")
        elif action == 'start': #ο χρήστης πατησε start
            return redirect("/game")
        else:                  #ο χρήστης άλλαξε τη δυσκολία
            session['difficulty'] = action

            user =Player(session['username'], None) #δημιουργω ενα αντικέιμενο player για να τρέξω την find_highdcore 
            best_score = user.find_highscore()
            best_score = 'Best score ever: '+ f"{best_score}"
        
            
            
            greeting = "Welocome "+session['username']+"!"
            Player_highscore = 'Your highscore: ' + f"{session['userscore']}"
            return render_template("main_menu.html", greeting=greeting, pressed=session['difficulty'], Player_highscore=Player_highscore, best_highscore=best_score )

        

    @app.route('/game')
    def game():
        round = Game(session['uesrname'], session['userscore'])
        round.difficulty = session['difficulty']
        
    
        return "Game has started"

        


        
        

        
        
 
        






app.run(debug=True)