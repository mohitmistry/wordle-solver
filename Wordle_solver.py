from random import randint

# Loads the text file with the applicable words into a txt file
def load_words(let):
    wordlist = open('dict.txt','r').read().split("\n")
    D = open(f"{let}letter_wordle_dict.txt", "a")
    lslen = len(wordlist)
    i = 0
    while i < lslen:
        if wordlist[i].isalpha() and len(wordlist[i]) == let:
            D.write(wordlist[i]+"\n")
        i+=1

# Global Variables
word = [""]*5
guesslst = []
answerlst = []
green = []
yellow = []
blank = []

# Getting proper format for the answers string since it relies on 3 letters
# outputs true and false depending on if the letters are all either g, y, b
def proper_format(str):
    for x in str:
        if x not in ['g','b','y']:
            return False
        else:
            continue
    return True

# getting the inputs for wordle guesses and appending them to the master answers list
# no output but has multiple validations
def get_input(gnum):
    while True:
        print(f"Input guess {gnum + 1}:")
        guess = input().lower()
        if guess.isalpha() and len(guess) == 5:
            guesslst.append(guess)  
            break
        else:
            print('Input not valid, try again.')
    
    # Getting the correct letter check and validating format
    while True:
        print("Input 5 letter check - G for Green, Y for Yellow, and B for blank (EX. GYBBB):")
        answer = input().lower()
        if proper_format(answer) and len(answer) ==5:
            answerlst.append(answer)
            break
        else:
            print('Input not valid, try again.')
    
# OLD  - use filter_sort_words instead
# Helper function to sort the guess and answer into the corresponding list for the letter
def OLD_sort_words(gnum):
    i=0
    while i < 5:
        if answerlst[gnum][i] == "g":
            word[i] = guesslst[gnum][i]
            green.append(word[i])

        elif answerlst[gnum][i] == "b" and guesslst[gnum][i] not in blank and guesslst[gnum][i] not in green:
            blank.append(guesslst[gnum][i])
            #print(blank)
            
        elif answerlst[gnum][i] == "y":
            yellow.append(guesslst[gnum][i])

        i += 1

# Incorporating both filter/sort functions to ensure 
# This one has yellow functionality B)
def filter_sort_words(gnum, lst):
    maxwordlistsize = len(lst)
    templst = []
    templst2 = []

    #getting blank letters into a list and setting the G letters in Word
    for i in range(5):
        if answerlst[gnum][i] == 'b':
            blank.append(guesslst[gnum][i])
        elif answerlst[gnum][i] == "g":
            word[i] = guesslst[gnum][i]
    
    #making templist for for words that have none of the blank letters
    for x in lst:
        if len(set(blank) & set(x))==0:
            templst.append(x)
    templistsize = len(templst)

    # the weird as frik Y filters
    for x in range(templistsize):
        for i in range(5):
            if templst[x] == '':
                continue
            elif answerlst[gnum][i] == 'y':
                if templst[x][i] == guesslst[gnum][i] or guesslst[gnum][i] not in templst[x]:
                    templst[x] = ''

    # clean up the templst    
    for x in templst:
        if x != '':
            templst2.append(x)
    
    templst = []
    templistsize = len(templst2)

    # the green one, finally
    for i in range(5):    
        if answerlst[gnum][i] == 'g':
            for x in range(templistsize):
                if templst2[x] == '':
                    continue
                if templst2[x][i] != guesslst[gnum][i]:
                    templst2[x] = ''
    
    #clean up the templst
    for x in templst2:
        if x != '':
            templst.append(x)

    return templst

# OLD - use filter_sort_words instead
# Helper function to use the sorted lists from above to filter out the incorrect words
# No functionality with yellow letters just yet - use filter_sort_words instead
def OLD_filter_words(lst):
    maxwordlistsize = len(lst)
    templst = []
    templst2 = []
    for x in range(5):
        if word[x] != '':
            for y in range(maxwordlistsize):
                if lst[y] == "":
                    continue
                elif word[x] != lst[y][x]:
                    lst[y] = ""
    
    for y in range(maxwordlistsize):
        if lst[y] == "":
            continue
        else:
            templst.append(lst[y])
    '''
    for x in templst:
        if len(set(yellow) & set(x))>0:
            print(set(yellow) & set(x))
            templst2.append(x)
    '''        
    
    for x in templst:
        if len(set(blank) & set(x))==0:
            templst2.append(x)
    
    return templst2
                    
# Helper to print out the next guesses to not overwhelm the user
# No word rank based functionality yet - COMING SOON!
def print_next_guess(lst):
    oglst = lst
    lstlen = len(lst)
    oglen = lstlen
    if lstlen == 0:
        print("There are no words, try this process again.")    
    elif lstlen <= 10:
        print("Try any of: " + ", ".join(lst))
    else:
        while True:
            if lstlen > 30:
                lst = lst[::randint(2,5)]
                lstlen = len(lst)
            elif lstlen <= 10:
                print(f"The list is over 10 items ({oglen}), you can try some of the following: "+", ".join(lst))
                break  
            else:
                lst = lst[::randint(2,3)]
                lstlen = len(lst)
    
    need_more = input("Need more? (Yes/No) ")

    if need_more.lower() == 'yes':
        lst = list(set(oglst).difference(set(lst)))
        lstlen = len(lst)

        if lstlen == 0:
            print("There are no words, try this process again.")    
        elif lstlen <= 10:
            print("Try any of: " + ", ".join(lst))
        else:
            while True:
                if lstlen > 30:
                    lst = lst[::randint(2,5)]
                    lstlen = len(lst)
                elif lstlen <= 10:
                    print(f"The list is over 10 items ({oglen}), you can try some of the following: "+", ".join(lst))
                    break  
                else:
                    lst = lst[::randint(2,3)]
                    lstlen = len(lst)

# Main function to call helpers
def wordle_solver():
    file_handle = open('wordle_dict.txt','r')
    maxwordlist = file_handle.read().lower().split("\n")
    file_handle.close()
    gnum = 0
    while gnum < 6:
        get_input(gnum)
        maxwordlist = filter_sort_words(gnum, maxwordlist)
        #print (maxwordlist)
        print_next_guess(maxwordlist)
        gnum += 1
        if "" not in word:
            print("You won!")
            break
        elif gnum == 6:
            print("Sorry, I couldn't help this time")
            break       

if __name__ == '__main__':
    wordle_solver()