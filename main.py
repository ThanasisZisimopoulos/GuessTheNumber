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
                
        if self.username == "":  #η περιπτωση οπου ο χρήστης πατησε το login χωρις να βαλει ονομα
            return 0
        
        if len(self.password)<8: #η περιπτωση οπου ο χρήστης έβαλε υπερβολικά μικρό κωδικό
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
        f = open("data.json",'r+')          #το αρχείο με τα σκόρ είναι τύπου json 
        database = json.load(f)
        highscore = 0
        for user in database:               #γίνεται αναζήτηση σε όλο το αρχείο σε όλους του αποθηκευμένους παίκτες για το μεγαλύτερο σκόρ
            if database[user][1] > highscore:
                highscore = database[user][1]

        session['best_score'] = highscore
        
        
        f.close()
        return highscore

        

    
        

    def lookup_player(self):     
        '''Μέθοδος της κλάσης Player που αναζητά αν υπάρχει το προφιλ στο αρχείο και επιστρέφει boolean'''
        f = open("data.json",'r+')
        database = json.load(f)
        profile_found = False

        if self.username == '':                 #Η περίπτωση που το username είναι κενό
            print("User didnt enter username")
            profile_found = False

        else:
            for profile in database:
                if self.username == profile:    #αν βρεθεί ο παίκτης επιστρέφει True
                    profile_found = True
                    break
       
        f.close()
        return profile_found





def generate_number(difficulty):            
    "μέθοδος της κλάσης game που επιστρέφει τυχαίο αριθμό ανάλογα με τη δυσκολία"
    if difficulty == 'easy':
        number = random.randint(1,10)
        return number
    elif difficulty == 'medium':
        number = random.randint(1,50)
        return number
    elif difficulty == 'hard':
        number = random.randint(1,100)
        return number
    else :
        return -1   #error
        
def test_number(player_number, game_number):
    '''μέθοδος της κλάσης game που ελέγχει αν ο παίκτης βρήκε τον αριθμό'''
    if player_number == game_number:
        return 0
    elif player_number < game_number:
        return -1
    elif player_number > game_number:
        return 1
    else:
        return 9999 #error
    
    
            


app = Flask(__name__, template_folder='html')
key = secrets.token_hex() 
key = md5(key.encode()).hexdigest() #για επιπλέων ασφάλεια, το αποτέλεσμα κατακερματίζεται με το md5 
app.secret_key = key

@app.route("/")
def initialize():                   #η αρχική οθόνη
    app.static_folder = 'static'
    session.clear()#γίνεται reset του παιχνιδιού

    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():                        #η login οθόνη
    user =Player(request.form['Username'], request.form['Password']) 
    result = user.login()
    
    
    if type(result) == int: #τα int χρησιμοποιούνται ως κωδικοί σφάλματος
        
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
            
    else:# type(result) != int:           αν δε προκύψει σφάλμα το result ειναι αντικείμενο
        
        
        session['username'] = result.username
        session['userscore'] = result.score
        
        return redirect("main_menu")
        
    # return render_template("index.html")

@app.route("/main_menu",methods=['GET', 'POST'])
def main_menu():                                #το μενού για την επιλογή δυσκολίας
    if 'game_started' not in session:#περίπτωση που δεν εχει αρχίσει το παιχνίδι, δημιουργείται ενα νεο

        session['difficulty'] = 'medium'#προεπιλογή
        session['game_started'] = 'yes'
        
    else:#περίπτωση που εχει ήδη αρχίσει ενα παιχνίδι και ο χρήστης πατησε τo play again

        action = request.form.get('action')
        
        Player_highscore = ''
        best_score = ''

        #διαχείρηση των κουμπιών
        if action == 'logout': #ο χρήστης πατησε logout
            
            session.clear() #γίνεται reset του παιχνιδιού
            return redirect("/")
        
        elif action == 'start': #ο χρήστης πατησε start
            
            return redirect("/game")
        
        elif action == 'easy' or 'medium' or 'hard':                  #ο χρήστης άλλαξε τη δυσκολία
            session['difficulty'] = action
            
            
    user =Player(session['username'], None) #δημιουργω ενα αντικέιμενο player για να τρέξω την find_highdcore 
    best_score = user.find_highscore()
    best_score = 'Best score ever: '+ f"{best_score}"        
    pressed = session['difficulty']
    greeting = "Welocome "+session['username']+"!"
    Player_highscore = 'Your highscore: ' + f"{session['userscore']}"
        
    return render_template("main_menu.html", greeting=greeting, pressed=pressed, Player_highscore=Player_highscore, best_highscore=best_score )


    

