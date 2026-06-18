import sys


def main_menu():
    print("\n********************************")
    print("|    GESTION BANCAIRE - MENU   |")
    print("|******************************|")
    print("|  1. Gestion des clients      |")
    print("|  2. Gestion des comptes      |")
    print("|  3. Gestion des opérations   |")
    print("|  0. Quitter                  |")
    print("********************************")
    return input("Votre choix : ").strip()


def main():
    print("Connexion à MongoDB Atlas...")
    try:
        from database import get_db
        get_db().command("ping")
        print("Connexion réussie.")
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        print("Vérifiez la configuration dans config.py")
        sys.exit(1)

    while True:
        main_menu()


if __name__ == "__main__":
    main()
