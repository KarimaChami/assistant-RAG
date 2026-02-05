from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.cluster import KMeans
import numpy as np
from src.ml.update_db import update_clusters_in_db
from src.api.db import SessionLocal
from src.api.models import Query
def cluster_questions(questions,question_ids, n_clusters=3):
       embeddings_model = HuggingFaceEmbeddings(
           model_name="sentence-transformers/all-MiniLM-L6-v2"
       )
       
       question_embeddings = embeddings_model.embed_documents(questions)
       X = np.array(question_embeddings)

       kmeans = KMeans(n_clusters=n_clusters, random_state=42,n_init='auto')
       clusters = kmeans.fit_predict(X)

       # Update database with cluster labels
       update_clusters_in_db(clusters, question_ids)
       
       return clusters


db = SessionLocal()
queries = db.query(Query).filter(Query.cluster == None).all()
questions = [q.question for q in queries]
question_ids = [q.id for q in queries]

clusters = cluster_questions(questions, question_ids, n_clusters=5)
print("✅ Clustering terminé :", clusters)