import os
import cv2
import numpy as np
import pickle
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

def entrenar_modelo():
    datos = []
    etiquetas = []

    for archivo in os.listdir('dataset'):
        if archivo.endswith(".jpg"):
            path = os.path.join("dataset", archivo)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            resized = cv2.resize(img, (100, 100)).flatten()
            datos.append(resized)
            etiquetas.append(int(archivo.split("_")[0]))

    if len(datos) < 2:
        print("⚠️ No hay suficientes imágenes para entrenar.")
        return

    X = np.array(datos)
    y = np.array(etiquetas)

    pca = PCA(n_components=50)
    X_pca = pca.fit_transform(X)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_pca, y)

    # Guardamos modelos
    with open("modelos/modelo_pca.pkl", "wb") as f:
        pickle.dump(pca, f)
    with open("modelos/modelo_logistico.pkl", "wb") as f:
        pickle.dump(model, f)

    print("✅ Modelo PCA + Regresión Logística entrenado y guardado.")
