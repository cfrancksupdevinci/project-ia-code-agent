# llm_interface.py
import requests
import json
import yaml
import openai
from agent.analyzer import CodeAnalyzer

class LLMClient:
    def __init__(self, provider, model=None):
        self.provider = provider
        self.model = model or "phi"
    
    # Charger la clé API depuis config.yaml
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    OPENAI_API_KEY = config["openai"]["api_key"]
    
    def run(self, mode, code_snippet):
        """Construit le prompt en fonction du mode et exécute l'appel au modèle."""
        analyzer = CodeAnalyzer(mode)  # Passe uniquement le mode (par exemple, 'mentor')
        prompt = analyzer.construct_prompt(code_snippet)  # Le prompt est construit ici
    
        # Appeler le modèle en fonction du fournisseur
        if self.provider == "openai":
            return self._call_openai(prompt, code_snippet)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, code_snippet)
        else:
            raise ValueError(f"Fournisseur non supporté : {self.provider}")
    
    def _call_ollama(self, prompt, code_snippet):
        """Appelle le modèle Mistral via Ollama."""
        input_text = f"{prompt}\n\n{code_snippet}"
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model, "prompt": input_text},
                stream=True  # Active le streaming des réponses
            )
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:  # Ignorer les lignes vides
                        try:
                            data = json.loads(line.decode("utf-8"))
                            full_response += data.get("response", "")
                        except json.JSONDecodeError:
                            print(f"Ligne non valide : {line}")
                return full_response.strip()
            else:
                raise RuntimeError(f"Erreur Ollama : {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Impossible de se connecter au service Ollama. Assurez-vous qu'il est actif.")
    
    def _call_openai(self, prompt, code_snippet):
        """Appelle le modèle OpenAI."""
        input_text = f"{prompt}\n\n{code_snippet}"
        try:
            openai.api_key = self.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Remplacez par le modèle souhaité (par exemple, gpt-4)
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant utile pour analyser du code Python."},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"].strip()
        except openai.OpenAIError as e:
            raise RuntimeError(f"Erreur OpenAI : {e}")
    
    def load_template(mode):
        """Charge le template correspondant au mode depuis templates.yaml."""
        with open("prompts/templates.yaml", "r") as file:
            templates = yaml.safe_load(file)
        if mode not in templates:
            raise ValueError(f"Mode '{mode}' non trouvé dans templates.yaml")
        return templates[mode]["description"]