@app.route('/game',methods=['GET', 'POST'])
def game():
    
    action = request.form.get('action')
    number = request.form.get('number')
    
    if session['difficulty'] == 'easy':                             #αναλογα τη δυσκολία δειχνω στο χρήστη το σύνολο
        if 'min' not in session: session['min'] = 1                 #στο οποιο ανοικει ο αριθμός
        if 'max' not in session: session['max'] = 10
    elif session['difficulty'] == 'medium':
        if 'min' not in session: session['min'] = 1
        if 'max' not in session: session['max'] = 50
    elif session['difficulty'] == 'hard':
        if 'min' not in session: session['min'] = 1
        if 'max' not in session: session['max'] = 100      
    
    
    if 'round_number' not in session:                               #εδω δημιουργείται ο αριθμός που καλείται να βρει ο παικτης
        
        session['round_number']= generate_number(session['difficulty'])
        print('current number is ',session['round_number'])
    
    if 'function_run_count' not in session:     #μετραω σε ποιο γυρο είναι το παιχνίδι
        session['function_run_count'] = 0
    elif session['function_run_count'] < 7 :
        session['function_run_count'] += 1

    if action == 'enter':
        if number == '' or int(number) > int(session['max']) or int(number) < int(session['min']):          #O παίκτης δεν εδωσε σωστό αριθμό
            session['function_run_count'] -= 1    #Δε μετράμε τον κενό γύρο
            print('rejected round number was', number)
        else:
            try:                                            #αν αυτο που έχει γράψει ο χρήστης δεν είναι αριθμός
                number = int(number)                        #το πρόγραμμα θα πάει στο except 
                if int(session['round_number'])>number: 
                    session['min'] = number
                    if session['function_run_count'] == 7:  #τέλος προσπάθειων αρα τέλος παιχνιδιού
                        session['win'] = False
                        return redirect("/winner_screen")
                elif int(session['round_number'])<number: 
                    session['max'] = number
                    if session['function_run_count'] == 7:   #τέλος προσπάθειων αρα τέλος παιχνιδιού
                        session['win'] = False
                        return redirect("/winner_screen")
                    
                elif int(session['round_number'])==number: #ο παίκτης βρήκε τον αριθμό
                    session['win']=True
                    print('session[win] is ',session['win'])
                    return redirect("/winner_screen")
            except: 
                if type(number)=='str':
                    session['function_run_count'] -= 1
                    
    elif action == 'logout':
        session.clear()
        return redirect('/')
            

    greeting = "Current Player: "+session['username']+"!"

    return render_template("game.html", round=session['function_run_count'], greeting = greeting, min=session['min'], max=session['max'])



@app.route('/winner_screen',methods=['GET', 'POST'])
def winner_screen():
    easy_multiplyer = 100                               # το σκορ υπολογιζεται απο τα εξης:
    medium_multiplyer = 150                             # α) Τη δυσκολία που επίλεξε ο χρήστης
    hard_multiplyer = 500                               # β) Το ποσο πολύ κατάφερε να περιορίσει το  διάστημα στο οποίο είναι ο αριθμός
                                                        # γ) Σε περίπτωση που βρεί τον αριθμό υπάρχει bonus
    win_multiplyer = 2
    attempt_multiplyer = (7 - session['function_run_count'])/7 +1
    
    action = request.form.get('action')
    
    if action == 'logout': #ο χρήστης πάτησε logout
        session.clear()    #γινεται reset του παιχνιδιου
        return redirect('/')
    elif action == 'play-again': # ο χρήστης πάτησε play again
        print('play again pressed')
        temp = (session['username'], session['userscore'])  #κρατάω τα στοιχεία του παικτη
        session.clear()                                     #γίνεται reset το παιχνίδι
        session['username'] = temp[0]                       #επιστρέφονται τα στοιχεία στο session
        session['userscore'] = temp[1]
        return redirect('main_menu')
    

    if session['win'] == True:                              #ο παίκτης βρήκε τον αριθμό
        if session['difficulty']=='easy':   score = win_multiplyer * easy_multiplyer * attempt_multiplyer           #υπολογίζεται το σκόρ
        if session['difficulty']=='medium': score = win_multiplyer * medium_multiplyer * attempt_multiplyer
        if session['difficulty']=='hard':   score = win_multiplyer * hard_multiplyer * attempt_multiplyer
        message1 = 'You have found the number!'
        message2 = 'It was indeed '+str(session['round_number'])+'!'
    else:
        if session['difficulty']=='easy':   score = (1-(  (int(session['max']) -  int(session['min'])) / 10 )  ) * easy_multiplyer   #user used all the attempts, attempt multiplyer is 1 so its omitted
        if session['difficulty']=='medium': score = (1-(  (int(session['max']) -  int(session['min'])) / 50 )  ) * medium_multiplyer
        if session['difficulty']=='hard':   score = (1-(  (int(session['max']) -  int(session['min'])) / 100)  ) * hard_multiplyer
        message1 = 'You were so close!'
        message2 = 'It was '+str(session['round_number'])+'!'

    f = open("data.json",'r+')          #το αρχείο με τα σκόρ είναι τύπου json
    score = round(score, 1)             #στροφφυλοποίηση του score στο 1ο δεκαδικο
    database = json.load(f)
    username = session['username']
    old_score = database[username][1]
    if score > old_score:               #αν το σκορ του παιχνιδιού είναι μεγαλύτερο από
        database[username][1] = score   #το highscore του παικτη, ανανεώνουμε το αρχείο
        session['userscore'] = score
        f.seek(0)
        json.dump(database, f, indent = 4)       
    f.close()
    
    return render_template("winner_screen.html", score = score, message1=message1, message2=message2)

if __name__ == "__main__":
    app.run()