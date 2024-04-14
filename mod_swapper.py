import os
from tkinter import Tk, filedialog, messagebox
import shutil
import configparser
import yaml

version = "1.0.6"
supported_language_versions = ["1.0.5"]
forbidden_names = ["0"]
GITHUB = "https://github.com/Navee82/Minecraft-mod-swapper"

# Créer un objet ConfigParser
config = configparser.ConfigParser()

def update(old_version):
    match old_version:
        case "1.0.3":
            config["Settings"]["transfer_detail"] = False
            config["General"]["version"] = "1.0.4"
        
        case "1.0.4":
            config["Settings"]["language"] = None
            config["General"]["version"] = "1.0.5"
        
        case "1.0.5":
            config["General"]["version"] = "1.0.6"

    with open('config.ini', "r+") as configfile:
        config.write(configfile)
    

def message(message_id, *value):
    if message_id in LANGUAGE:
        message = LANGUAGE[message_id]
        if value:
            for i in range (len(value)):
                # Trouver l'index du premier % et du dernier % dans la chaîne
                idx_first = message.find('%')-1
                idx_last = message.find('%', idx_first + 2)+1

                # Extraire le texte entre les deux %
                placeholder = message[idx_first + 1: idx_last]

                message = message.replace(placeholder, str(value[i]))
    else:
        message = f"Error : message id '{message_id}' does not exists in message file"
    return message

def check_for_config():
    config_path = "config.ini"
    if os.path.exists(config_path):
        return True
    return False

def check_language():
    '''
    Fonction qui renvoie un bool après une série de tests sur la validité du fichier de langue
    '''
    check = True
    if LANGUAGE["language_version"] not in supported_language_versions:
        check = False
    return check

