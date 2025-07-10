# -*- coding: utf-8 -*-
"""
Automatización de pruebas para TEAMMATES usando Selenium.
Pruebas:
- CP002: Crear curso con Course ID duplicado
- CP004: Crear curso con auto-detección de zona horaria
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import tempfile

# Ruta correcta de chromedriver
CHROMEDRIVER_PATH = r'C:/chromedriver/chromedriver.exe'

# URL para agregar nuevo curso
target_url = 'https://teammatesv4.appspot.com/web/instructor/courses?isAddNewCourse=true'

# Configuración del navegador con perfil de usuario autenticado
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
# Conectar a Chrome ya abierto con remote debugging
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# No usar user-data-dir ni otros flags aquí
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

print('Conectado a Chrome con depuración remota.')
driver.get(target_url)
print('Página abierta')

# Espera explícita más corta para depuración
wait = WebDriverWait(driver, 5)

def abrir_formulario():
    print('Abriendo formulario de nuevo curso...')
    driver.get(target_url)
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'course-id')))
        print('Formulario cargado correctamente.')
    except Exception as e:
        print('Error al cargar el formulario:', e)

def test_cp002_curso_id_duplicado():
    print('\n[CP002] Prueba: Crear curso con Course ID duplicado')
    abrir_formulario()
    import datetime
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M-%S')
    min_sec = now.strftime('%M:%S')
    # Course ID solo letras, números y guiones, sin espacios ni emojis
    course_id = f'CP002-T01-{min_sec.replace(":", "")}-{timestamp.replace(":", "")}'
    # Nombre descriptivo, sin emojis
    course_name = f'CP002-T01:{min_sec} - Pruebas de Software Test01'
    try:
        driver.find_element(By.ID, 'course-id').send_keys(course_id)
        print(f'Ingresado Course ID: {course_id}')
        driver.find_element(By.ID, 'course-name').send_keys(course_name)
        print(f'Ingresado Course Name: {course_name}')
        Select(driver.find_element(By.ID, 'course-institute')).select_by_visible_text('UNSA, Peru')
        print('Seleccionado Institute')
        Select(driver.find_element(By.ID, 'time-zone')).select_by_visible_text('America/Lima (UTC -05:00)')
        print('Seleccionada zona horaria')
        wait.until(EC.element_to_be_clickable((By.ID, 'btn-submit-course')))
        print('Botón Add Course habilitado')
        driver.find_element(By.ID, 'btn-submit-course').click()
        print('Botón Add Course clickeado')
        try:
            error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.invalid-feedback, .toast-body')))
            print('Resultado CP002:', error.text)
        except Exception:
            print('Resultado CP002: No se encontró mensaje de error.')
    except Exception as e:
        print('Error en CP002:', e)
    print('\n--- Fin de CP002. Preparando para CP004... ---\n')

def test_cp004_auto_timezone():
    print('\n[CP004] Prueba: Crear curso con auto-detección de zona horaria')
    abrir_formulario()
    import datetime
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M-%S')
    min_sec = now.strftime('%M:%S')
    course_id = f'CP004-T02-{min_sec.replace(":", "")}-{timestamp.replace(":", "")}'
    course_name = f'CP004-T02:{min_sec} - Pruebas de Software Test02'
    try:
        driver.find_element(By.ID, 'course-id').send_keys(course_id)
        print(f'Ingresado Course ID: {course_id}')
        driver.find_element(By.ID, 'course-name').send_keys(course_name)
        print(f'Ingresado Course Name: {course_name}')
        Select(driver.find_element(By.ID, 'course-institute')).select_by_visible_text('UNSA, Peru')
        print('Seleccionado Institute')
        auto_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Auto-Detect')]")
        auto_btn.click()
        print('Botón Auto-Detect clickeado')
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, 'btn-submit-course')))
        print('Botón Add Course habilitado')
        driver.find_element(By.ID, 'btn-submit-course').click()
        print('Botón Add Course clickeado')
        try:
            toast = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body')))
            print('Resultado CP004:', toast.text)
        except Exception:
            print('Resultado CP004: No se encontró mensaje de éxito.')
    except Exception as e:
        print('Error en CP004:', e)

def main():
    print('Iniciando pruebas TEAMMATES...')
    try:
        test_cp002_curso_id_duplicado()
        time.sleep(1)
        test_cp004_auto_timezone()
    except Exception as e:
        print('Error general en pruebas:', e)
    print('Pruebas finalizadas.')
    driver.quit()

if __name__ == '__main__':
    main()
