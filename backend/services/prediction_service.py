import numpy as np
from pathlib import Path
from repository.model_repository import ModelRepository

class PredictionService:

    def predict(self, values):
        repo = ModelRepository()
        
        # Usar ruta absoluta
        models_dir = Path(__file__).parent.parent / "models"
        model_path = str(models_dir / "linear_model.pkl")
        
        model = repo.load(model_path)

        X = np.array(values).reshape(-1, 1)
        predictions = model.predict(X)

        return predictions.tolist()