def generate_config():

    # Définition des paramètres

    config['General'] = {
    'version': version,
    'GAME_FOLDER_PATH': None,
    'loaded_profile': None
    }

    config['Settings'] = {
        'language': None,
        'transfer_details': True
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
    Exemple param = [(General,GAME_FOLDER_PATH,C:/user/.minecraft),(General,loaded_profile,fabric 1.18.2),(PROFILES,server,C:/user/...)]
    '''
    # Définition des paramètres
    try :
        for category, key, value in param:

            if not category in config:
                messagebox.showerror(title=message("messagebox_title_error"), message=f"La catégorie {category} est inexistante", icon="error", type="ok")
            else:
                if key in config[category]:
                    config[category][key] = value
                else:
                    print(category)
                    if category == "Profiles":
                        config[category][key] = value
                    else:
                        messagebox.showerror(title=message("messagebox_title_error"), message=f"La clé {key} est inexistante", icon="error", type="ok")
        
        # Écriture du fichier pour les données à ajouter
        with open('config.ini', "r+") as configfile:
            config.write(configfile)

        # Écriture du ficher pour les données à supprimer
        for profile_name in config["Profiles"].keys():
            if not profile_name in PROFILES:
                del config['Profiles'][profile_name]
        
        with open('config.ini', "w") as configfile:
            config.write(configfile)

        print(message("saved_config"))

    except Exception as e :
        messagebox.showerror(title=message("messagebox_title_error"), message=message("saving_error_full"), icon="error", type="ok")
        print(message("saving_error"))
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
    Cette fonction renvoie la liste PROFILES modifiée
    Entrée : le dictionnaire des profiles, peu importe la longueur
    Sortie : Les profils avec des dossiers inexistants enlevés du dictionnaire si l'utilisateur valide; Les caractères \\ changés en "/".
    '''

    profiles_to_delete = []

    for name,path in profiles.items():
        print(path)
        path = path.replace("\\","/")
        if not os.path.exists(path):
            if confirmation(titre=message("messagebox_title_error"),message=message("profile_not_existing",name,path)):
                profiles_to_delete.append(name)

    for name in profiles_to_delete:
        del profiles[name]

    return profiles


def create_profile(profiles,name):
    print(message("creating_profile"))
    if not name in profiles:
        try:
            current_dir = os.getcwd()
            path = os.path.join(current_dir, name)

            path = path.replace("\\", "/")

            os.mkdir(path)
            profiles[name] = path

            print(message("created_profile"))
            return profiles
        
        except Exception as e:
            print(message("creating_profile_error"))
            print(e)

    else:
        print(message("profile_already_exists"))


def delete_profile(to_delete):
    current_dir = os.getcwd()
    path = os.path.join(current_dir, to_delete)

    path = path.replace("\\", "/")

    shutil.rmtree(path)

    del PROFILES[to_delete]

    return PROFILES


def rename_profile(old_name,new_name):
    old_path = PROFILES[old_name]
    new_path = os.getcwd() + f"/{new_name}"

    new_path = new_path.replace("\\", "/")

    os.rename(old_path,new_path)

    del PROFILES[old_name]
    PROFILES[new_name] = new_path

    return PROFILES






def openfolder(window_title):
    '''
    Cette fonction renvoie un path de dossier
    Entrée un string (de préférence) qui servira de titre à la fenêtre ouverte
    '''
    folderpath = filedialog.askdirectory(title = window_title)
    return folderpath

def openfile(window_title):
    '''
    même chose que openfolder mais avec un fichier
    '''
    filepath = filedialog.askopenfilename(title = window_title)
    return filepath


def ask_game_folder():
    game_folder = openfolder(message("ask_game_folder_window_title"))
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
            print(f"\n   {message("main_console_title")}\n")
            print(f" 1) {message("option_swap_profiles")}")
            print(f" 2) {message("option_manage_profiles")}")
            print(f" 3) {message("option_settings")}")
            print(f" 4) {message("option_save")}")
            print(f" 0) {message("option_quit")}")

        case "profiles":
            print(f"\n {message("profiles_list_title")}")
            print(f"{message("profile_list_subtitle")}\n")
            if len(PROFILES) == 0:
                print(message("no_existing_profiles"))
            else:
                for name, path in PROFILES.items():
                    print(f" {name} -> {path}")
            print(f"\n {message("active_profile", loaded_profile)}")
            print("\n ----------------------------------\n")
        
        case "profils_swap":
            print(message("profile_to_swap"))
            print(message("type_to_main"))

        case "profils_gestion":
            
            print(f" 1) {message("create_profile")}")
            print(f" 2) {message("rename_profile")}")
            print(f" 3) {message("delete_profile")}")
            print(f" 4) {message("verify_profiles")}")
            print(f"\n 0) {message("back_to_main")}")
        
        case "settings":
            print(f"\n       {message("settings_title")}\n")
            print(f" 1) {message("reset_settings")}")
            print(f" 2) {message("change_minecraft_folder")}")
            print(f" 3) {message("transfer_details")}")
            print(f"\n 0) {message("back_to_main")}")
        



def swapmods(old,new,folder):
    '''
    Cette fonction inverse les contenus de deux profils de mods en plusieurs étapes:
        - Enlève les mods déja présent dans le dossier "mods pour les stocker dans le dossier du profil     <- permet de modifier le contenu d'un profil en ajoutant le mod dans le dossier "mods" directementS
        - Transfère les mods du nouveau profil vers le dossier "mods"

    Entrée : "old" et "new" deux variables contenant les chemins respectifs des dossiers des profils
            "folder" le chemin du dossier "mods
    '''

    if not old == "None":
        transfered_mods = 0
        try:
            # Copie de chaque fichier du dossier mods dans le dossier du profil actuel
            print(f"\n{message("swapping_mods_to_old",old)}")
            for contenu in os.listdir(folder):
                new_path = os.path.join(old, contenu)
                file_path = os.path.join(folder, contenu)
                if os.path.isfile(file_path):
                    shutil.copy(file_path, new_path)

                    if TRANSFER_DETAIL == True:
                        print(f"{message("transfered_mod_fancy",contenu)}")
                    transfered_mods += 1

                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    print(f"{message("ignored_folder",contenu)}")

            if TRANSFER_DETAIL == True:
                print(f"{message("mods_folder_transfered")}")
            else:
                print(f"{message("transfered_mod_light",transfered_mods)}")

        except Exception as e:
            print(f"{message("copy_error",e)}")

    transfered_mods = 0
    try:
        # Copie de chaque fichier du dossier du nouveau profil dans le dossier mods
        print(f"\n{message("swapping_new_to_mods",new)}")
        for contenu in os.listdir(new):
            new_path = os.path.join(folder, contenu)
            file_path = os.path.join(new, contenu)
            if os.path.isfile(file_path):
                shutil.copy(file_path, new_path)
                
                if TRANSFER_DETAIL == True:
                    print(f"{message("transfered_mod_fancy",contenu)}")
                transfered_mods += 1

                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f"{message("ignored_folder",contenu)}")
               
        if TRANSFER_DETAIL == True:
            print(f"{message("new_folder_transfered",new)}")
        else:
            print(f"{message("transfered_mod_light",transfered_mods)}")

    except Exception as e:
        print(f"{message("copy_error",e)}")





