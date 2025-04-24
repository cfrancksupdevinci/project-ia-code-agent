# llm_interface.py
import requests

class LLMClient:
    def __init__(self, provider, model=None):
        self.provider = provider
        self.model = model or "phi"

    def run(self, prompt, code_snippet):
        if self.provider == "ollama":
            return self._call_ollama(prompt, code_snippet)
        else:
            raise ValueError(f"Fournisseur non supporté : {self.provider}")

    def _call_ollama(self, prompt, code_snippet):
        """Appelle le modèle Mistral via Ollama."""
        input_text = f"{prompt}\n\n{code_snippet}"
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",  # Port par défaut d'Ollama
                json={"model": self.model, "prompt": input_text}
            )
            print("Réponse brute d'Ollama :", response.text)  # Ajoutez cette ligne pour afficher la réponse brute
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                raise RuntimeError(f"Erreur Ollama : {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Impossible de se connecter au service Ollama. Assurez-vous qu'il est actif.")