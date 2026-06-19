from database import get_db, next_id


def _col():
    return get_db()["accounts"]


def _print_account(a):
    print(f"  ID      : {a['_id']}")
    print(f"  IBAN    : {a.get('accountIban', '')}")
    print(f"  Balance : {a.get('balance', 0):,.2f}")
    print(f"  Client  : {a.get('clientId', '')}")


def create_account():
    print("\n** Créer un compte **")
    client_id = input("ID du client : ").strip()
    if not get_db()["clients"].find_one({"_id": client_id}):
        print("Client introuvable.")
        return
    iban = input("IBAN : ").strip()
    if not iban:
        print("L'IBAN est obligatoire.")
        return
    balance_input = input("Solde initial (0 par défaut) : ").strip() or "0"
    try:
        balance = float(balance_input)
    except ValueError:
        print("Solde invalide.")
        return
    aid = next_id("accounts", "CPT")
    account = {"_id": aid, "accountIban": iban, "balance": balance, "clientId": client_id}
    _col().insert_one(account)
    print("*** Compte créé avec succès. ***")
    _print_account(account)


def view_account():
    print("\n** Consulter un compte **")
    aid = input("ID du compte : ").strip()
    account = _col().find_one({"_id": aid})
    if not account:
        print("Compte introuvable.")
        return
    print()
    _print_account(account)


def edit_account():
    print("\n** Modifier un compte **")
    aid = input("ID du compte : ").strip()
    account = _col().find_one({"_id": aid})
    if not account:
        print("Compte introuvable.")
        return
    print("Laissez vide pour conserver la valeur actuelle.")
    iban = input(f"IBAN [{account['accountIban']}] : ").strip() or account["accountIban"]
    client_id = input(f"ID client [{account['clientId']}] : ").strip() or account["clientId"]
    if client_id != account["clientId"] and not get_db()["clients"].find_one({"_id": client_id}):
        print("Client introuvable.")
        return
    updated = {"accountIban": iban, "clientId": client_id}
    _col().update_one({"_id": aid}, {"$set": updated})
    print("*** Compte mis à jour avec succès. ***")
    updated["_id"] = aid
    updated["balance"] = account["balance"]
    _print_account(updated)


def delete_account():
    print("\n** Supprimer un compte **")
    aid = input("ID du compte : ").strip()
    account = _col().find_one({"_id": aid})
    if not account:
        print("Compte introuvable.")
        return
    ops = get_db()["transactions"].count_documents({
        "$or": [{"sourceAccountId": aid}, {"receiverAccountId": aid}]
    })
    if ops:
        print(f"Attention : ce compte a {ops} transaction(s) associée(s).")
        confirm = input("Supprimer quand même ? (oui/non) : ").strip().lower()
        if confirm != "oui":
            print("Annulé.")
            return
    _col().delete_one({"_id": aid})
    print("*** Compte supprimé. ***")
    _print_account(account)


def list_accounts():
    print("\n** Liste des comptes **")
    accounts = list(_col().find().sort("_id", 1))
    if not accounts:
        print("Aucun compte enregistré.")
        return
    print(f"{'ID':<8} {'IBAN':<38} {'Balance':>12} Client")
    print("-" * 70)
    for a in accounts:
        print(f"{a['_id']:<8} {a.get('accountIban',''):<38} {a.get('balance', 0):>12,.2f} {a.get('clientId','')}")


def menu():
    options = {
        "1": ("Créer un compte", create_account),
        "2": ("Consulter un compte", view_account),
        "3": ("Modifier un compte", edit_account),
        "4": ("Supprimer un compte", delete_account),
        "5": ("Lister les comptes", list_accounts),
        "0": ("Retour", None),
    }
    while True:
        print("\n*** Gestion des comptes ***")
        for k, (label, _) in options.items():
            print(f"  {k}. {label}")
        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix in options and options[choix][1]:
            options[choix][1]()
        else:
            print("Choix invalide.")