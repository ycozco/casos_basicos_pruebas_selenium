# test_cp002.py
"""
Prueba CP002: Crear curso con Course ID único (simula duplicado si lo deseas)
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

def test_cp002_curso_id_duplicado():
    print('\n[CP002] Prueba: Crear curso con Course ID único')
    driver = get_driver()
    wait = WebDriverWait(driver, 5)
    abrir_formulario(driver, wait)
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M-%S')
    min_sec = now.strftime('%M:%S')
    course_id = f'CP002-T01-{min_sec.replace(":", "")}-{timestamp.replace(":", "")}'
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
    finally:
        driver.quit()
        print('Driver cerrado.')

if __name__ == '__main__':
    test_cp002_curso_id_duplicado()
