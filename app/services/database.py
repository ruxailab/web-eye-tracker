from firebase_admin import firestore


def create_document(collection, doc_id, data):
    db = firestore.client()
    return db.collection(collection).document(doc_id).set(data)


def get_documents(collection, field, op, value):
    db = firestore.client()
    if field is not None and op is not None and value is not None:
        return db.collection(collection).where(field, op, value).stream()
    return db.collection(collection).stream()


def get_document(collection, doc_id):
    db = firestore.client()
    return db.collection(collection).document(doc_id).get()


def delete_document(collection, doc_id):
    db = firestore.client()
    return db.collection(collection).document(doc_id).delete()


def update_document(collection, doc_id, data):
    db = firestore.client()
    return db.collection(collection).document(doc_id).update(data)
