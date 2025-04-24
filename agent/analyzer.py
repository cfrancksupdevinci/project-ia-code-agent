import yaml

class CodeAnalyzer:
    def __init__(self, mode):
        self.mode = mode
        self.prompt_template = self.load_template(mode)

    def load_template(self, mode):
        """Charge le template correspondant au mode depuis templates.yaml."""
        try:
            with open("prompts/templates.yaml", "r") as file:
                templates = yaml.safe_load(file)
            if mode not in templates:
                raise ValueError(f"Mode '{mode}' non trouvé dans templates.yaml")
            return templates[mode]["description"]
        except FileNotFoundError:
            raise RuntimeError("Le fichier templates.yaml est introuvable.")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Erreur lors du chargement de templates.yaml : {e}")

    def construct_prompt(self, code_snippet):
        """Construit le prompt en combinant le template et le code."""
        return f"{self.prompt_template}\n\nVoici le code à analyser :\n{code_snippet}"
    
if __name__ == "__main__":
    # Spécifiez le mode
    mode = "mentor"

    # Chemin vers le fichier à analyser
    file_path = "examples/clean_script.py"

    try:
        # Lire le contenu du fichier
        with open(file_path, "r") as file:
            code_snippet = file.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        exit(1)

    # Initialiser l'analyseur et construire le prompt
    analyzer = CodeAnalyzer(mode=mode)
    prompt = analyzer.construct_prompt(code_snippet)
    print(prompt)