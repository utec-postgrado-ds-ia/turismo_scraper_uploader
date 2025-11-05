import pandas as pd
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from pprint import pprint
from flask import Flask, jsonify, request
import boto3
import os

app = Flask(__name__)

@app.route("/generar-scraping", methods=["POST"])
def generar_scraping():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        url_pagina = "https://www.ytuqueplanes.com/rutas-cortas"
        driver.get(url_pagina)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.swiper-slide article.card-poster"))
        )

        slides = driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide article.card-poster")
        detalle_urls = []
        for slide in slides:
            try:
                a_tag = slide.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")
                if href:
                    detalle_urls.append(href)
            except:
                continue

        data = []

        for url in detalle_urls:
            driver.get(url)

            ruta_turistica = region = nombre_ruta = numero_lugares = ""

            try:
                h2_tag = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h2.card-poster__titulo"))
                )
                ruta_turistica = h2_tag.text.strip()
                partes = ruta_turistica.split("\n", 1)
                region = partes[0] if len(partes) > 0 else ""
                nombre_ruta = partes[1] if len(partes) > 1 else ""
            except:
                pass

            try:
                span_tag = driver.find_element(By.CSS_SELECTOR, "span.boton strong")
                numero_lugares = ''.join(filter(str.isdigit, span_tag.text)) if span_tag else ""
            except:
                pass

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.wrapper-first-right-list-item"))
                )
                time.sleep(1)
                items = driver.find_elements(By.CSS_SELECTOR, "div.wrapper-first-right-list-item")
            except TimeoutException:
                items = []

            for item in items:
                nombre_sitio = item.get_attribute("data-name")
                lat = item.get_attribute("data-lat")
                lng = item.get_attribute("data-lng")

                descripcion = ""
                try:
                    desc_elem = item.find_element(By.CSS_SELECTOR, "p.wflitem-apt-description")
                    descripcion = desc_elem.text.strip()
                except:
                    pass

                actividades = []
                try:
                    acts = item.find_elements(By.CSS_SELECTOR, "ul.wflitem-activity-list li span")
                    actividades = [act.text.strip() for act in acts if act.text.strip()]
                except:
                    pass

                recomendado = []
                try:
                    recs = item.find_elements(By.CSS_SELECTOR, "ul.wflitem-apt-list li")
                    recomendado = [rec.text.strip() for recs in recs if recs.text.strip()]
                except:
                    pass

                imagen_url = ""
                try:
                    img = item.find_element(By.CSS_SELECTOR, "ul.wflitem-activity-list li img")
                    imagen_url = img.get_attribute("src")
                except:
                    pass

                fila = {
                    "extraccion_id": str(uuid.uuid4()),
                    "ruta_turistica": ruta_turistica,
                    "region": region,
                    "nombre_ruta": nombre_ruta,
                    "url": url,
                    "numero_lugares": numero_lugares,
                    "subsitio_nombre": nombre_sitio,
                    "lat": lat,
                    "lng": lng,
                    "descripcion": descripcion,
                    "imagen_url": imagen_url,
                    "actividades": ", ".join(actividades),
                    "recomendado": ", ".join(recomendado),
                    "fecha_extraccion": datetime.now().strftime("%Y-%m-%d")
                }

                data.append(fila)

        driver.quit()

        df = pd.DataFrame(data)
        filename = "rutas_turisticas_destacadas.csv"
        df.to_csv(filename, index=False)

        s3 = boto3.client("s3")
        bucket_name = "turismo-datalake-31102025"
        key = f"raw/lugar_turistico/rutas_turisticas_destacadas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        s3.upload_file(filename, bucket_name, key)

        return jsonify({
            "status": "ok",
            "message": f"Archivo subido correctamente a s3://{bucket_name}/{key}",
            "total_registros": len(data)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
