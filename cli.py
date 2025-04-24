import argparse
from agent.llm_interface import LLMClient

def main():
    # Configuration de l'interface en ligne de commande
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--file", required=True, help="Chemin du fichier Python à analyser")
    parser.add_argument("--mode", required=True, help="Mode d'analyse (strict, mentor, test_focus)")
    parser.add_argument("--provider", required=True, help="Fournisseur LLM (ollama)")
    args = parser.parse_args()

    # Lecture du fichier Python
    try:
        with open(args.file, "r") as file:
            code_snippet = file.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {args.file} est introuvable.")
        return

    # Initialisation du client LLM
    llm_client = LLMClient(provider=args.provider, model="mistral")

    # Construction du prompt en fonction du mode
    prompt = f"Mode : {args.mode}. Analysez le code suivant et fournissez des commentaires détaillés :"

    # Appel au modèle et affichage du résultat
    try:
        review = llm_client.run(prompt, code_snippet)
        print("=== Résultat de la revue ===")
        print(review)
    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")

if __name__ == "__main__":
    main()