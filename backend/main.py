import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent))

from ml.dataset_loader import DatasetLoader

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.model_service import ModelService
from services.prediction_service import PredictionService
from schemas import PredictionRequest

app = FastAPI()

# CONFIGURACIÓN CORS - DEBE IR ANTES DE LAS RUTAS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo, permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = ModelService()
prediction_service = PredictionService()


@app.get("/")
async def root():
    return {"message": "Servidor de Regresión Lineal"}

@app.post("/train")
async def train_model(file: UploadFile = File(...), x_col: str = Form(None), y_col: str = Form(None)):
    try:
        # Debug: verificar qué se recibe
        print(f"DEBUG: x_col={x_col}, y_col={y_col}, x_col_type={type(x_col)}, y_col_type={type(y_col)}")
        
        # Si las columnas son strings vacíos, convertir a None
        x_col = x_col if x_col and x_col.strip() else None
        y_col = y_col if y_col and y_col.strip() else None
        
        print(f"DEBUG: Después de procesamiento: x_col={x_col}, y_col={y_col}")
        
        result = service.train_from_file(file.file, x_col, y_col)
        return result
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"error": str(e), "detail": "Error al procesar el archivo"}


@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        predictions = prediction_service.predict(request.x)
        return {
            "inputs": request.x,
            "predictions": predictions
        }
    except Exception as e:
        return {"error": str(e), "detail": "Error al realizar la predicción"}

@app.post("/columns")
async def get_columns(file: UploadFile = File(...)):
    try:
        loader = DatasetLoader()
        df = loader.load(file.file)
        numeric_cols = loader.get_numeric_columns(df)
        return {"numeric_columns": numeric_cols}
    except Exception as e:
        return {"error": str(e), "detail": "Error al procesar el archivo"}