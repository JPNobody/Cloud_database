

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import getpass
import hashlib

def initialize_firestore():
    """
    Create database connection
    """
    # Setup Google Cloud Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Family Recipe Database-6c495b38cba0.json"

    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'family-recipe-database',
    })

    # Get reference to database
    db = firestore.client()
    return db

def check_account(ref):
    """
    This function checks the password given by a user against the password stored in the
    database for that uses. This uses hashing by hashing the password provided and checking
    it against the hashed password in the database.
    """
    # Use getpass so that the password is kept secret
    possiblePassword = getpass.getpass()
    # hash the passord
    hashedPassword = hashlib.sha224(possiblePassword.encode('utf8')).hexdigest()
    print()
    password = ref.collection('password').document('password').get()
    # check if the passwords match
    if hashedPassword == password.to_dict()['password']:
        return True
    else:
        # If the user has a security key, allow them into the account and prompt them to 
        # change their password.
        if 'security key' in password.to_dict():
            securityKey = getpass.getpass("Security Key: ")
            if securityKey == password.to_dict()['security key']:
                edit_account(ref)
                return True
            else:
                return False
        else:
            return False

def add_account(db):
    """
    This function adds an account if the account doesn't already exist
    """
    account_name = input('Account name: ')
    doc = db.collection('accounts').document(account_name).get()
    # print an error if the account already exists
    if doc.exists:
        print('ERROR! User already exists!')
        return
    else:
        # take in a password then hash it and store it.
        password = input('Password: ')
        hashedPassword = hashlib.sha224(password.encode('utf8')).hexdigest()

        # take in a security key for the account.
        securityKey = input("Add a securty key for account recovery: ")
        data = {'name' : account_name}
        passwordData = {"account" : account_name, "password" : hashedPassword, "security key" : securityKey}
        db.collection("accounts").document(account_name).set(data)
        db.collection("accounts").document(account_name).collection('password').document('password').set(passwordData)
        print()

def display_recipe(ref):
    """
    This displays a recipe that the user asks for. 
    a reference to the user's account in the database is passed in.
    """
    # print out the recipes that the user has in their account
    docs = ref.collection('recipes').stream()
    for doc in docs:   
        print(f'{doc.to_dict()["name"]}')

    # get the recipe
    recipe_name = input("What recipe would you like to view? ")
    print()
    results = ref.collection('recipes').document(recipe_name).get()

    # check if the recipe exists and if so, print out the items in the recipe
    if results.exists:
        print(f'Name: {results.to_dict()["name"]}')
        print()
        print(f'Ingrediant : Quantity')
        for item, quant in results.to_dict()["ingrediants"].items():
            print(f'{item} : {quant}')
        print()
        print(f'Directions: \n{results.to_dict()["directions"]}')
        print()
    else:
        print("You don't have a recipe for that.")
        print()

    

def create_list_of_ingrediants():
    """
    This function creates a list of ingrediants, as a dictionary,
    from inputs from the user, and returns that dictionary.
    """
    ingrediants = {}
    choice = None
    ing = input("Ingrediant: ")
    quant = input("Quantity: ")
    print()
    ingrediants[ing] = quant
    # Keep asking to add or delete ingrediants until the user is finished.
    while choice != "f":
        print("(a)dd ingrediant")
        print("(d)elete ingrediant")
        print("(f)inish")
        choice = input("> ")
        print()
        if choice == "a":
            ing = input("Ingrediant: ")
            quant = input("Quantity: ")
            print()
            ingrediants[ing] = quant
        elif choice == "d":
            ing = input("What ingrediant do you want to remove from the recipe: ")
            if ing in ingrediants:
                del ingrediants[ing]
                print("ingrediant removed.")
            else: 
                print("That ingrediant is not in the recipe.")
        elif choice == "f":
            return ingrediants
        else: 
            print("That's not an option.")
            print()

def getRecipeDirections():
    """
    This function creates a string of recipe diretions. The user can continue to add steps
    until they are finished.
    """
    choice = None
    instructions = 'Step 1: ' + input('Step 1: ') + '\n'
    currStep = 2
    while choice != "f": 
        print('(a)dd step')
        print('(f)inish')
        choice = input('> ')
        if choice == "a":
            # add a step according to the current step that is in the recipe. This could use
            # some editing to make it more secure.
            instructions += "Step " + str(currStep) + ': ' + input(f'Step {currStep}: ') + '\n'
            currStep += 1
        elif choice == "f":
            print()
            return instructions
        else:
            print("That's not an options.")
            print()


def add_recipe(ref):
    """
    This function adds a recipe to the user's account.
    The reference to the user's account in the database is passed in.
    """
    recipe_name = input('Recipe name: ')
    ingrediants = create_list_of_ingrediants()
    directions = getRecipeDirections()
    recipe = {"name" : recipe_name, "ingrediants" : ingrediants, "directions" : directions }
    # Use the information gotten above to set the recipe for that account.
    ref.collection('recipes').document(recipe_name).set(recipe)

