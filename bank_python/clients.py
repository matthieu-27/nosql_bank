from database import get_db, next_id


def _col():
    return get_db()["clients"]


def _print_client(c):
    print(f"  ID       : {c['_id']}")
    print(f"  Prénom   : {c.get('firstName', '')}")
    print(f"  Nom      : {c.get('lastName', '')}")
    print(f"  Email    : {c.get('email', '')}")


def create_client():
    print("\n** Créer un client **")
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
    print("\n** Rechercher un client **")
    terme = input("ID, prénom ou nom : ").strip()
    results = list(_col().find({
        "$or": [
            {"_id": terme},
            {"firstName": {"$regex": terme, "$options": "i"}},
            {"lastName": {"$regex": terme, "$options": "i"}},
        ]
    }))
    if not results:
        print("Aucun client trouvé.")
        return
    for c in results:
        print()
        _print_client(c)


def edit_client():
    print("\n** Modifier un client **")
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


def list_clients():
    print("\n** Liste des clients **")
    clients = list(_col().find().sort("_id", 1))
    if not clients:
        print("Aucun client enregistré.")
        return
    print(f"{'ID':<8} {'Prénom':<15} {'Nom':<15} Email")
    print("-" * 60)
    for c in clients:
        print(f"{c['_id']:<8} {c.get('firstName',''):<15} {c.get('lastName',''):<15} {c.get('email','')}")

def delete_client():
    print("\n** Supprimer un client **")
    cid = input("ID du client : ").strip()
    client = _col().find_one({"_id": cid})
    if not client:
        print("Client introuvable.")
        return
    comptes = list(get_db()["accounts"].find({"clientId": cid}, {"_id": 1}))
    if comptes:
        ids = ", ".join(c["_id"] for c in comptes)
        print(f"Attention : ce client possède des comptes ({ids}).")
        confirm = input("Supprimer quand même ? (oui/non) : ").strip().lower()
        if confirm != "oui":
            print("Annulé.")
            return
    _col().delete_one({"_id": cid})
    print("Client supprimé. Adieu")
    client["_id"] = cid
    _print_client(client)



def menu():
    options = {
        "1": ("Créer un client", create_client),
        "2": ("Éditer un client", edit_client),
        "3": ("Supprimer un client", delete_client),
        "4": ("Rechercher un client", search_client),
        "5": ("Afficher les client", list_clients),
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