################################################
# __  __       _          ____          _      #
#|  \/  | __ _(_)_ __    / ___|___   __| | ___ #
#| |\/| |/ _` | | '_ \  | |   / _ \ / _` |/ _ \#
#| |  | | (_| | | | | | | |__| (_) | (_| |  __/#
#|_|  |_|\__,_|_|_| |_|  \____\___/ \__,_|\___|#
################################################


# Check de la config
if check_for_config() == False:
    print(" Unable to find a configuration file ! \nCreating the file : 'config.ini'")
    generate_config()
    print(" Successfully created the config file !")
else:
    print(" Found the config file ! \nRecovering data...")

# Lecture du fichier de config
config.read('config.ini')

# Auto updater
print(" Checking for updates...")
while config["General"]["version"] != version:
    config.read('config.ini')
    update(config["General"]["version"])
print(" Program is up to date !")


# Récupération de la langue

language_path = config["Settings"]["language"]

language = True
while language:
    asking_file = True
    while asking_file:
        if not os.path.exists(language_path):
            language_path = openfile("Please select your langage file")

            if not language_path:
                print(f" You need a language file to run this program please select one or download it from the GitHub page :\n {GITHUB}")
                input("")
        else:
            asking_file = False

    with open(language_path, "r") as file:
        LANGUAGE = yaml.safe_load(file)

    checking_file = True
    while checking_file:
        if check_language() == False:
            print(f" Your langage file is not correct (probably not up to date) please download a correct one on the GitHub page :\n {GITHUB}")
            input("")
        else:
            language = False

        checking_file = False


    
# Assignations des variables

try :
    GAME_FOLDER_PATH = config["General"]["GAME_FOLDER_PATH"]
    loaded_profile = config["General"]["loaded_profile"]
    TRANSFER_DETAIL = config["Settings"]["transfer_detail"]

    PROFILES = {name: path for name, path in config["Profiles"].items()}
except Exception as e:
    messagebox.showerror(title=message("messagebox_title_error"), message=message("retrieving_data_error",e), icon="error", type="ok")
    

# Check des valeurs de la config

if GAME_FOLDER_PATH == "None":
    print(message("minecraft_folder_not_defined"))
    messagebox.showinfo(title=message("messagebox_title_info"),message=message("select_minecraft_folder"),type="ok")
    
    GAME_FOLDER_PATH = ask_game_folder()

while not os.path.exists(GAME_FOLDER_PATH+"/mods"):
    if confirmation(message("messagebox_title_error"),f"{message("minecraft_folder_not_existing",GAME_FOLDER_PATH)}"):
        GAME_FOLDER_PATH = ask_game_folder()
    else:
        break


# Menu de navigation
running = True
clear()
ui_show("main")

# print(PROFILES)

