# -*- coding: utf-8 -*-
"""AerialDetectionAtualizado.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xs9O8s9fp8soOmpNxhIWwvy7EtKAeAgH
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install ultralytics
# %pip install roboflow
# %pip install tensorflow
# %pip install kaggle

from ultralytics import YOLO
import tensorflow as tf
import os
import shutil

tf.config.list_physical_devices('GPU')

if tf.config.list_physical_devices('GPU'):
    print("Usando GPU")
else:
    print("Usando CPU")

# Carregando dados do Google Drive
from google.colab import drive
drive.mount('/content/drive')

dataset_path = '/content/drive/MyDrive/Colab Notebooks/IC/Datasets/Dataset/YOLOv8DATASET/drone-detection-new.v5-new-train.yolov8'

# Caminho para salvar o arquivo YAML
yaml_file_path = os.path.join(dataset_path, "drone-detection.yaml")

# Conteúdo do YAML
yaml_content = """
train: ../train/images
val: ../valid/images
test: ../test/images

nc: 3
names: ['AirPlane', 'Drone', 'Helicopter']

roboflow:
  workspace: ahmedmohsen
  project: drone-detection-new-peksv
  version: 5
  license: MIT
  url: https://universe.roboflow.com/ahmedmohsen/drone-detection-new-peksv/dataset/5
"""

# Salvando o YAML no caminho especificado
with open(yaml_file_path, 'w') as yaml_file:
    yaml_file.write(yaml_content)

print(f"Arquivo YAML salvo em: {yaml_file_path}")

# Caminho do arquivo YAML
yaml_file_path = os.path.join(dataset_path, "drone-detection.yaml")

# Configuração do modelo YOLOv8
model = YOLO('yolov8n.pt')

# Treinamento da rede
model.train(data=yaml_file_path, epochs=30, imgsz=640, batch=16, project='DroneDetectionProject', name='YOLOv8_Training')

print("Treinamento concluído!")

# Realizando a validação do modelo treinado
metrics = model.val()

# Exibindo as métricas de validação
print("Métricas de validação:")
print(metrics)

import matplotlib.pyplot as plt
import os

# Caminho dos resultados do treinamento
training_results_path = os.path.join('runs', 'train', 'YOLOv8_Training')

# Verifica se os resultados estão disponíveis
if not os.path.exists(training_results_path):
    print(f"Resultados de treinamento não encontrados em {training_results_path}")
else:
    # Caminho do arquivo de resultados
    results_file = os.path.join(training_results_path, 'results.csv')

    # Lendo o arquivo de resultados
    if os.path.exists(results_file):
        import pandas as pd
        results_df = pd.read_csv(results_file)

        # Plotando a perda (loss)
        plt.figure(figsize=(10, 6))
        plt.plot(results_df['epoch'], results_df['box_loss'], label='Box Loss')
        plt.plot(results_df['epoch'], results_df['obj_loss'], label='Objectness Loss')
        plt.plot(results_df['epoch'], results_df['cls_loss'], label='Class Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Loss durante o treinamento')
        plt.legend()
        plt.grid()
        plt.show()

        # Plotando a precisão e recall
        plt.figure(figsize=(10, 6))
        plt.plot(results_df['epoch'], results_df['precision'], label='Precision')
        plt.plot(results_df['epoch'], results_df['recall'], label='Recall')
        plt.xlabel('Epochs')
        plt.ylabel('Score')
        plt.title('Precisão e Recall durante o treinamento')
        plt.legend()
        plt.grid()
        plt.show()

        # Plotando mAP
        plt.figure(figsize=(10, 6))
        plt.plot(results_df['epoch'], results_df['metrics/mAP_0.5'], label='mAP@0.5')
        plt.plot(results_df['epoch'], results_df['metrics/mAP_0.5:0.95'], label='mAP@0.5:0.95')
        plt.xlabel('Epochs')
        plt.ylabel('mAP')
        plt.title('mAP durante o treinamento')
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print(f"Arquivo de resultados não encontrado em {results_file}")
