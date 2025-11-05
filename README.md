# 🕸️ Turismo Scraper Uploader

Script en **Python + Flask** que realiza *web scraping* del portal oficial de turismo del Perú  
👉 [Y Tú Qué Planes](https://www.ytuqueplanes.com/rutas-cortas),  
extrayendo información sobre **rutas, regiones y lugares turísticos**,  
y subiendo automáticamente los resultados a un bucket **Amazon S3** dentro de AWS.  

Este proceso representa la **Raw Layer (Storage Layer)** dentro de una arquitectura **Data Lakehouse**.

---

## 🚀 Características

- 🌐 Extrae datos reales desde *ytuqueplanes.com/rutas-cortas* usando **Selenium**.  
- 🧾 Genera un archivo CSV con información sobre rutas, coordenadas y descripciones.  
- ☁️ Sube automáticamente el CSV al bucket **S3** configurado.  
- 🧠 Ideal como fuente para **AWS Glue (Catalog Layer)** y **Athena (Consumption Layer)**.  
- ⚙️ Se puede invocar fácilmente desde **Postman** mediante una llamada HTTP.

---

## ⚙️ Requisitos

- **Instancia EC2 (Ubuntu 22.04 o superior)**
- **Python 3.10+**
- **Rol IAM:** `LabRole` (con acceso a S3)
- **Google Chrome** y **ChromeDriver** instalados
- **Librerías Python:** `Flask`, `Selenium`, `Boto3`, `Pandas`, `WebDriver-Manager`

---

## 🧩 Pasos de instalación en EC2

### 1️⃣ Abrir la consola

- En la consola AWS, ve a **EC2 → Instances → selecciona tu instancia → Connect**  
- Usa la pestaña **Session Manager** y haz clic en **Connect** para abrir la terminal web.

---

### 2️⃣ Instalar dependencias básicas
```bash
sudo apt update -y
sudo apt install git python3-pip -y
```

---

### 3️⃣ Clonar el repositorio
```bash
git clone https://github.com/utec-postgrado-ds-ia/turismo_scraper_uploader.git
cd turismo_scraper_uploader
```

Verifica que el script esté presente:
```bash
ls
```
Deberías ver:
```
scraping_api.py
README.md
```

---

### 4️⃣ Crear e instalar dependencias del scraping

Crea el archivo `requirements.txt` (si no existe):
```bash
echo "flask
pandas
boto3
selenium
webdriver-manager" > requirements.txt
```

Instala todo:
```bash
pip install -r requirements.txt
```

---

### 5️⃣ Instalar Google Chrome y ChromeDriver

Instala Chrome:
```bash
sudo apt install unzip -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

⚙️ Ahora instala el ChromeDriver correcto (ajustado a tu versión 142.0.7444.59):
```bash
CHROME_VERSION=142.0.7444.59
wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
```

---

### 6️⃣ Ejecutar el servidor Flask
```bash
python3 scraping_api.py
```

Si todo está correcto, deberías ver:
```
* Running on http://0.0.0.0:5000
```

---

## 🧪 Cómo probar con Postman

1. Abre el puerto **5000** en tu **Security Group**  
   *(Inbound Rule → Custom TCP → 5000 → 0.0.0.0/0)*  
2. Obtén la **IP pública** de tu instancia (por ejemplo: `3.84.125.40`)  
3. En **Postman**, crea una nueva petición:

   - **Método:** `POST`  
   - **URL:** `http://<tu-ip-ec2>:5000/generar-scraping`  
   - **Body:** vacío  

4. Presiona **Send**. Si todo sale bien, obtendrás una respuesta como:
```json
{
    "status": "ok",
    "message": "Archivo subido correctamente a s3://turismo-datalake-31102025/raw/lugar_turistico/lugares_turisticos_20251031_123000.csv",
    "total_registros": 128
}
```

---

## 🪣 Bucket S3 esperado

**Bucket:** `turismo-datalake-31102025`

**Estructura recomendada:**
```
turismo-datalake-31102025/
│
├── raw/
│   └── lugar_turistico/
│       └── lugares_turisticos_<fecha>.csv
│
├── silver/
└── gold/
```

---

## 💡 Notas finales

- Este scraper está pensado para uso académico y demostrativo dentro del curso de **AWS Data Lakehouse (UTEC)**.  
- Puede ampliarse fácilmente para incluir más fuentes de datos (por ejemplo, **bases de datos o APIs**).  
- No requiere configurar credenciales IAM: el **LabRole** del entorno de UTEC ya tiene los permisos necesarios para S3.