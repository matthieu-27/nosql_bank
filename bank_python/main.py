import sys


def main_menu():
    print("\n********************************")
    print("|         PYTHON  BANK         |")
    print("|******************************|")
    print("|  1. Clients menu             |")
    print("|  2. Accounts menu            |")
    print("|  3. Transaction menu         |")
    print("|  0. Exit                     |")
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
