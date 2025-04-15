import sys

if len(sys.argv) != 3:
    print("Erreur: Deux arguments sont nécessaires.")
    sys.exit(1)

try:
    arg1 = float(sys.argv[1])
    arg2 = float(sys.argv[2])
except ValueError:
    print("Erreur: Les arguments doivent être des nombres.")
    sys.exit(1)

resultat = arg1 + arg2
print(resultat)
