from database import get_db, next_id


def _col():
    return get_db()["clients"]


def _print_client(c):
    print(f"  ID       : {c['_id']}")
    print(f"  Prénom   : {c.get('firstName', '')}")
    print(f"  Nom      : {c.get('lastName', '')}")
    print(f"  Email    : {c.get('email', '')}")


def create_client():
    print("\n-- Créer un client --")
    first = input("Prénom : ").strip()
    last = input("Nom    : ").strip()
    email = input("Email  : ").strip()
    if not (first and last and email):
        print("Tous les champs sont obligatoires.")
        return
    cid = next_id("clients", "CLI")
    client = {"_id": cid, "firstName": first, "lastName": last, "email": email}
    _col().insert_one(client)
    print("*** Client crée avec succès. ***")
    _print_client(client)


def search_client():
    pass


def edit_client():
    print("\n-- Modifier un client --")
    cid = input("ID du client : ").strip()
    client = _col().find_one({"_id": cid})
    if not client:
        print("Client introuvable.")
        return
    print("Laissez vide pour conserver la valeur actuelle.")
    first = input(f"Prénom [{client['firstName']}] : ").strip() or client["firstName"]
    last = input(f"Nom    [{client['lastName']}] : ").strip() or client["lastName"]
    email = input(f"Email  [{client['email']}] : ").strip() or client["email"]
    client = {"firstName": first, "lastName": last, "email": email}
    _col().update_one({"_id": cid}, {"$set": client})
    print("*** Client mis à jour avec succès. ***")
    client["_id"] = cid
    _print_client(client)

def menu():
    options = {
        "1": ("Créer un client", create_client),
        "2": ("Éditer un client", edit_client),
        "3": ("Rechercher un client", search_client),
        "0": ("Retour", None),
    }
    while True:
        print("\n*** Gestion des clients ***")
        for k, (label, _) in options.items():
            print(f"  {k}. {label}")
        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix in options and options[choix][1]:
            options[choix][1]()
        else:
            print("Choix invalide.")
