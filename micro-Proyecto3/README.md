# Aplicación para predecir diversas enfermedades

Se crea con Python una aplicación para predecir diversas enfermedades en función de un modelo de aprendizaje automático entrenado, “Regresor logístico con regularización tipo Ridge”. 


![App overview](https://i.ibb.co/bsrVPrT/Diseasesprediccionapp.jpg)

## Tabla de Contenido
1. [Introducción](#general-info)
2. [Tecnologia](#technologies)
3. [Modelo en producción con servidor remoto](#installation)


## Introducción 

En este proyecto, se construyó un regresor logístico con regularización tipo Ridge, para predecir el diagnóstico de 42 enfermedades de origen infeccioso, metabólico, agudo, crónico e inmunológico en función de un modelo de aprendizaje automático entrenado a con un regresor logístico. 

Este modelo de aprendizaje automático se entrenó con aproximadamente 3936 datos reunidos de una base de información de sintomatología clínica. El conjunto de datos está disponible públicamente en el repositorio Kaggle, en el siguiente enlace: https://www.kaggle.com/datasets/kaushil268/disease-predictionusing-machine-learning; dispone de 4920 muestras y 132 características de síntomas clínicos que abarcan desde dolores físicos hasta signos de comportamiento. 

Entre tanto, para el despliegue del modelo en producción, se generó un aplicación que puede ser consultada en el archivo `app.py`. Este archivo usa el conjunto de datos almacenado en la carpeta `data` y el modelo de aprendizaje autómatico guardado y entrenado previamente en la carpeta `models`. 

* Se debe destacar que el modelo de aprendizaje automático abordado en este proyecto tiene un desempeño adecuado, con una precisión aproximada del 98 %. 

## Tecnologías

La aplicación `app.py` esta desarrollada en `Python`, mientras que la interfaz de usuario esta creada con `Streamlit`. Por otro lado, el modelo de aprendizaje automático fue diseñado usando el módulo `scikit-learn` y se implementaron algunas librerías como `pandas`, `numpy` and `polars`, para manipular y cargar los datos, crear y operar matrices multidimensionales.

## Modelo en producción con servidor remoto

El proyecto fue subido a la nube usando Microsoft Azure. Puede acceder al mismo con el siguiente enlace: http://djmdiseaseapp.australiasoutheast.cloudapp.azure.com:8080
