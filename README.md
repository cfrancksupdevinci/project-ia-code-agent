# 🧠 AI Script Reviewer CLI

Ce projet permet d’analyser et de recevoir des retours intelligents sur des scripts Python via une interface en ligne de commande (CLI) alimentée par des modèles de langage (LLMs).

---

## ⚙️ Prérequis & Installation

### 1. Cloner le projet

```bash
git clone <url-de-ton-repo>
cd <nom-du-dossier>
```

### 2. Créer et activer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Variables d’environnement (si tu utilises OpenAI)

Crée un fichier `.env` à la racine du projet avec ta clé :

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Pour utiliser Ollama

Assure-toi d’avoir installé [Ollama](https://ollama.com) puis :

```bash
ollama serve  # Lancer le serveur Ollama (obligatoire)
```

---

## 🚀 Utilisation

### Commande de base

```bash
python cli.py --file <chemin_vers_script.py> --mode <mode> --provider <provider>
```

### 🔧 Arguments disponibles

- `--file` : Chemin vers un fichier `.py` à analyser  
  Exemples :

  - `examples/clean_script.py`
  - `examples/buggy_script.py`

- `--mode` : Mode d’analyse :

  - `test_focus` – vérifie la logique et les tests
  - `mentor` – feedback pédagogique
  - `strict` – analyse rigoureuse, niveau expert

- `--provider` : Modèle utilisé :
  - `openai` – via API OpenAI (⚠️ quotas sur comptes gratuits)
  - `ollama` – modèle local avec Ollama (⚠️ `ollama serve` requis)

---

## 🛑 Limitations

- `OpenAI` a un **quota limité** avec un compte gratuit.
- `Anthropic` (Claude) **non utilisé** ici car uniquement accessible avec un compte **payant**.
- `Ollama` nécessite que :
  - Le serveur soit lancé : `ollama serve`
  - Un modèle soit démarré : `ollama run llama3`

---

## 🧪 Exemples

```bash
# Analyse avec OpenAI
python cli.py --file examples/clean_script.py --mode mentor --provider openai

# Analyse stricte avec Ollama
python cli.py --file examples/buggy_script.py --mode strict --provider ollama

# Vérification logique d’un script
python cli.py --file examples/clean_script.py --mode test_focus --provider openai
```

---

## ✅ Exemple de requirements.txt

Si tu n’as pas encore le fichier, crée un `requirements.txt` avec :

```
python-dotenv
openai
ollama
```

Ajoute d’autres libs si ton projet en dépend.

---

## 📁 Organisation

```
.
├── cli.py
├── examples/
│   ├── clean_script.py
│   └── buggy_script.py
├── requirements.txt
└── README.md
```

---

🎉 Voilà ! Tout est prêt pour que tu puisses analyser tes scripts Python avec des LLMs en local ou via OpenAI.
