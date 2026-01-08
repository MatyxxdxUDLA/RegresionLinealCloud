from sklearn.model_selection import train_test_split
from ml.dataset_loader import DatasetLoader
from ml.regression_model import RegressionModel
from ml.evaluator import ModelEvaluator
from repository.model_repository import ModelRepository
from pathlib import Path

class ModelService:

    def train_from_file(self, file, x_col=None, y_col=None):
        loader = DatasetLoader()
        model = RegressionModel()
        evaluator = ModelEvaluator()
        repo = ModelRepository()

        # 1. Cargar dataset
        df = loader.load(file)
        X, y, x_col, y_col = loader.split_features(df, x_col, y_col)
        
        # 2. Dividir en entrenamiento y prueba (igual que notebook)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=1/3, random_state=0
        )

        # 3. Entrenar modelo
        model.train(X_train, y_train)

        # 4. Predicciones
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # 5. Evaluación (solo sobre test, como debe ser)
        metrics_test = evaluator.evaluate(y_test, y_pred_test)
        metrics_train = evaluator.evaluate(y_train, y_pred_train)
        coefficients = model.coefficients()

        # Advertencias
        correlation_info = evaluator.correlation_warning(X, y)
        fitting_info = evaluator.fitting_warning(
            metrics_train["r2_score"],
            metrics_test["r2_score"]
        )

        # 6. Guardar modelo entrenado
        models_dir = Path(__file__).parent.parent / "models"
        models_dir.mkdir(exist_ok=True)

        repo.save(
            model.model,
            str(models_dir / "linear_model.pkl")
        )

        # 7. Respuesta completa para frontend
        return {
            "features": {
                "x": x_col,
                "y": y_col
            },
            "metrics": {
                "train": metrics_train,
                "test": metrics_test
            },
            "warnings": {
                "correlation": correlation_info,
                "fitting": fitting_info
            },
            "coefficients": coefficients,
            "train": {
                "x": X_train.flatten().tolist(),
                "y_real": y_train.tolist(),
                "y_pred": y_pred_train.tolist()
            },
            "test": {
                "x": X_test.flatten().tolist(),
                "y_real": y_test.tolist(),
                "y_pred": y_pred_test.tolist()
            }
        }
