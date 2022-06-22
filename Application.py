import wikipedia
import sqlite3

con = sqlite3.connect('famous_people.db')
cur = con.cursor()

#Creating the database table if not existing
cur.execute('''CREATE TABLE IF NOT EXISTS famous_people
               (ID INTEGER PRIMARY KEY, Name text NOT NULL, Summary text)''')

#Mini command line program to look on wikipedia
while True :
    who = input("Who should I look for on Wikipedia? (If you want to exit, write \"exit\".)\n")
    if who == "exit" :
        break
    # Getting the search
    query = wikipedia.search(who, suggestion=True)
    result = query[0]
    suggestion = query[1]
    name = result[0] if len(result) != 0 else None
    if name == who: # if there is an error in the name
        summary = wikipedia.summary(name, sentences=10, auto_suggest=False, redirect=False)
        if len(result)>=1 : # if we found at least one result
            print("I found : ")
            print(name) # it shows the first result
            print("I hope it was the person you were looking for !")
            if suggestion is not None :
                  print("else I do suggest you to look for \""+suggestion+"\".")
            # we then insert it into the db
            cur.execute('''INSERT OR REPLACE INTO famous_people (Name, Summary) VALUES (?,?)''', (name, summary))
            con.commit()
        elif suggestion is not None : # if we found nothing but we have a suggestion
            print("I found no one for the query about : "+who+"\nBut maybe you meant : \""+suggestion+"\" ?")
        else : # if we found nothing and there isn't even a suggestion
            print("I found no one for the query about : "+who+"\nAnd there was no suggestion available.")
    else :
        print("I found no one for the query about : "+who)
        if suggestion is not None : # if there is a suggestion
            print("But maybe you meant : \""+suggestion+"\" ?")
        else :
            print("And there was no suggestion. But here what I found : ")
            print(result) # debug ; it shows what it found without suggestion, shouldn't happen in this situation
            
con.close()