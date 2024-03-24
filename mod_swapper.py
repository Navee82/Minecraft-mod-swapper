import os
from tkinter import Tk, filedialog, messagebox
import shutil
import configparser

version = 1.0.1
forbidden_names =["EXIT"]

# Créer un objet ConfigParser
config = configparser.ConfigParser()


def check_for_config():
    config_path = "config.ini"
    if os.path.exists(config_path):
        return True
    return False


def generate_config():

    # Définition des paramètres

    config['General'] = {
    'version': version,
    'game_folder_path': "None",
    'loaded_profile': "None"
    }

    config['Profiles'] = {}    


    # Création du fichier
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("config generated")



def save_config(param):
    '''
    Cette fonction va écraser les valeurs des clés déjà présentes dans le fichier de configuration
    Entrée : une liste de tuples contenant toutes les catégories, les paramètres à modifier et leurs valeurs respectives
    Exemple param = [(General,game_folder_path,C:/user/.minecraft),(General,loaded_profile,fabric 1.18.2),(Profiles,server,C:/user/...)]
    '''
    # Définition des paramètres
    try :
        for category, key, value in param:

            if not category in config:
                messagebox.showerror(title="Erreur", message=f"La catégorie {category} est inexistante", icon="error", type="ok")
            else:
                if key in config[category]:
                    config[category][key] = value
                else:
                    print(category)
                    if category == "Profiles":
                        config[category][key] = value
                    else:
                        messagebox.showerror(title="Erreur", message=f"La clé {key} est inexistante", icon="error", type="ok")
        
        # Écriture du fichier pour les données à ajouter
        with open('config.ini', "r+") as configfile:
            config.write(configfile)

        # Écriture du ficher pour les données à supprimer
        for profile_name in config["Profiles"].keys():
            if not profile_name in profiles:
                del config['Profiles'][profile_name]
        
        with open('config.ini', "w") as configfile:
            config.write(configfile)

        print(" config sauvegardée !")

    except Exception as e :
        messagebox.showerror(title="Erreur", message="Une erreur s'est produite lors de la sauvegarde des données.\nSi le problème persiste veuillez contacter le créateur de ce logiciel", icon="error", type="ok")
        print(" Erreur lors de la sauvegarde :")
        print(e)



def directory_empty(directory):
    # Liste des fichiers et dossiers dans le répertoire
    files = os.listdir(directory)
    # Vérifier si la liste est vide
    if len(files) == 0:
        return True
    else:
        return False


def clear():
    os.system('cls')


def check_profiles(profiles):
    '''
    Cette fonction renvoie la liste profiles modifiée
    Entreée : le dictionnaire des profiles, peu importe la longueur
    Sortie : Les profils avec des dossiers inexistants enlevés du dictionnaire si l'utilisateur valide.
    '''

    profiles_to_delete = []

    for name,path in profiles.items():
        if not os.path.exists(path):
            if confirmation("erreur",f"Il semble que le profil {name} -> {path} n'existe pas sur votre ordinateur.\nVoulez vous le supprimer de la liste des profils ?"):
                profiles_to_delete.append(name)

    for name in profiles_to_delete:
        del profiles[name]

    return profiles

def create_profile(profiles,name):
    print(" Création du profil...")
    if not name in profiles:
        try:
            path = os.getcwd() + f"/{name}"

            os.mkdir(path)
            profiles[name] = path

            print(" Profil créé")
            return profiles
        
        except Exception as e:
            print(" Erreur lors de la création du profil !")
            print(e)

    else:
        print(" Ce profil existe déjà !")


def delete_profile(to_delete):
    path = os.getcwd() + f"/{to_delete}"

    shutil.rmtree(path)

    del profiles[to_delete]

    return profiles


def rename_profile(old_name,new_name):
    old_path = profiles[old_name]
    new_path = os.getcwd() + f"/{new_name}"
    os.rename(old_path,new_path)

    del profiles[old_name]
    profiles[new_name] = new_path

    return profiles






def openfolder(window_title):
    '''
    Cette fonction renvoie un path de dossier
    Entrée un string (de préférence) qui servira de titre à la fenêtre ouverte
    '''
    folderpath = filedialog.askdirectory(title = window_title)
    return folderpath


def ask_game_folder():
    game_folder = openfolder("Choisir votre dossier .minecraft")
    return game_folder

def confirmation(titre,message):

    parent = Tk()
    parent.withdraw()  # Cacher la fenêtre parente principale
    parent.lift()

    confirmation = messagebox.askyesno(titre, message, parent=parent)

    parent.destroy()  # Détruire la fenêtre parente après utilisation

    return confirmation

