import joblib

class ModelRepository:

    def save(self, model, path):
        joblib.dump(model, path)

    def load(self, path):
        return joblib.load(path)
