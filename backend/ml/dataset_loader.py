import pandas as pd
import numpy as np

class DatasetLoader:

    def load(self, file):
        return pd.read_csv(file)

    def get_numeric_columns(self, df):
        """Retorna lista de nombres de columnas numéricas"""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.columns.tolist()

    def split_features(self, df, x_col=None, y_col=None):
        """
        Divide las características en X e Y.
        Si x_col e y_col son especificadas, los usa.
        Si no, selecciona automáticamente basado en varianza y correlación.
        """
        # 1. Filtrar solo columnas numéricas
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            raise ValueError("El dataset debe contener al menos una columna numérica para características y una para la variable objetivo.")
        
        # Si se especifican ambas columnas, usarlas
        if x_col and y_col:
            if x_col not in numeric_df.columns or y_col not in numeric_df.columns:
                raise ValueError(f"Las columnas especificadas no son numéricas o no existen. X: {x_col}, Y: {y_col}")
            X = numeric_df[[x_col]].values
            y = numeric_df[y_col].values
            return X, y, x_col, y_col

        # 2. Si no se especifican, seleccionar automáticamente
        # Seleccionar Y: columna con mayor varianza
        y_column = numeric_df.var().idxmax()

        # 3. Seleccionar X: la numérica distinta de Y con mayor correlación
        correlations = numeric_df.corr()[y_column].drop(y_column)
        x_column = correlations.abs().idxmax()

        X = numeric_df[[x_column]].values
        y = numeric_df[y_column].values

        return X, y, x_column, y_column
        return numeric_cols