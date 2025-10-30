#dag.py

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG(
    
    # Nom du workflow
    'simple_harassment_pipeline',
    
    # Description
    description='Pipeline pour traiter les tweets de cyberharcèlement',
    
    # Date de début 
    start_date=datetime(2025, 1, 1),
    
    # Exécution manuelle seulement (pas de planification automatique)
    schedule_interval=None,
    
    # Ne pas exécuter les runs passés
    catchup=False,
    
    # Tags pour mieux organiser
    tags=['cyberbullying', 'pfe', 'data_pipeline']git status
) as dag:
    
    # Tache 1 : Nettoyer et charger les données
    clean_and_load = BashOperator(
        task_id='clean_and_load_data',
        bash_command='cd /Users/yosri/Desktop/"Test Stage" && python data_processing.py',
        dag=dag,
    )
