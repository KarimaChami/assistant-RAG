# src/ml/mlflow_tracking.py
# src/ml/mlflow_tracking.py
from src.utils.rag_service import ask_rag
import mlflow

# Configuration MLflow
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("RAG_Assistant_Experiment")

# Démarrer un run MLflow
with mlflow.start_run():
    
    # 1. Log des paramètres du modèle
    mlflow.log_param("model", "gemini-2.5-flash")
    mlflow.log_param("temperature", 0.3)
    mlflow.log_param("chunk_size", 500)
    mlflow.log_param("chunk_overlap", 50)
    mlflow.log_param("retriever_k", 3)
    
    # 2. Exécuter la requête RAG (récupère 2 valeurs)
    question = "who is mike halsey ?"
    
    response, latency_ms = ask_rag(question)  # ✅ CORRECTION : récupère les 2 valeurs
    
    # 3. Log des métriques
    mlflow.log_metric("latency_ms", latency_ms)
    mlflow.log_metric("num_chunks_retrieved", 3)
    
    # 4. Log des textes (question et réponse)
    mlflow.log_text(question, "question.txt")
    mlflow.log_text(response, "answer.txt")
    
    # 5. Affichage
    print(f"✅ Run MLflow enregistré")
    print(f"Question : {question}")
    print(f"Réponse : {response}")
    print(f"Latence : {latency_ms:.2f} ms")