while running == True:
    user_input = input(" Input -> ")

    match user_input:
        case "1":
            # SWAP DES PROFILS
            profils_swap = True
            clear()
            print(f"\n   {message("profile_swap_title")}")
            ui_show("profiles")
            ui_show("profils_swap")



            while profils_swap:

                to_swap = input(" Input ->")
                if to_swap == "0":
                    profils_swap = False
                    clear()
                    ui_show("main")

                elif to_swap not in PROFILES:
                    print(message("profile_to_swap_not_existing"))
                elif to_swap == loaded_profile:
                    print(message("profile_already_active"))
                else:
                    if not loaded_profile == "None":
                        old_path = PROFILES[loaded_profile]
                    else: old_path = "None"
                    new_path = PROFILES[to_swap]
                    mods_path = GAME_FOLDER_PATH+"/mods"

                    swapmods(old_path,new_path,mods_path)

                    loaded_profile = to_swap

                    config["General"]["loaded_profile"] = loaded_profile

                    with open('config.ini', "r+") as configfile:
                        config.write(configfile)
                    


        case "2":
            # GESTION DES PROFILS
            profils_gestion = True

            clear()
            print(f"\n   {message("profiles_gestion_title")}")
            ui_show("profiles")
            ui_show("profils_gestion")

            while profils_gestion :

                user_input = input(" Input -> ")

                match user_input:
                    case "1":
                        # Création de profil

                        profil_name = input(message("profile_naming"))
                        if profil_name in PROFILES:
                            print(message("profile_already_exists"))
                        elif profil_name in forbidden_names:
                            print(message("forbidden_naming"))
                        else:
                            PROFILES = create_profile(PROFILES,profil_name)


                    case "2":
                        # Renommer un profil
                        to_rename = input(message("profile_to_rename"))
                        new_name = input(" Comment souhaitez vous le renommer : ")

                        if to_rename not in PROFILES:
                            print(message("profile_to_rename_not_existing"))
                        elif new_name in PROFILES:
                            print(message("profile_already_exists"))
                        elif new_name in forbidden_names:
                            print(message("forbidden_naming"))
                        else:
                            PROFILES = rename_profile(to_rename,new_name)
                            print(message("successful_renaming",to_rename,new_name))
                            if loaded_profile == to_rename:
                                loaded_profile = new_name

                    case "3":
                        # Suppression de profils

                        to_delete = input(message("profile_to_delete"))

                        if to_delete not in PROFILES:
                            print(message("profile_to_delete_not_existing"))
                        elif to_delete == loaded_profile:
                            print(message("profile_to_delete_active"))
                
                        else:
                            PROFILES = delete_profile(to_delete)
                            print(message("profile_deleted",to_delete))

                    case "4":
                        # Vérification des profils (ne vérifie que config -> dossiers, à approfondir)

                        print(message("checking_profiles"))
                        PROFILES = check_profiles(PROFILES)
                        if loaded_profile not in PROFILES:
                            loaded_profile = "None"
                        print(message("checked_profiles"))
                    case "0":
                        profils_gestion = False
                        clear()
                        ui_show("main")
                    case _:
                        print(message("choose_existing_option"))
                    
        case "3":
            # PARAMETRES
            clear()
            ui_show("settings")

            settings = True

            while settings:
                user_input = input(" Input ->")

                match user_input:

                    case "1":
                        # Reinitialisation complète

                        if confirmation(titre=message("messagebox_title_confirm"),message=message("messagebox_message_reset")):
                            for value in PROFILES.keys():
                                delete_profile(value)

                            config_path = "config.ini"
                            os.remove(config_path)
                    
                    case "2":
                        ask_game_folder()
                    
                    case "3":
                        TRANSFER_DETAIL = confirmation(titre=message("messagebox_title_details"),message=message("messagebox_message_details"))

                    case "0":
                        settings = False
                        clear()
                        ui_show("main")
                    case _:
                        print(message("choose_existing_option"))


        case "4":
            # SAUVEGARDE DU PROGRAMME
            print(message("saving_program"))

            config_values = [
            ("General", "version", str(version)),
            ("General", "GAME_FOLDER_PATH", GAME_FOLDER_PATH),
            ("General", "loaded_profile", loaded_profile),
            ("Settings", "transfer_detail", str(TRANSFER_DETAIL)),
            ("Settings", "language", language_path)
            ]

            # Ajout des valeurs des profiles au format requis
            for profile_name, profile_path in PROFILES.items():
                config_values.append(("Profiles", profile_name, profile_path))

            save_config(config_values)
            
        case "0":
            if confirmation(titre=message("messagebox_title_confirm"),message=message("quit_program")):
                running = False
        case "debug":
            print(f"version= {version}")
            print(f"GAME_FOLDER_PATH= {GAME_FOLDER_PATH}")
            print(f"loaded_profile= {loaded_profile}")
            print(type(loaded_profile))
            print(f"transfer_detail= {TRANSFER_DETAIL}")

            print(f"\nProfiles dictionnary\n{PROFILES}")
        case _:
            print(message("choose_existing_option"))