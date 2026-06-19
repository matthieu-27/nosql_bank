from datetime import datetime, timezone
from database import get_db, next_id


def _col():
    return get_db()["transactions"]


def _print_transaction(t):
    date_str = t["date"].strftime("%d/%m/%Y %H:%M") if isinstance(t.get("date"), datetime) else str(t.get("date", ""))
    print(f"  ID      : {t['_id']}")
    print(f"  Type    : {t.get('type', '')}")
    print(f"  Montant  : {t.get('amount', 0):,.2f}")
    print(f"  Date    : {date_str}")
    print(f"  Source  : {t.get('sourceAccountId', '')}")
    if t.get("receiverAccountId"):
        print(f"  Destinataire: {t.get('receiverAccountId')}")


def deposit():
    print("\n** Effectuer un dépôt **")
    account_id = input("ID du compte : ").strip()
    account = get_db()["accounts"].find_one({"_id": account_id})
    if not account:
        print("Compte introuvable.")
        return
    try:
        amount = float(input("Montant : ").strip())
    except ValueError:
        print("Montant invalide.")
        return
    if amount <= 0:
        print("Le montant doit être positif.")
        return
    get_db()["accounts"].update_one({"_id": account_id}, {"$inc": {"balance": amount}})
    tid = next_id("transactions", "OPE")
    transaction = {
        "_id": tid,
        "amount": amount,
        "date": datetime.now(timezone.utc),
        "sourceAccountId": account_id,
        "type": "Deposit",
    }
    _col().insert_one(transaction)
    print("*** Dépôt effectué avec succès. ***")
    _print_transaction(transaction)
    print(f"  Nouveau solde : {account['balance'] + amount:,.2f}")


def withdrawal():
    print("\n** Effectuer un retrait **")
    account_id = input("ID du compte : ").strip()
    account = get_db()["accounts"].find_one({"_id": account_id})
    if not account:
        print("Compte introuvable.")
        return
    try:
        amount = float(input("Montant : ").strip())
    except ValueError:
        print("Montant invalide.")
        return
    if amount <= 0:
        print("Le montant doit être positif.")
        return
    if account["balance"] < amount:
        print(f"Solde insuffisant. Solde actuel : {account['balance']:,.2f}")
        return
    get_db()["accounts"].update_one({"_id": account_id}, {"$inc": {"balance": -amount}})
    tid = next_id("transactions", "OPE")
    transaction = {
        "_id": tid,
        "amount": amount,
        "date": datetime.now(timezone.utc),
        "sourceAccountId": account_id,
        "type": "Withdrawal",
    }
    _col().insert_one(transaction)
    print("*** Retrait effectué avec succès. ***")
    _print_transaction(transaction)
    print(f"  Nouveau solde : {account['balance'] - amount:,.2f}")


def transfer():
    print("\n** Effectuer un virement **")
    src_id = input("ID du compte source       : ").strip()
    dst_id = input("ID du compte destinataire : ").strip()
    if src_id == dst_id:
        print("Les comptes source et destinataire doivent être différents.")
        return
    src = get_db()["accounts"].find_one({"_id": src_id})
    dst = get_db()["accounts"].find_one({"_id": dst_id})
    if not src:
        print("Compte source introuvable.")
        return
    if not dst:
        print("Compte destinataire introuvable.")
        return
    try:
        amount = float(input("Montant : ").strip())
    except ValueError:
        print("Montant invalide.")
        return
    if amount <= 0:
        print("Le montant doit être positif.")
        return
    if src["balance"] < amount:
        print(f"Solde insuffisant. Solde compte source : {src['balance']:,.2f}")
        return
    get_db()["accounts"].update_one({"_id": src_id}, {"$inc": {"balance": -amount}})
    get_db()["accounts"].update_one({"_id": dst_id}, {"$inc": {"balance": amount}})
    tid = next_id("transactions", "OPE")
    transaction = {
        "_id": tid,
        "amount": amount,
        "date": datetime.now(timezone.utc),
        "sourceAccountId": src_id,
        "receiverAccountId": dst_id,
        "type": "Transfer",
    }
    _col().insert_one(transaction)
    print("*** Virement effectué avec succès. ***")
    _print_transaction(transaction)
    print(f"  Nouveau solde (compte source) : {src['balance'] - amount:,.2f}")


def history():
    print("\n** Historique des transactions **")
    account_id = input("ID du compte (vide = toutes) : ").strip()
    if account_id:
        if not get_db()["accounts"].find_one({"_id": account_id}):
            print("Compte introuvable.")
            return
        query = {"$or": [{"sourceAccountId": account_id}, {"receiverAccountId": account_id}]}
    else:
        query = {}
    transactions = list(_col().find(query).sort("date", 1))
    if not transactions:
        print("Aucune transaction trouvée.")
        return
    print(f"\n{'ID':<8} {'Type':<12} {'Amount':>12}  {'Date':<18} Source    Receiver")
    print("-" * 75)
    for t in transactions:
        _print_transaction(t)


def menu():
    options = {
        "1": ("Effectuer un dépôt", deposit),
        "2": ("Effectuer un retrait", withdrawal),
        "3": ("Effectuer un virement", transfer),
        "4": ("Historique des transactions", history),
        "0": ("Retour", None),
    }
    while True:
        print("\n*** Gestion des transactions ***")
        for k, (label, _) in options.items():
            print(f"  {k}. {label}")
        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix in options and options[choix][1]:
            options[choix][1]()
        else:
            print("Choix invalide.")
