# 🕸️ scraping_to_s3.py

Script en **Python** que realiza *web scraping* del portal oficial de turismo del Perú,  
**[Y Tú Qué Planes (https://www.ytuqueplanes.com/rutas-cortas)](https://www.ytuqueplanes.com/rutas-cortas)**,  
extrayendo información sobre **rutas y lugares turísticos destacados**.  

El script genera un archivo CSV con los datos recolectados y lo sube automáticamente a un bucket **Amazon S3**,  
formando parte de la capa **Storage Layer** dentro de una arquitectura **Data Lakehouse**.

---

## 🚀 Características

- 🌐 Extrae datos reales desde **ytuqueplanes.com/rutas-cortas**.  
- 🧾 Crea automáticamente un CSV con información de rutas, regiones, coordenadas y descripciones.  
- ☁️ Sube los resultados al bucket **Amazon S3** configurado.  
- ⚙️ Código fácil de adaptar a otros portales turísticos o fuentes.  
- 🧠 Ideal como fuente de datos para **AWS Glue (Catalog Layer)** y **Athena (Consumption Layer)**.  

---

## ⚙️ Requisitos

- **Python 3.9+**
- **Google Chrome** y **ChromeDriver** instalados  
- **AWS CLI** configurado o credenciales IAM en el entorno  
- Librerías necesarias (instalar con pip):

```bash
pip install selenium boto3 pandas
