"""
Utilidades para el modelo v9
Guardar en: Training/model_v9/model_v9_utils.py
"""
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

def load_model_v9(model_path, prep_path):
    """Carga modelo v9 guardado"""
    model = joblib.load(model_path)
    preprocessors = joblib.load(prep_path)
    
    return model, preprocessors

def predict_with_symptoms_v9(symptoms_dict, model, preprocessors):
    """Predicción con síntomas para modelo v9"""
    feature_cols = preprocessors['feature_columns']
    label_encoder = preprocessors['diagnosis_encoder']
    
    # Crear vector de características
    feature_vector = np.zeros(len(feature_cols))
    
    for symptom, value in symptoms_dict.items():
        if symptom in feature_cols:
            idx = feature_cols.index(symptom)
            feature_vector[idx] = value
    
    # Predicción
    feature_vector = feature_vector.reshape(1, -1)
    prediction = model.predict(feature_vector)[0]
    probabilities = model.predict_proba(feature_vector)[0]
    
    # Resultados
    predicted_disease = label_encoder.inverse_transform([prediction])[0]
    confidence = probabilities[prediction]
    
    # Top predicciones
    top_indices = np.argsort(probabilities)[-10:][::-1]
    top_predictions = []
    
    for idx in top_indices:
        disease = label_encoder.inverse_transform([idx])[0]
        prob = probabilities[idx]
        top_predictions.append({
            'disease': disease,
            'probability': float(prob * 100)
        })
    
    return {
        'success': True,
        'main_diagnosis': predicted_disease,
        'confidence': float(confidence * 100),
        'confidence_level': get_confidence_level(confidence * 100),
        'top_predictions': top_predictions,
        'model_version': 'v9'
    }

def get_confidence_level(confidence):
    """Determina nivel de confianza"""
    if confidence >= 80:
        return "Muy Alta"
    elif confidence >= 60:
        return "Alta"
    elif confidence >= 40:
        return "Media"
    elif confidence >= 20:
        return "Baja"
    else:
        return "Muy Baja"