import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor
import numpy as np




# Esta función realizará la consulta para una porción del DataFrame
def consultar_numeros(parte_df):
    options = Options()
    options.headless = True
    driver_path = r"C:\Users\Magellan Banyuls\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver=webdriver.Chrome(service=service, options=options)
    
    
    for index, row in parte_df.iterrows():
        

        # Entrar a la web con usuario y contraseña
        driver.get("http://iris.tmoviles.com.ar/workspace/faces/jsf/workspace/workspace.xhtml")
                
        # Esperar a que la página cargue completamente
        time.sleep(2)

        # Ingresar usuario y contraseña
        user= "Aqui va el usuario"
        usuario_input=driver.find_element(By.ID, "loginForm:workspace_login_user_name")
        usuario_input.send_keys(str(user))
        passw= "Aqui va la contraseña"
        pass_input=driver.find_element(By.ID, "loginForm:workspace_login_password")
        pass_input.send_keys(str(passw))
        inicio_sesion= driver.find_element(By.ID,"loginForm:submitbutton")
        inicio_sesion.click()

        time.sleep(3)

        # Abrir consulta de operacion para entrar a consultar cada numero
        consulta_operacion_button = driver.find_element(By.ID, "portletComponentApplications_menuActionNormalModeApplications__id185_4_applicationButton")

        consulta_operacion_button.click()
                
        # Esperar 2 segundos
        time.sleep(2)
        # Cambiar al iframe con el id "executionPanelApplications"
        iframe = driver.find_element(By.ID, "executionPanelApplications")
        driver.switch_to.frame(iframe)


        # Iterar sobre cada fila del DataFrame
        for index, row in parte_df.iterrows():
            estado = row['Estado']
            telefono = row['Recurso']
            checked = row['Revisado']

            # Verificar si el estado no es "Activo"
            if estado != 'Activo' and checked == 'No' :
                # Escribir el número de teléfono en el campo correspondiente
                numero_input = driver.find_element(By.ID, "att$nroLinea")
                numero_input.send_keys(int(telefono))
                
                # Hacer clic en el botón "Consultar"
                consultar_button = driver.find_element(By.ID, "button6_comp")
                consultar_button.click()
                
                # Esperar a que la tabla cargue (2 segundos)
                time.sleep(2)
                
                # Verificar si el texto "Port Out" está presente en la página
                texto_port_out = driver.find_elements(By.CLASS_NAME, "fo_text")
                if any("Port Out" in elemento.text for elemento in texto_port_out):
                    # Hacero dos click en fecha para poner el ultimo port out primero
                    fecha_alta = driver.find_element(By.ID, "array1_5_header")
                    fecha_alta.click()
                    time.sleep(0.9)
                    fecha_alta = driver.find_element(By.ID, "array1_5_header")
                    fecha_alta.click()

                    time.sleep(0.9)
                    

                    # Hacer clic en el enlace de detalle
                    detalle_link = driver.find_element(By.ID, "detalle_comp")
                    detalle_link.click()
                    
                    # Esperar a que la página de detalle cargue (2 segundos)
                    time.sleep(2)
                    
                    try:
                        # Obtener el operador del detalle
                        print("Buscando el operador...")
                        operador_div = driver.find_element(By.ID, "operador_comp")
                        operador_texto = operador_div.find_element(By.CLASS_NAME, "fo_text").text
                    
                        # Actualizar el operador en la columna "Operador" del DataFrame
                        if "Claro" in operador_texto:
                            df.at[index, 'Operador'] = "Claro"
                        elif "Personal" in operador_texto:
                            df.at[index, 'Operador'] = "Personal"

                        # Obtener fecha de alta
                        elemento = driver.find_element(By.ID, "att$fechaAlta")
                        fecha_texto = elemento.get_attribute("value")
                        # Extraer solo la fecha
                        fecha = fecha_texto.split("$")[1].split(" ")[0]

                        # Actualizar fecha de alta
                        df.at[index, 'Fecha de Alta'] = str(fecha)

                        # Vuelta exitosa
                        volver1 = driver.find_element(By.ID, "att$button0") # Salir del formulario con datos
                        volver1.click()
                        time.sleep(0.5)
                        volver2 = driver.find_element(By.ID, "att$button0") # Salir de seccion de Port Out 
                        volver2.click()
                        time.sleep(0.5)
                        # Volver a localizar el número input
                        numero_input = driver.find_element(By.ID, "att$nroLinea")
                        numero_input.clear() # Limpiar la celda para próximo bucle
                        time.sleep(0.5)
                    
                    except NoSuchElementException:
                        try:
                            print("Buscando boton volver")
                            volver1 = driver.find_element(By.ID, "att$button0")  # Salir del formulario con datos
                            volver1.click()
                            time.sleep(0.5)
                            volver2 = driver.find_element(By.ID, "att$button0")  # Salir de sección de Port Out
                            volver2.click()
                            time.sleep(0.5)
                            # Volver a localizar el número input
                            numero_input = driver.find_element(By.ID, "att$nroLinea")
                            numero_input.clear()  # Limpiar la celda para próximo bucle
                            time.sleep(0.5)
                            

                        except NoSuchElementException:
                            

                            # Continuar con el código si no se encuentra el elemento de error
                            driver.switch_to.default_content()
                            print("buscando boton cerrar...")
                            cerrar_btn = driver.find_element(By.ID, "portletComponentApplications_menuActionNormalModeApplications_executionDialogViewApplications_executionDialogApplications_CloseButton")
                            cerrar_btn.click()
                            # Esperar que cargue
                            time.sleep(2)

                            # Abrir consulta de operacion para entrar a consultar cada numero
                            consulta_operacion_button = driver.find_element(By.ID, "portletComponentApplications_menuActionNormalModeApplications__id185_4_applicationButton")
                            consulta_operacion_button.click()

                            # Esperar
                            time.sleep(2)
                            # Cambiar al iframe con el id "executionPanelApplications"
                            iframe = driver.find_element(By.ID, "executionPanelApplications")
                            driver.switch_to.frame(iframe)

                # Volver atrás si no es exitoso
                elif not any("Port Out" in elemento.text for elemento in texto_port_out):
                    volver = driver.find_element(By.ID, "att$button0")  # Volver desde antes de entrar a detalle
                    volver.click()
                    time.sleep(0.5)
                    # Volver a localizar el número input
                    numero_input = driver.find_element(By.ID, "att$nroLinea")
                    numero_input.clear()  # Limpiar la celda para próximo bucle
                    time.sleep(0.5)

            # Checkear el numero para no buscarlo de vuelta
            df.at[index, 'Revisado'] = "Si"
            # Guardar el DataFrame actualizado en un nuevo archivo CSV
            df.to_csv(archivo_csv, index=False, sep=";")
                
        # Cerrar el navegador
        driver.quit()




# Ruta del archivo CSV
archivo_csv = r"C:\Users\Magellan Banyuls\Desktop\Numeros INACTIVOS\base_12_revisado_final.csv"

# Leer el archivo CSV con Pandas
df = pd.read_csv(archivo_csv, sep=";", engine="python", on_bad_lines='skip')

# Verificar si las columnas "Operador", "Fecha de Alta" y "Revisado" ya existen en el DataFrame
if 'Operador' not in df.columns:
    df['Operador'] = ''

if 'Fecha de Alta' not in df.columns:
    df['Fecha de Alta'] = ''

if 'Revisado' not in df.columns:
    df['Revisado'] = 'No'

# Dividir el DataFrame en partes para distribuir entre los hilos
num_threads = 40
particiones = np.array_split(df, num_threads)

# Configurar el número máximo de hilos
max_workers = 40

# Crear un ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []

    # Lanzar una tarea para cada porción del DataFrame
    for parte_df in particiones:
        future = executor.submit(consultar_numeros, parte_df)
        futures.append(future)

    # Esperar a que todas las tareas se completen
    for future in futures:
        future.result()