def ui_show(ui):
    match ui:
        
        case "main" :
            print("\n   MAIN CONSOLE\n")
            print(" 1)   Changer les profils")
            print(" 2)   Gérer les profils")
            print(" 3)   Paramètres")
            print(" 4)   Sauvegarder")
            print(" 0)   Quitter le programme")

        case "profiles":
            print("\n Liste des profils :")
            print(" Nom -> Chemin\n")
            if len(profiles) == 0:
                print(" Il n'y a actuellement aucun profil de créé.")
            else:
                for name, path in profiles.items():
                    print(f" {name} -> {path}")
            print(f"\n Profil actif : {loaded_profile}")
            print("\n ----------------------------------\n")
        
        case "profils_swap":
            print(" Quel profil souhaitez vous activer ?")
            print(" Pour revenir à la console principale tapez 'EXIT'")

        case "profils_gestion":
            
            print(" 1) Créer un profil")
            print(" 2) Renommer un profil")
            print(" 3) Supprimer un profil")
            print(" 4) Vérifier les profils")
            print("\n 0) Retour à la console principale")
        



def swapmods(old,new,folder):
    '''
    Cette fonction inverse les contenus de deux profils de mods en plusieurs étapes:
        - Enlève les mods déja présent dans le dossier "mods pour les stocker dans le dossier du profil     <- permet de modifier le contenu d'un profil en ajoutant le mod dans le dossier "mods" directementS
        - Transfère les mods du nouveau profil vers le dossier "mods"

    Entrée : "old" et "new" deux variables contenant les chemins respectifs des dossiers des profils
            "folder" le chemin du dossier "mods
    '''

    if not old == "None":
        try:
            # Copie de chaque fichier du dossier mods dans le dossier du profil actuel
            for contenu in os.listdir(folder):
                new_path = os.path.join(old, contenu)
                file_path = os.path.join(folder, contenu)
                if os.path.isfile(file_path):
                    shutil.copy(file_path, new_path)
                    print(f" MOD : {contenu} transféré avec succès.")
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    print(f" Ignoré le dossier {contenu}.")
            print(f" \nContenu du dossier mod transféré avec succès dans le dossier {old}.")
        except Exception as e:
            print(f" Erreur lors de la copie du contenu du dossier : {e}")

    try:
        # Copie de chaque fichier du dossier du nouveau profil dans le dossier mods
        for contenu in os.listdir(new):
            new_path = os.path.join(folder, contenu)
            file_path = os.path.join(new, contenu)
            if os.path.isfile(file_path):
                shutil.copy(file_path, new_path)
                print(f" MOD : {contenu} transféré avec succès.")
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f" Ignoré le dossier {contenu}.")
        print(f" Contenu du dossier {new} transféré avec succès dans le dossier mods.")
    except Exception as e:
        print(f" Erreur lors de la copie du contenu du dossier : {e}")



################################################
# __  __       _          ____          _      #
#|  \/  | __ _(_)_ __    / ___|___   __| | ___ #
#| |\/| |/ _` | | '_ \  | |   / _ \ / _` |/ _ \#
#| |  | | (_| | | | | | | |__| (_) | (_| |  __/#
#|_|  |_|\__,_|_|_| |_|  \____\___/ \__,_|\___|#
################################################


# Check de la config
if check_for_config() == False:
    print("Fichier de configuration introuvable ! \nCréation d'un fichier 'config.ini'")
    generate_config()
    print("Fichier créé avec succès !")
else:
    print("fichier de configuration trouvé ! \nRécupération des données...")


config.read('config.ini')
# Assignations des variables

try :
    game_folder_path = config["General"]["game_folder_path"]
    loaded_profile = config["General"]["loaded_profile"]

    profiles = {name: path for name, path in config["Profiles"].items()}
except Exception as e:
    messagebox.showerror(title="Erreur", message=f"Erreur lors de la récupération des données de {e}", icon="error", type="ok")
    

# Check des valeurs de la config

if game_folder_path == "None":
    print(" Il semblerais que vous n'ayez pas encore définit votre emplacement de dossier .minecraft")
    messagebox.showinfo(title="Info",message="Veuillez choisir votre dossier  .minecraft",type="ok")
    
    game_folder_path = ask_game_folder()

while not os.path.exists(game_folder_path+"/mods"):
    if confirmation("Erreur",f"il semble que le dossier de mods : {game_folder_path} n'existe pas\nVoulez vous le modifier ?"):
        game_folder_path = ask_game_folder()
    else:
        break




