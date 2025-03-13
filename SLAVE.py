import MetaTrader5 as mt5

# Déclaration des variables globales
filename = "TradeCopy"
LotCoeff = 0.1
ForceLot = 0.01
MicroLotBalance = 0
delay = 1000
PipsTolerance = 5
magic = 20111219
Prefix = ""
Suffix = ""
CopyDelayedTrades = False
IgnoreSLTP = False

# Détails de connexion à MetaTrader 5
login = 62765695            # Remplacer par votre numéro de compte
password = "!t2bEG*"    # Remplacer par votre mot de passe
server = "OANDATMS-MT5"     # Remplacer par le nom du serveur de votre courtier


# Fonction d'initialisation (OnInit équivalent en Python)
def on_init():
    global filename, LotCoeff, ForceLot, MicroLotBalance
    global delay, PipsTolerance, magic, Prefix, Suffix
    global CopyDelayedTrades, IgnoreSLTP

    # Initialisation des variables
    filename = "TradeCopy"
    LotCoeff = 0.1
    ForceLot = 0.01
    MicroLotBalance = 0
    delay = 1000
    PipsTolerance = 5
    magic = 20111219
    Prefix = ""
    Suffix = ""
    CopyDelayedTrades = False
    IgnoreSLTP = False

    # Connexion à MetaTrader 5
    if not mt5.initialize():
        print("Échec de l'initialisation de MetaTrader 5")
        return "INIT_FAILED"

    # Connexion au compte MetaTrader 5
    if not mt5.login(login, password, server=server):
        print(f"Connexion échouée. Erreur : {mt5.last_error()}")
        mt5.shutdown()
        return "LOGIN_FAILED"

    print("Connexion réussie à MetaTrader 5")
    return "INIT_SUCCEEDED"

# Appel de la fonction d'initialisation
status = on_init()
print(f"Initialisation status: {status}")

# Ne pas oublier de fermer la connexion à la fin de l'exécution du programme
if status == "INIT_SUCCEEDED":
    # Ici, vous pouvez ajouter vos opérations de trading avec mt5
    print("Prêt pour l'exécution des ordres...")
    
    # À la fin, fermez la connexion à MetaTrader 5
    mt5.shutdown()
