import pickle

with open("cklib1.pkl", "rb") as openfile:
    print(openfile)
    while True:
        try:
            print(pickle.load(openfile))
        except EOFError:
            break