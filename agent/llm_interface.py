# llm_interface.py
import requests
import json
import yaml
import openai
from agent.analyzer import CodeAnalyzer
import os

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
        print(f"Mode reçu dans run : {mode}")  # Debug
        analyzer = CodeAnalyzer(mode)
        prompt = analyzer.construct_prompt(code_snippet)
        print(f"Prompt construit : {prompt}")  # Debug
    
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "ollama":
            return self._call_ollama(prompt)
        else:
            raise ValueError(f"Fournisseur non supporté : {self.provider}")
    
    def _call_ollama(self, prompt, code_snippet=None):
        """Appelle le modèle Mistral via Ollama."""
        input_text = f"{prompt}\n\n{code_snippet}" if code_snippet else prompt
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
    
    def _call_openai(self, prompt):
        """Appelle le modèle OpenAI."""
        try:
            openai.api_key = self.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Remplacez par le modèle souhaité (par exemple, gpt-4)
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant utile pour analyser du code Python."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"].strip()
        except openai.OpenAIError as e:
            raise RuntimeError(f"Erreur OpenAI : {e}")
    
    def load_template(self, mode):
        """Charge le template correspondant au mode depuis templates.yaml."""
        try:
            with open("prompts/templates.yaml", "r") as file:
                templates = yaml.safe_load(file)
            print(f"Templates chargés : {templates}")  # Debug
            if mode not in templates:
                raise ValueError(f"Mode '{mode}' non trouvé dans templates.yaml")
            print(f"Description pour le mode '{mode}' : {templates[mode]['description']}")  # Debug
            return templates[mode]["description"]
        except FileNotFoundError:
            raise RuntimeError("Le fichier templates.yaml est introuvable.")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Erreur lors du chargement de templates.yaml : {e}")