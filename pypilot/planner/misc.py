import os


def clear():
    if os.environ.get("TERM") is None:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n########################################")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
