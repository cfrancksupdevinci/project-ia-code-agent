# llm_interface.py
import requests
import json
import yaml
import openai

class LLMClient:
    def __init__(self, provider, model=None):
        self.provider = provider
        self.model = model or "phi"
    
    # Charger la clé API depuis config.yaml
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    OPENAI_API_KEY = config["openai"]["api_key"]

    def run(self, prompt, code_snippet):
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
                openai.api_key = OPENAI_API_KEY
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Remplacez par le modèle souhaité
                    prompt=input_text,
                    max_tokens=1500,
                    temperature=0.7
                )
                return response["choices"][0]["text"].strip()
            except openai.error.OpenAIError as e:
                raise RuntimeError(f"Erreur OpenAI : {e}")