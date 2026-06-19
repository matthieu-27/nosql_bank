from datetime import datetime
from database import get_db


def _col():
    return get_db()["transactions"]


def _print_transaction(t):
    date_str = t["date"].strftime("%d/%m/%Y %H:%M") if isinstance(t.get("date"), datetime) else str(t.get("date", ""))
    print(f"  ID      : {t['_id']}")
    print(f"  Type    : {t.get('type', '')}")
    print(f"  Amount  : {t.get('amount', 0):,.2f}")
    print(f"  Date    : {date_str}")
    print(f"  Source  : {t.get('sourceAccountId', '')}")
    if t.get("receiverAccountId"):
        print(f"  Receiver: {t.get('receiverAccountId')}")


# def menu():
#     options = {
#         "1": ("Effectuer un dépôt", deposit),
#         "2": ("Effectuer un retrait", withdrawal),
#         "3": ("Effectuer un virement", transfer),
#         "4": ("Historique des transactions", history),
#         "0": ("Retour", None),
#     }
#     while True:
#         print("\n*** Gestion des transactions ***")
#         for k, (label, _) in options.items():
#             print(f"  {k}. {label}")
#         choix = input("Votre choix : ").strip()
#         if choix == "0":
#             break
#         if choix in options and options[choix][1]:
#             options[choix][1]()
#         else:
#             print("Choix invalide.")
