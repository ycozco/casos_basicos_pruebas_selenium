# test_cp004.py
"""
Prueba CP004: Crear curso con auto-detección de zona horaria
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from driver_setup import get_driver

target_url = 'https://teammatesv4.appspot.com/web/instructor/courses?isAddNewCourse=true'

def abrir_formulario(driver, wait):
    print('Abriendo formulario de nuevo curso...')
    driver.get(target_url)
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'course-id')))
        print('Formulario cargado correctamente.')
    except Exception as e:
        print('Error al cargar el formulario:', e)

def test_cp004_auto_timezone():
    print('\n[CP004] Prueba: Crear curso con auto-detección de zona horaria')
    driver = get_driver()
    wait = WebDriverWait(driver, 5)
    abrir_formulario(driver, wait)
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
    finally:
        driver.quit()
        print('Driver cerrado.')

if __name__ == '__main__':
    test_cp004_auto_timezone()
