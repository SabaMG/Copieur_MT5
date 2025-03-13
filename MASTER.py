import MetaTrader5 as mt5
import time
from datetime import datetime

# Détails de connexion à MetaTrader 5
login = 62528834            # Remplacer par votre numéro de compte
password = "xY54d!t4"    # Remplacer par votre mot de passe
server = "OANDATMS-MT5"     # Remplacer par le nom du serveur de votre courtier

# Initialiser MetaTrader 5
if not mt5.initialize():
    print("Échec de l'initialisation de MetaTrader5")
    quit()

# Connexion au compte MetaTrader 5
if not mt5.login(login, password, server=server):
    print(f"Connexion échouée. Erreur : {mt5.last_error()}")
    mt5.shutdown()
    quit()

print("Connexion réussie à MetaTrader 5")

# Afficher les informations de connexion
print(mt5.terminal_info())
print(mt5.version())

# Définir le seuil de chute de l'équité (en pourcentage)
equityDropThreshold = 0.0  # 1%

# Obtenir la balance initiale
account_info = mt5.account_info()
if account_info is None:
    print("Impossible d'obtenir les informations du compte. Erreur :", mt5.last_error())
    mt5.shutdown()
    quit()

initial_balance = account_info.balance

def should_copy_trades():
    """Vérifier si la chute de l'équité est supérieure au seuil."""
    current_equity = mt5.account_info().equity
    drop_percentage = ((initial_balance - current_equity) / initial_balance) * 100
    if drop_percentage >= equityDropThreshold:
        print(f"Chute de l'équité détectée: {drop_percentage:.2f}%")
        return True
    return False

def get_positions():
    """Obtenir les positions actuelles."""
    positions = mt5.positions_get()
    if positions is None:
        print("Aucune position ouverte.")
        return []
    return positions

def compare_positions(prev_positions, current_positions):
    """Comparer les positions précédentes et actuelles."""
    if len(prev_positions) != len(current_positions):
        return True
    for prev_pos, curr_pos in zip(prev_positions, current_positions):
        if (prev_pos.ticket != curr_pos.ticket or
            prev_pos.price_open != curr_pos.price_open or
            prev_pos.sl != curr_pos.sl or
            prev_pos.tp != curr_pos.tp or
            prev_pos.volume != curr_pos.volume):
            return True
    return False

def save_positions(positions):
    """Sauvegarder les positions dans un fichier CSV."""
    with open("TradeCopy.csv", "w") as file:
        for position in positions:
            file.write(f"{position.ticket},{position.symbol},{position.volume},{position.price_open},{position.sl},{position.tp}\n")
    print("Positions sauvegardées dans TradeCopy.csv")

# Boucle principale pour surveiller l'équité et copier les positions
previous_positions = []

while True:
    if should_copy_trades():
        current_positions = get_positions()

        if compare_positions(previous_positions, current_positions):
            save_positions(current_positions)

        previous_positions = current_positions
    
    # Attendre 1 seconde avant de vérifier à nouveau
    time.sleep(1)

# Fermer la connexion MetaTrader 5 après l'arrêt
mt5.shutdown()
