from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

class ModelEvaluator:

    def evaluate(self, y_test, y_pred_test):
        r2 = r2_score(y_test, y_pred_test)
        mse = mean_squared_error(y_test, y_pred_test)
        rmse = np.sqrt(mse)

        return {
            "r2_score": r2,
            "mse": mse,
            "rmse": rmse
        }
    
    def correlation_warning(self, X, y):
        corr = np.corrcoef(X.flatten(), y)[0, 1]
        if abs(corr) < 0.3:
            level = "low"
            message = (
                "La correlación entre la variable independiente "
                "es baja. El modelo puede no ser fiable."
            )
        elif abs(corr) < 0.6:
            level = "medium"
            message = (
                "La correlación entre la variable independiente "
                "es moderada. Los resultados deben interpretarse con cautela."
            )
        else:
            level = "high"
            message = "La correlación es alta. El modelo es probablemente fiable."
        return {
            "correlation": corr,
            "level": level,
            "message": message
        }
    
    def fitting_warning(self, r2_train, r2_test):
        if r2_train - r2_test > 0.2:
            return {
                "type": "overfitting",
                "message": (
                    "El modelo presenta un ajuste significativamente mejor "
                    "en entrenamiento que en prueba. Puede existir overfitting."
                )
            }

        if r2_train < 0.3 and r2_test < 0.3:
            return {
                "type": "underfitting",
                "message": (
                    "El modelo presenta bajo desempeño tanto en entrenamiento "
                    "como en prueba. Puede existir underfitting."
                )
            }

        return None