# Menu de navigation
running = True
clear()
ui_show("main")

# print(profiles)

while running == True:
    user_input = input(" Input -> ")

    match user_input:
        case "1":
            # SWAP DES PROFILS
            profils_swap = True
            clear()
            print("\n   ÉCHANGE DES PROFILS")
            ui_show("profiles")
            ui_show("profils_swap")



            while profils_swap:

                to_swap = input(" Input ->")
                if to_swap == "EXIT":
                    profils_swap = False
                    clear()
                    ui_show("main")

                elif to_swap not in profiles:
                    print(" Le profil que vous souhaitez activer n'existe pas !")
                elif to_swap == loaded_profile:
                    print(" Le profil est déja actif !")
                else:
                    if not loaded_profile == "None":
                        old_path = profiles[loaded_profile]
                    else: old_path = "None"
                    new_path = profiles[to_swap]
                    mods_path = game_folder_path+"/mods"

                    swapmods(old_path,new_path,mods_path)

                    loaded_profile = to_swap

                    config["General"]["loaded_profile"] = loaded_profile

                    with open('config.ini', "r+") as configfile:
                        config.write(configfile)
                    


        case "2":
            # GESTION DES PROFILS
            profils_gestion = True

            clear()
            print("\n   GESTION DES PROFILS")
            ui_show("profiles")
            ui_show("profils_gestion")
            # print(profiles)

            while profils_gestion :

                user_input = input(" Input -> ")

                match user_input:
                    case "1":
                        # Création de profil

                        profil_name = input(" Comment voulez-vous appeller votre profil : ")
                        if profil_name in profiles:
                            print(" Ce profil existe déjà")
                        elif profil_name in forbidden_names:
                            print(" Vous ne pouvez pas appeler votre profil comme cela !")
                        else:
                            profiles = create_profile(profiles,profil_name)


                    case "2":
                        # Renommer un profil
                        to_rename = input(" Quel profil souhaitez vous renommer : ")
                        new_name = input(" Comment souhaitez vous le renommer : ")

                        if to_rename not in profiles:
                            print(" Le profil que vous souhaitez renommer n'existe pas !")
                        elif new_name in profiles:
                            print(" Le nouveau nom de profil existe déjà !")
                        elif new_name in forbidden_names:
                            print(" Vous ne pouvez pas appeler votre profil comme cela !")
                        else:
                            profiles = rename_profile(to_rename,new_name)
                            print(f" Le profil {to_rename} a bien été renommé en {new_name}")
                            if loaded_profile == to_rename:
                                loaded_profile = new_name

                    case "3":
                        # Suppression de profils

                        to_delete = input(" Quel profil souhaitez vous supprimer : ")

                        if to_delete not in profiles:
                            print(" Le profil que vous shouhaitez supprimer n'existe pas.")
                        elif to_delete == loaded_profile:
                            print(" Vous ne pouvez pas supprimer le profil actif !")
                
                        else:
                            profiles = delete_profile(to_delete)
                            print(f" Le profil {to_delete} a bien été supprimé !")

                    case "4":
                        # Vérification des profils (ne vérifie que config -> dossiers, à approfondir)

                        print("\n Vérification des profils...")
                        profiles = check_profiles(profiles)
                        if loaded_profile not in profiles:
                            loaded_profile = "None"
                        print(" Profils vérifiés !")
                    case "0":
                        profils_gestion = False
                        clear()
                        ui_show("main")
                    case _:
                        print(" Veuillez choisir une option existante.")
                    
        case "3":
            # PARAMETRES
            print(" Cette fonction n'est pas encore disponnible (à venir)")
        case "4":
            # SAUVEGARDE DU PROGRAMME
            print(" Sauvegarde du programme...")

            config_values = [
            ("General", "version", str(version)),
            ("General", "game_folder_path", game_folder_path),
            ("General", "loaded_profile", loaded_profile)
            ]
            # Ajout des valeurs de profiles au format requis
            for profile_name, profile_path in profiles.items():
                config_values.append(("Profiles", profile_name, profile_path))

            save_config(config_values)
            
        case "0":
            if confirmation("Confirmation","Etes vous sûr de vouloir quitter le programme ?\nToute donnée non sauvegardée sera effacée !"):
                running = False
        case "debug":
            print(f"version= {version}")
            print(f"game_folder_path= {game_folder_path}")
            print(type(loaded_profile))
            print(f"loaded_profile= {loaded_profile}\n")
            print(profiles)
        case _:
            print(" Veuillez choisir une option existante.")


print("fin")

