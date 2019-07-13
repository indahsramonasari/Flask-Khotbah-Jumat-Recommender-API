from app import db


class Details(db.Model):
    __tablename__ = "details"  # Define table name

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    document = db.Column(db.String, nullable=False)
    label = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    link = db.Column(db.String, nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey("queries.id"))

    def __init__(self, data):
        document, label, score, link = data
        self.document = document
        self.label = label
        self.score = score
        self.link = link

    def __repr__(self):
        return "<Link: {}>".format(self.Link)

    @staticmethod
    def getAll(queryId):
        details = Details.query.filter_by(query_id=queryId).order_by(Details.score.desc()).limit(5).all()
        result = list()
        for data in details:
            obj = {
                "id": data.id,
                "document": data.document,
                "label": data.label,
                "score": data.score,
                "link": data.link
            }
            result.append(obj)
        return result
