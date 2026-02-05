from sqlalchemy.orm import Session
from src.api.db import SessionLocal
from src.api.models import Query

def update_clusters_in_db(clusters, question_ids):
    db: Session = SessionLocal()
    for qid, cluster_label in zip(question_ids, clusters):
        q = db.query(Query).get(qid)
        if q:
            q.cluster = int(cluster_label)
    db.commit()
    db.close()
