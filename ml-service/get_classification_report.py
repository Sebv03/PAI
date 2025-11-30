# ml-service/get_classification_report.py
"""
Script para obtener el reporte de clasificación detallado del modelo ML
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from services.data_service import DataService
from services.feature_engineering import FeatureEngineering
from services.model_service import ModelService

def main():
    print("=" * 70)
    print("REPORTE DE CLASIFICACIÓN DETALLADO DEL MODELO ML")
    print("=" * 70)
    
    # Inicializar servicios
    data_service = DataService()
    feature_engineering = FeatureEngineering()
    model_service = ModelService()
    
    try:
        # Obtener datos históricos
        print("\n📊 Obteniendo datos históricos...")
        historical_data = data_service.get_historical_data()
        
        if historical_data.empty:
            print("❌ No hay datos históricos disponibles")
            return
        
        print(f"✅ Datos obtenidos: {len(historical_data)} registros")
        
        # Feature engineering
        print("\n🔧 Calculando features...")
        features_df = feature_engineering.calculate_features(historical_data)
        
        if features_df.empty:
            print("❌ No se pudieron calcular features")
            return
        
        print(f"✅ Features calculadas: {len(features_df)} registros")
        
        # Entrenar modelo
        print("\n🤖 Entrenando modelo...")
        metrics = model_service.train_model(features_df)
        
        # Guardar modelo
        model_service.save_model()
        
        # Mostrar reporte detallado
        print("\n" + "=" * 70)
        print("REPORTE DE CLASIFICACIÓN DETALLADO")
        print("=" * 70)
        
        print("\n📈 MÉTRICAS GENERALES:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"  Precision: {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
        print(f"  Recall:    {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
        print(f"  F1-Score:  {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
        
        print("\n📊 DISTRIBUCIÓN DE CLASES:")
        print(f"  Conjunto de Entrenamiento:")
        print(f"    - Riesgo Bajo: {metrics['class_distribution']['train']['riesgo_bajo']} muestras")
        print(f"    - Riesgo Alto: {metrics['class_distribution']['train']['riesgo_alto']} muestras")
        print(f"  Conjunto de Prueba:")
        print(f"    - Riesgo Bajo: {metrics['class_distribution']['test']['riesgo_bajo']} muestras")
        print(f"    - Riesgo Alto: {metrics['class_distribution']['test']['riesgo_alto']} muestras")
        
        print("\n🎯 MÉTRICAS POR CLASE:")
        print("\n  Riesgo Bajo:")
        print(f"    - Precision: {metrics['per_class_metrics']['riesgo_bajo']['precision']:.4f}")
        print(f"    - Recall:    {metrics['per_class_metrics']['riesgo_bajo']['recall']:.4f}")
        print(f"    - F1-Score:  {metrics['per_class_metrics']['riesgo_bajo']['f1_score']:.4f}")
        print(f"    - Support:   {metrics['per_class_metrics']['riesgo_bajo']['support']}")
        
        print("\n  Riesgo Alto:")
        print(f"    - Precision: {metrics['per_class_metrics']['riesgo_alto']['precision']:.4f}")
        print(f"    - Recall:    {metrics['per_class_metrics']['riesgo_alto']['recall']:.4f}")
        print(f"    - F1-Score:  {metrics['per_class_metrics']['riesgo_alto']['f1_score']:.4f}")
        print(f"    - Support:   {metrics['per_class_metrics']['riesgo_alto']['support']}")
        
        print("\n📋 MATRIZ DE CONFUSIÓN:")
        cm = metrics['confusion_matrix']
        print(f"                Predicho")
        print(f"              Bajo  Alto")
        print(f"Real Bajo    {cm[0][0]:4d}  {cm[0][1]:4d}")
        print(f"     Alto    {cm[1][0]:4d}  {cm[1][1]:4d}")
        
        print("\n📄 REPORTE DE CLASIFICACIÓN COMPLETO:")
        print(metrics['classification_report'])
        
        print("\n" + "=" * 70)
        print("✅ Reporte generado exitosamente")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

