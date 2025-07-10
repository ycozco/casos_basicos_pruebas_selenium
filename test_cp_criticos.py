# test_cp_criticos.py
"""
Pruebas críticas automatizadas para TEAMMATES (muestreo representativo)
Incluye:
- CP010: Buscar estudiante por nombre
- CP012: Agregar instructor con permisos Co-owner
- CP015: Crear sesión con plantilla team peer feedback (point-based)
- CP016: Crear sesión vacía con preguntas personalizadas
- CP056: Crear curso con nombre de longitud máxima
- CP060: Crear sesión de feedback con nombre vacío
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from driver_setup import get_driver

# Configuración global para el curso y las URLs base
COURSE_ID = 'CP004-T02-0819-20250619-1908-19'
BASE_URL = 'https://teammatesv4.appspot.com/web/instructor'

# --- CP010: Buscar estudiante por nombre ---
def test_cp010_buscar_estudiante():
    print('\n[CP010] Buscar estudiante por nombre')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    try:
        url = f"{BASE_URL}/courses/students?courseid={COURSE_ID}"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'student-search-box')))
        search_box = driver.find_element(By.ID, 'student-search-box')
        search_box.clear()
        search_box.send_keys('Alice')
        search_box.submit()
        time.sleep(2)
        results = driver.find_elements(By.CSS_SELECTOR, '.student-row')
        print(f'Resultados encontrados: {len(results)}')
        for r in results:
            print(r.text)
    except Exception as e:
        print('Error en CP010:', e)
    finally:
        driver.quit()

# --- CP012: Agregar instructor con permisos Co-owner ---
def test_cp012_agregar_instructor_coowner():
    print('\n[CP012] Agregar instructor Co-owner')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    try:
        url = f"{BASE_URL}/courses/edit?courseid={COURSE_ID}"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'add-instructor-form')))
        driver.find_element(By.ID, 'instructorname').send_keys('Dr. Carlos Mendoza')
        driver.find_element(By.ID, 'instructoremail').send_keys('carlos.mendoza@unsa.edu.pe')
        driver.find_element(By.ID, 'instructordisplayname').send_keys('Dr. Mendoza')
        # El rol se selecciona por visible text si es un <select>, si no, por send_keys
        try:
            Select(driver.find_element(By.ID, 'instructorrole')).select_by_visible_text('Co-owner')
        except Exception:
            driver.find_element(By.ID, 'instructorrole').send_keys('Co-owner')
        driver.find_element(By.ID, 'btn-add-instructor').click()
        time.sleep(2)
        try:
            success = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body, .alert-success')))
            print('Resultado CP012:', success.text)
        except Exception:
            print('Resultado CP012: No se encontró mensaje de éxito.')
    except Exception as e:
        print('Error en CP012:', e)
    finally:
        driver.quit()

# --- CP015: Crear sesión con plantilla team peer feedback (point-based) ---
def test_cp015_crear_sesion_plantilla():
    print('\n[CP015] Crear sesión con plantilla team peer feedback (point-based)')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    try:
        url = f"{BASE_URL}/sessions/add?courseid={COURSE_ID}"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'session-template-dropdown')))
        Select(driver.find_element(By.ID, 'session-template-dropdown')).select_by_visible_text('team peer feedback (point-based)')
        driver.find_element(By.ID, 'session-name').send_keys('Evaluación Proyecto 1')
        driver.find_element(By.ID, 'instructions').send_keys('Por favor evalúe a sus compañeros')
        driver.find_element(By.ID, 'btn-create-session').click()
        time.sleep(2)
        try:
            success = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body, .alert-success')))
            print('Resultado CP015:', success.text)
        except Exception:
            print('Resultado CP015: No se encontró mensaje de éxito.')
    except Exception as e:
        print('Error en CP015:', e)
    finally:
        driver.quit()

# --- CP016: Crear sesión vacía con preguntas personalizadas ---
def test_cp016_crear_sesion_vacia():
    print('\n[CP016] Crear sesión vacía con preguntas personalizadas')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    try:
        url = f"{BASE_URL}/sessions/add?courseid={COURSE_ID}"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'session-template-dropdown')))
        Select(driver.find_element(By.ID, 'session-template-dropdown')).select_by_visible_text('session with my own questions')
        driver.find_element(By.ID, 'session-name').send_keys('Feedback Personalizado')
        driver.find_element(By.ID, 'instructions').send_keys('Responda con honestidad')
        driver.find_element(By.ID, 'btn-create-session').click()
        time.sleep(2)
        try:
            success = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body, .alert-success')))
            print('Resultado CP016:', success.text)
        except Exception:
            print('Resultado CP016: No se encontró mensaje de éxito.')
    except Exception as e:
        print('Error en CP016:', e)
    finally:
        driver.quit()

# --- CP056: Crear curso con nombre de longitud máxima ---
def test_cp056_curso_nombre_max():
    print('\n[CP056] Crear curso con nombre de longitud máxima')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    try:
        url = f"{BASE_URL}/courses?isAddNewCourse=true"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'course-id')))
        driver.find_element(By.ID, 'course-id').send_keys('CP056-MAX-LEN-20250619')
        max_name = 'A' * 96
        driver.find_element(By.ID, 'course-name').send_keys(max_name)
        Select(driver.find_element(By.ID, 'course-institute')).select_by_visible_text('UNSA, Peru')
        Select(driver.find_element(By.ID, 'time-zone')).select_by_visible_text('America/Lima (UTC -05:00)')
        driver.find_element(By.ID, 'btn-submit-course').click()
        time.sleep(2)
        try:
            success = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body, .alert-success')))
            print('Resultado CP056:', success.text)
        except Exception:
            print('Resultado CP056: No se encontró mensaje de éxito.')
    except Exception as e:
        print('Error en CP056:', e)
    finally:
        driver.quit()

# --- CP060: Crear sesión de feedback con nombre vacío ---
def test_cp060_sesion_nombre_vacio():
    print('\n[CP060] Crear sesión de feedback con nombre vacío')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    try:
        url = f"{BASE_URL}/sessions/add?courseid={COURSE_ID}"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'session-template-dropdown')))
        Select(driver.find_element(By.ID, 'session-template-dropdown')).select_by_visible_text('session with my own questions')
        driver.find_element(By.ID, 'session-name').clear()
        driver.find_element(By.ID, 'instructions').send_keys('Instrucciones de prueba')
        driver.find_element(By.ID, 'btn-create-session').click()
        time.sleep(2)
        try:
            error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.invalid-feedback, .toast-body, .alert-danger')))
            print('Resultado CP060:', error.text)
        except Exception:
            print('Resultado CP060: No se encontró mensaje de error.')
    except Exception as e:
        print('Error en CP060:', e)
    finally:
        driver.quit()

if __name__ == '__main__':
    test_cp010_buscar_estudiante()
    test_cp012_agregar_instructor_coowner()
    test_cp015_crear_sesion_plantilla()
    test_cp016_crear_sesion_vacia()
    test_cp056_curso_nombre_max()
    test_cp060_sesion_nombre_vacio()