def update_recipe(ref):
    """
    This function is used to update any or all parts of a recipe.
    The reference to the account the recipe belongs to is passed in.
    """
    # print out all the recipes that belong to that account.
    docs = ref.collection('recipes').stream()
    print("Recipes: ")
    for doc in docs:    
        print(f'{doc.to_dict()["name"]}')
    print()
    recipe_name = input('What recipe would you like to update? ')
    recipe_ref = ref.collection('recipes').document(recipe_name)
    # if the recipe exists, continue
    if recipe_ref.get().exists:
        print('What part of the recipe would you like to update?')
        print('(1) Name')
        print('(2) Ingrediants')
        print('(3) Instructions')
        print('(4) The whole recipe')
        choice = input('> ')
        if choice == "1":
            new_recipe_name = input('Recipe name: ')
            print()
            """
            Because the name of the recipe is also the recipe's id, each time the name is 
            changed, a new recipe has to be created with the old recipe's data. Otherwise
            The program will have errors printing out all the recipes in the various functions 
            it does that.
            """
            new_recipe = {
                'name' : new_recipe_name,
                'ingrediants' : recipe_ref.get().to_dict()["ingrediants"],
                'directions' : recipe_ref.get().to_dict()["directions"]
            }
            ref.collection("recipes").document(new_recipe_name).set(new_recipe)
            recipe_ref.delete()
        elif choice == "2":
            # asks the user to either replace the current list of ingredians or add to it.
            print("(a)dd to current list")
            print("(r)eplace current list")
            choice_2 = input('> ')
            print()
            if choice_2 == 'a':
                # here create a new dictionary with the values that the user gives
                updated_ingrediants = create_list_of_ingrediants() 
                # combine that dictionary with the one already listed for that recipe
                updated_ingrediants.update(recipe_ref.get().to_dict()['ingrediants'])
                # update the recipe with the new dictionary of ingrediants.
                recipe_ref.update({'ingrediants': updated_ingrediants})
            elif choice_2 == 'r':
                # create a new dictionary and set the ingrediants for the recipe equal to that dictionary.
                ingrediants = create_list_of_ingrediants()
                recipe_ref.update({'ingrediants': ingrediants})
        elif choice == "3":
            # create a new string of directions.
            directions = getRecipeDirections()
            recipe_ref.update({'directions': directions})
        elif choice == "4":
            # create a new recipe, and delete the old one.
            new_recipe_name = input('Recipe name: ')
            ingrediants = create_list_of_ingrediants()
            directions = getRecipeDirections()
            recipe = {
                "name" : new_recipe_name,
                "ingrediants" : ingrediants,
                "directions" : directions
            }
            ref.collection("recipes").document(new_recipe_name).set(recipe)
            recipe_ref.delete()
        else:
            print("That's not an option.")
            print()
    else:
        print("You don't have a recipe for that.")
        print()

def delete_recipe(ref):
    """
    This function deletes a recipe in an account.
    The reference to that account in the database is passed in.
    """
    # print out all the recipe names in the database.
    docs = ref.collection('recipes').stream()
    print("Recipes: ")
    for doc in docs:    
        print(f'{doc.to_dict()["name"]}')
    print()
    # get which recipe to delete
    recipe_name = input("Recipe to delete: ")
    print()
    # delete that recipe
    ref.collection('recipes').document(recipe_name).delete()
    print('deleted {}'.format(recipe_name))

def delete_account(ref):
    """
    This function deletes an account by first deleting the password collection and document
    then deleting the recipe collection and documents, and finally deleting the account
    document.
    """
    # make sure the user wants to delete the account.
    choice = input("Are you sure you want to delete your account? (y/n) ")
    if choice == 'y':
        # delete the password collection and document.
        ref.collection('password').document('password').delete()
        # delete the recipes collection and documents
        docs = ref.collection('recipes').stream()

        for doc in docs:
            doc.delete()
        
        # delete the account document.
        ref.delete()
    else:
        return

def edit_account(ref):
    """
    This function currently can only edit the password because of the problem with 
    the account name and id mention in the update function comment about updating
    the name, and in the project description. 
    """
    choice = input("would you like to change your password? (y/n)")
    if choice == 'y':
        # get the new password and hash it
        new_password = input("New password: ")
        hashedPassword = hashlib.sha224(new_password.encode('utf8')).hexdigest()
        print()
        # change the password to the new password.
        ref.collection('password').document('password').update({'password' : hashedPassword})
    else:
        return

def main():
    """
    This function asks the user to sign into an account, and calls all the other 
    functions based on what the user wants to do.
    """
    db = initialize_firestore()
    choice_1= None
    while choice_1 != "q":
        print("(m)ake a new account")
        print("(s)ign into an account")
        print("(q)uit")
        choice_1 = input("> ")
        print()
        if choice_1 == 'm':
            add_account(db)
        elif choice_1 == 's':
            # get which account to access
            account_name = input("Account name: ")
            ref = db.collection("accounts").document(account_name)
            doc = ref.get()
            # if the account exists, call check_account to check the password.
            if doc.exists:
                if check_account(ref):
                    choice_2 = None
                    # as long as they don't want to quit, continue.
                    while choice_2 != "7":
                        print("1) Display recipe")
                        print("2) Add recipe")
                        print("3) Update recipe")
                        print("4) Delete recipe")
                        print("5) Delete account")
                        print("6) Edit account")
                        print("7) Quit")
                        choice_2 = input("> ")
                        print()
                        # This is pretty straightforward.
                        if choice_2 == "1":
                            display_recipe(ref)

                        elif choice_2 == "2":
                            add_recipe(ref)

                        elif choice_2 == "3":
                            update_recipe(ref)

                        elif choice_2 == "4":
                            delete_recipe(ref)

                        elif choice_2 == "5":
                            delete_account(ref)
                            return
                        
                        elif choice_2 == "6":
                            edit_account(ref)
                            
                        elif choice_2 == "7":
                            return

                    else: 
                        print("invalid choice. try again.")
                else: 
                    print("invalid password.")
            else:
                print('ERROR! Account not found!')
                print()
        elif choice_1 == 'q':
            return
        else: 
            print("That's not an option.")
            print()

if __name__ == "__main__":
    main()