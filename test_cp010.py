# test_cp010.py
"""
Prueba CP010: Inscripción masiva de estudiantes usando spreadsheet
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

def test_cp010_enroll_students():
    print('\n[CP010] Prueba: Inscripción masiva de estudiantes')
    driver = get_driver()
    wait = WebDriverWait(driver, 7)
    driver.get(target_url)
    try:
        # Esperar a que cargue la tabla Handsontable
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'htCore')))
        print('Página de enroll cargada.')
        # Datos tabulados de ejemplo (lista de listas)
        datos = [
            ['Tutorial Group 1', 'Team 1', 'Alice Brown', 'alice.brown1@unsa.edu.pe', ''],
            ['Tutorial Group 1', 'Team 2', 'Bob Smith', 'bob.smith2@unsa.edu.pe', ''],
            ['Tutorial Group 1', 'Team 3', 'Carol White', 'carol.white3@unsa.edu.pe', ''],
            ['Tutorial Group 1', 'Team 4', 'David Lee', 'david.lee4@unsa.edu.pe', ''],
            ['Tutorial Group 1', 'Team 5', 'Eva Torres', 'eva.torres5@unsa.edu.pe', ''],
            ['Tutorial Group 2', 'Team 6', 'Frank Miller', 'frank.miller6@unsa.edu.pe', ''],
            ['Tutorial Group 2', 'Team 7', 'Grace Kim', 'grace.kim7@unsa.edu.pe', ''],
            ['Tutorial Group 2', 'Team 8', 'Henry Zhao', 'henry.zhao8@unsa.edu.pe', ''],
            ['Tutorial Group 2', 'Team 9', 'Irene Chen', 'irene.chen9@unsa.edu.pe', ''],
            ['Tutorial Group 2', 'Team 10', 'Jack Black', 'jack.black10@unsa.edu.pe', ''],
            ['Tutorial Group 3', 'Team 11', 'Karen Wong', 'karen.wong11@unsa.edu.pe', ''],
            ['Tutorial Group 3', 'Team 12', 'Luis Perez', 'luis.perez12@unsa.edu.pe', ''],
            ['Tutorial Group 3', 'Team 13', 'Maria Lopez', 'maria.lopez13@unsa.edu.pe', ''],
            ['Tutorial Group 3', 'Team 14', 'Nina Patel', 'nina.patel14@unsa.edu.pe', ''],
            ['Tutorial Group 3', 'Team 15', 'Oscar Diaz', 'oscar.diaz15@unsa.edu.pe', ''],
            ['Tutorial Group 4', 'Team 16', 'Paula Ruiz', 'paula.ruiz16@unsa.edu.pe', ''],
            ['Tutorial Group 4', 'Team 17', 'Quentin Yu', 'quentin.yu17@unsa.edu.pe', ''],
            ['Tutorial Group 4', 'Team 18', 'Rosa Silva', 'rosa.silva18@unsa.edu.pe', ''],
            ['Tutorial Group 4', 'Team 19', 'Samuel Vega', 'samuel.vega19@unsa.edu.pe', ''],
            ['Tutorial Group 4', 'Team 20', 'Tania Cruz', 'tania.cruz20@unsa.edu.pe', '']
        ]
        # Esperar a que haya al menos una fila y una celda editable
        from selenium.webdriver.common.keys import Keys
        cell_clicked = False
        # Siempre empezar en la segunda columna (Section)
        try:
            first_cell = driver.find_element(By.XPATH, "//table[contains(@class,'htCore')]/tbody/tr[1]/td[2]")
            first_cell.click()
            cell_clicked = True
        except Exception:
            print('No se encontró una celda editable en la tabla. Revisa si hay filas disponibles.')
        if not cell_clicked:
            raise Exception('No se pudo hacer clic en la celda editable. Abortando prueba.')
        time.sleep(0.5)
        for row_idx, row in enumerate(datos):
            # Validar que la fila tenga exactamente 5 elementos
            if len(row) != 5:
                raise ValueError(f'Fila {row_idx+1} no tiene 5 columnas: {row}')
            # Hacer clic en la celda Section de la fila correspondiente (td[2])
            cell = driver.find_element(By.XPATH, f"//table[contains(@class,'htCore')]/tbody/tr[{row_idx+1}]/td[1]")
            cell.click()
            time.sleep(0.1)
            from selenium.webdriver.common.keys import Keys
            # Escribir Section
            driver.switch_to.active_element.send_keys(row[0])
            # Escribir Team
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[1])
            # Escribir Name
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[2])
            # Escribir Email
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[3])
            # Escribir Comments
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(row[4])
        print('Datos escritos celda por celda en el spreadsheet.')
        # Hacer clic en Enroll Students
        enroll_btn = driver.find_element(By.ID, 'btn-enroll')
        enroll_btn.click()
        print('Botón Enroll Students clickeado.')
        # Esperar mensaje de éxito
        try:
            success = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.toast-body, .alert-success')))
            print('Resultado CP010:', success.text)
        except Exception:
            print('Resultado CP010: No se encontró mensaje de éxito.')
        time.sleep(2)
    except Exception as e:
        print('Error en CP010:', e)
    finally:
        driver.quit()
        print('Driver cerrado.')

if __name__ == '__main__':
    test_cp010_enroll_students()
