"""
Análisis Comparativo: V1 vs V2
Compara el rendimiento de ambas versiones del sistema
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_comparison():
    """Analiza y compara V1 vs V2."""
    
    try:
        # Cargar datos
        df_v1 = pd.read_csv('model_comparison.csv')
        df_v2 = pd.read_csv('model_comparison_v2.csv')
        
        df_v1['Version'] = 'V1'
        df_v2['Version'] = 'V2'
        
        print("="*80)
        print("[ANÁLISIS] COMPARACIÓN V1 vs V2")
        print("="*80)
        
        # Estadísticas básicas
        print(f"\n[INFO] Datos cargados:")
        print(f"  V1: {len(df_v1)} registros ({df_v1['Cycle'].nunique()} ciclos)")
        print(f"  V2: {len(df_v2)} registros ({df_v2['Cycle'].nunique()} ciclos)")
        
        # Distribución de señales V1
        print(f"\n[V1] DISTRIBUCIÓN DE SEÑALES:")
        signal_dist_v1 = df_v1.groupby('Model_Name')['Model_Signal'].value_counts()
        print(signal_dist_v1)
        
        # Distribución de señales V2
        print(f"\n[V2] DISTRIBUCIÓN DE SEÑALES:")
        signal_dist_v2 = df_v2.groupby('Model_Name')['Model_Signal'].value_counts()
        print(signal_dist_v2)
        
        # Consenso V1
        print(f"\n[V1] CONSENSO:")
        consensus_v1 = df_v1.groupby('Cycle').first()['Consensus_Signal'].value_counts()
        print(consensus_v1)
        print(f"Agreement promedio: {df_v1.groupby('Cycle').first()['Agreement_Level'].mean():.1f}%")
        
        # Consenso V2
        print(f"\n[V2] CONSENSO:")
        consensus_v2 = df_v2.groupby('Cycle').first()['Consensus_Signal'].value_counts()
        print(consensus_v2)
        print(f"Agreement promedio: {df_v2.groupby('Cycle').first()['Agreement_Level'].mean():.1f}%")
        
        # Confidence Score V2
        if 'Confidence_Score' in df_v2.columns:
            print(f"\n[V2] CONFIDENCE SCORE:")
            print(f"  Promedio: {df_v2.groupby('Cycle').first()['Confidence_Score'].mean():.1f}")
            print(f"  Mediana: {df_v2.groupby('Cycle').first()['Confidence_Score'].median():.1f}")
            print(f"  Mínimo: {df_v2.groupby('Cycle').first()['Confidence_Score'].min():.1f}")
            print(f"  Máximo: {df_v2.groupby('Cycle').first()['Confidence_Score'].max():.1f}")
            
            # Operaciones válidas (confidence >= 75)
            valid_trades = df_v2.groupby('Cycle').first()
            valid_count = (valid_trades['Confidence_Score'] >= 75).sum()
            total_cycles = len(valid_trades)
            print(f"\n[V2] OPERACIONES VÁLIDAS (Confidence ≥75%):")
            print(f"  {valid_count}/{total_cycles} ciclos ({valid_count/total_cycles*100:.1f}%)")
        
        # Setup Score V2
        if 'Setup_Score' in df_v2.columns:
            print(f"\n[V2] SETUP SCORE:")
            print(f"  Promedio: {df_v2.groupby('Cycle').first()['Setup_Score'].mean():.1f}/10")
            print(f"  Máximo: {df_v2.groupby('Cycle').first()['Setup_Score'].max()}/10")
        
        # Tiempos de respuesta
        print(f"\n[COMPARACIÓN] TIEMPOS DE RESPUESTA:")
        print(f"  V1 promedio: {df_v1['Model_Response_Time_ms'].mean():.0f}ms")
        print(f"  V2 promedio: {df_v2['Model_Response_Time_ms'].mean():.0f}ms")
        
        # Gráficos
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Distribución de señales de consenso
        ax1 = axes[0, 0]
        consensus_comparison = pd.DataFrame({
            'V1': df_v1.groupby('Cycle').first()['Consensus_Signal'].value_counts(),
            'V2': df_v2.groupby('Cycle').first()['Consensus_Signal'].value_counts()
        }).fillna(0)
        consensus_comparison.plot(kind='bar', ax=ax1, color=['#3498db', '#2ecc71'])
        ax1.set_title('Distribución de Señales de Consenso: V1 vs V2', fontweight='bold')
        ax1.set_ylabel('Frecuencia')
        ax1.set_xlabel('Señal')
        ax1.legend(['V1', 'V2'])
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Agreement Level
        ax2 = axes[0, 1]
        agreement_v1 = df_v1.groupby('Cycle').first()['Agreement_Level']
        agreement_v2 = df_v2.groupby('Cycle').first()['Agreement_Level']
        ax2.hist([agreement_v1, agreement_v2], bins=20, label=['V1', 'V2'], 
                 color=['#3498db', '#2ecc71'], alpha=0.7, edgecolor='black')
        ax2.set_title('Distribución de Agreement Level', fontweight='bold')
        ax2.set_xlabel('Agreement (%)')
        ax2.set_ylabel('Frecuencia')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Confidence Score V2
        ax3 = axes[1, 0]
        if 'Confidence_Score' in df_v2.columns:
            confidence_v2 = df_v2.groupby('Cycle').first()['Confidence_Score']
            ax3.hist(confidence_v2, bins=20, color='#2ecc71', alpha=0.7, edgecolor='black')
            ax3.axvline(x=75, color='red', linestyle='--', linewidth=2, label='Threshold (75%)')
            ax3.set_title('V2: Distribución de Confidence Score', fontweight='bold')
            ax3.set_xlabel('Confidence Score')
            ax3.set_ylabel('Frecuencia')
            ax3.legend()
            ax3.grid(axis='y', alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'V2: No Confidence Score data', 
                     ha='center', va='center', transform=ax3.transAxes)
        
        # 4. Setup Score V2
        ax4 = axes[1, 1]
        if 'Setup_Score' in df_v2.columns:
            setup_v2 = df_v2.groupby('Cycle').first()['Setup_Score']
            ax4.hist(setup_v2, bins=11, range=(0, 10), color='#2ecc71', 
                     alpha=0.7, edgecolor='black')
            ax4.set_title('V2: Distribución de Setup Score', fontweight='bold')
            ax4.set_xlabel('Setup Score (0-10)')
            ax4.set_ylabel('Frecuencia')
            ax4.set_xticks(range(0, 11))
            ax4.grid(axis='y', alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'V2: No Setup Score data', 
                     ha='center', va='center', transform=ax4.transAxes)
        
        plt.tight_layout()
        plt.savefig('comparison_v1_vs_v2.png', dpi=300, bbox_inches='tight')
        print(f"\n[OK] Gráfico guardado: comparison_v1_vs_v2.png")
        plt.show()
        
        # Recomendación
        print(f"\n{'='*80}")
        print("[RECOMENDACIÓN]")
        print("="*80)
        
        if 'Confidence_Score' in df_v2.columns:
            avg_confidence = df_v2.groupby('Cycle').first()['Confidence_Score'].mean()
            if avg_confidence >= 75:
                print(f"✅ V2 tiene un Confidence Score promedio de {avg_confidence:.1f}%")
                print("   Esto sugiere que las señales son de ALTA CALIDAD.")
            else:
                print(f"⚠️  V2 tiene un Confidence Score promedio de {avg_confidence:.1f}%")
                print("   Considera ajustar el threshold o esperar más datos.")
        
        print("\n💡 Próximos pasos:")
        print("  1. Ejecutar ambas versiones durante 1-2 semanas")
        print("  2. Comparar rentabilidad con model_analysis_simple.ipynb")
        print("  3. Seleccionar la versión con mejor R/R y menor drawdown")
        
    except FileNotFoundError as e:
        print(f"[ERROR] Archivo no encontrado: {e}")
        print("\n💡 Asegúrate de ejecutar ambas versiones primero:")
        print("  python model_comparison.py")
        print("  python model_comparison_v2.py")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    analyze_comparison()
