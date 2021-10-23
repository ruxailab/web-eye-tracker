from firebase_admin import firestore

def create_document(collection, doc_id, data):
    db = firestore.client()
    doc_ref = db.collection(collection).document(doc_id).set(data)
    return doc_ref