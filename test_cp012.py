# test_cp012.py
"""
Prueba CP012: Inscripción masiva de 120 estudiantes usando spreadsheet y archivo CSV
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from driver_setup import get_driver
import csv

# URL de enroll para el curso de ejemplo
course_id = 'CP004-T02-0819-20250619-1908-19'
target_url = f'https://teammatesv4.appspot.com/web/instructor/courses/enroll?courseid={course_id}'

def test_cp012_enroll_120_students():
    print('\n[CP012] Prueba: Inscripción masiva de 120 estudiantes en 2 secciones')
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(target_url)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'htCore')))
        print('Página de enroll cargada.')
        # Leer datos del CSV
        datos = []
        with open('students_cp012.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                datos.append(row)
        print(f'Se leerán {len(datos)} filas del CSV.')
        from selenium.webdriver.common.keys import Keys
        for row_idx, row in enumerate(datos):
            if len(row) != 5:
                raise ValueError(f'Fila {row_idx+1} no tiene 5 columnas: {row}')
            cell = driver.find_element(By.XPATH, f"//table[contains(@class,'htCore')]/tbody/tr[{row_idx+1}]/td[1]")
            cell.click()
            time.sleep(0.05)
            driver.switch_to.active_element.send_keys(row[0])
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[1])
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[2])
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[3])
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[4])
        print('Datos escritos celda por celda en el spreadsheet.')
        enroll_btn = driver.find_element(By.ID, 'btn-enroll')
        enroll_btn.click()
        print('Botón Enroll Students clickeado.')
        try:
            success = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body, .alert-success')))
            print('Resultado CP012:', success.text)
        except Exception:
            print('Resultado CP012: No se encontró mensaje de éxito.')
        time.sleep(2)
    except Exception as e:
        print('Error en CP012:', e)
    finally:
        driver.quit()
        print('Driver cerrado.')

if __name__ == '__main__':
    test_cp012_enroll_120_students()
