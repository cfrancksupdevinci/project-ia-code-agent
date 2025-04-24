def add(a, b):
    """
    Ajoute deux nombres entiers.

    Args:
        a (int): Le premier nombre entier.
        b (int): Le deuxième nombre entier.

    Returns:
        int: La somme des deux nombres.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Les deux arguments doivent être des entiers.")
    return a + b

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        result = add(2, 3)
        print(f"La somme est : {result}")
    except ValueError as e:
        print(f"Erreur : {e}")