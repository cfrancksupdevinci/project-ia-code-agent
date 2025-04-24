# cli.py

import argparse
from agent.llm_interface import LLMClient

def main():
    # Configuration de l'interface en ligne de commande
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--file", required=True, help="Chemin du fichier Python à analyser")
    parser.add_argument("--mode", required=True, help="Mode d'analyse (strict, mentor, test_focus)")
    parser.add_argument("--provider", required=True, help="Fournisseur LLM (openai, ollama)")
    args = parser.parse_args()

    # Lecture du fichier Python
    try:
        with open(args.file, "r") as file:
            code_snippet = file.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {args.file} est introuvable.")
        return

    # Initialisation du client LLM
    llm_client = LLMClient(provider=args.provider)

    # Appel au modèle et affichage du résultat
    try:
        # Passe uniquement args.mode (par exemple, 'mentor') à llm_client.run
        review = llm_client.run(args.mode, code_snippet)
        print("=== Résultat de la revue ===")
        print(review)
    
        # Écrire le résultat dans review_output.md
        output_file = "reviews/review_output.md"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("# Résultat de la revue\n\n")
            file.write(review)
        print(f"Le résultat a été écrit dans {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")

if __name__ == "__main__":
    main()