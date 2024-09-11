# Data_Engineer entrega final

**NOTA:**  Renombrar el archivo `.env` (elimina el guion bajo `_` del nombre del archivo), y llenar las variables correspondientes

Para arrancar el proyecto escribir en la terminal

  ```bash
    docker-comnpose up
  ```

## Descripción del Proyecto

Este proyecto de ingeniería de datos está diseñado para extraer, transformar y cargar datos financieros en una base de datos Redshift utilizando Apache Airflow para la orquestación de tareas.

### Funcionamiento del Proyecto

1. **Extracción de Datos**: Los datos financieros se extraen desde la API de Twelve Data. Esta etapa obtiene los datos más recientes para una serie de símbolos de acciones y ETFs definidos en la configuración.

2. **Transformación de Datos**: Los datos extraídos son transformados para ajustarse al formato requerido, incluyendo la generación de identificadores únicos y la adición de columnas como la fecha de ingestión.

3. **Carga de Datos**: Los datos transformados se cargan en una base de datos Redshift. Se maneja la creación de la tabla necesaria, la inserción en bloques y la eliminación de registros duplicados.

4. **Orquestación con Apache Airflow**:
   - **Configuración**: El proyecto utiliza Apache Airflow para gestionar el flujo de trabajo ETL. Este está configurado para ejecutar el proceso diariamente.
   - **Ejecución**: Para probar el funcionamiento del DAG, debes acceder a la interfaz de usuario de Apache Airflow con las credenciales predeterminadas (usuario: `airflow`, contraseña: `airflow`). Desde allí, puedes activar manualmente el DAG para verificar su funcionamiento.

## Estructura del Proyecto

1. **`dags/`**
   - **`etl_dag.py`**: Define el DAG (Directed Acyclic Graph) para Apache Airflow que orquesta el proceso ETL. Utiliza el operador `PythonOperator` para ejecutar la función `etl()` del módulo `main.py` en un intervalo diario.

2. **`modules/`**
   - **`config.py`**: Contiene las variables de configuración y credenciales, incluyendo detalles de conexión a Redshift y la API de Twelve Data. Define los símbolos de acciones y ETFs para la extracción de datos.
   - **`extract.py`**: Contiene la función `extract_data()`, que extrae datos financieros desde la API de Twelve Data y los organiza en un DataFrame de Pandas. Limita la cantidad de registros a los más recientes y maneja errores de extracción.
   - **`transform.py`**: Define la función `transform_data()`, que transforma el DataFrame extraído, renombra columnas, genera un ID único para cada registro y añade columnas adicionales. También maneja errores de transformación.
   - **`load.py`**: Contiene la función `load_data()`, que carga el DataFrame transformado en una tabla en Redshift. Maneja la creación de la tabla, inserción de datos en bloques y evita la inserción de duplicados.
   - **`main.py`**: Define la función `etl()`, que ejecuta el proceso ETL completo: extracción de datos, transformación y carga. También incluye una línea comentada para probar el proceso ETL manualmente.
   - **`redshift_conn.py`**: Contiene la función `connect_redshift()` para manejar la conexión a la base de datos Redshift utilizando `psycopg2`.

3. **`dependencies/`**
   - **`requirements.txt`**: Lista las dependencias necesarias para el proyecto, como `pandas`, `requests`, `psycopg2`, y `apache-airflow`.

4. **`docker-compose.yml`**: Configura los servicios necesarios para el proyecto, incluyendo la base de datos y el entorno de Airflow, utilizando Docker Compose.

5. **`.gitignore`**: Especifica los archivos y directorios que deben ser ignorados por Git, como el entorno virtual y archivos temporales.

6. **`README.md`**: Documento que proporciona una visión general del proyecto, incluyendo instrucciones de uso y detalles de configuración.

## Funciones y tareas del DAG 

El DAG `ETL_NICOLAS_ALARCON` automatiza un proceso ETL (Extracción, Transformación y Carga) de datos financieros. Su propósito es gestionar la extracción de datos, su transformación y carga en el destino final, así como la gestión de archivos temporales.

## Tareas del DAG

1. **Extracción de Datos**
   - **Descripción**: Extrae datos desde la fuente especificada.
   - **Tarea**: `extract_data`

2. **Transformación de Datos**
   - **Descripción**: Lee los datos extraídos y los transforma en el formato adecuado.
   - **Tarea**: `transform_data`

3. **Carga de Datos**
   - **Descripción**: Carga los datos transformados en el destino final.
   - **Tarea**: `load_data`

4. **Verificación de Archivos de Extracción**
   - **Descripción**: Verifica la existencia del archivo de datos extraídos antes de proceder con la transformación.
   - **Tarea**: `extract_file_sensor`

5. **Verificación de Archivos Transformados**
   - **Descripción**: Verifica la existencia del archivo de datos transformados antes de proceder con la carga.
   - **Tarea**: `transform_file_sensor`

6. **Limpieza de Archivos Temporales**
   - **Descripción**: Elimina todos los archivos temporales en el directorio `/tmp` después de la carga de datos.
   - **Tarea**: `cleanup_tmp_files`

## Dependencias

Las tareas están organizadas de manera que:
- La extracción de datos ocurre primero.
- La verificación del archivo de extracción sigue a la extracción de datos.
- La transformación de datos ocurre después de la verificación del archivo de extracción.
- La verificación del archivo transformado sigue a la transformación de datos.
- La carga de datos ocurre después de la verificación del archivo transformado.
- Finalmente, se realiza la limpieza de archivos temporales después de la carga de datos.


## Control de duplicados

### Creación de un ID unico para el control de datos duplicados

  ```python
  import hashlib

  def generate_id(row):
      # Crear una cadena que represente los datos de la fila
      data_string = f"{row['symbol']}-{row['date']}-{row['opening_price']}-{row['closing_price']}-{row['category']}-{row['description']}"
      
      # Generar un hash MD5 de la cadena
      return hashlib.md5(data_string.encode()).hexdigest()
  ```

#### Creación de una cadena representativa de los datos

- La función toma un registro (`row`) del DataFrame como entrada.
- Se crea una cadena (`data_string`) que concatena los valores de varias columnas del registro, separadas por guiones (`-`). Estas columnas incluyen:
  - `'symbol'`: El símbolo de la acción.
  - `'date'`: La fecha del registro.
  - `'opening_price'`: El precio de apertura.
  - `'closing_price'`: El precio de cierre.
  - `'category'`: La categoría del registro.
  - `'description'`: Una descripción del registro.

#### Generación del hash MD5

- La cadena `data_string` se codifica a bytes utilizando `data_string.encode()`.
- Se utiliza `hashlib.md5()` para generar el hash MD5 de la cadena codificada.
- La función `hexdigest()` convierte el hash en una cadena hexadecimal.

#### Retorno del hash MD5

- La función devuelve el hash MD5 generado como una cadena hexadecimal, que sirve como un identificador único para el registro basado en los datos proporcionados.

#### Propósito

La generación de un hash MD5 asegura que cada registro tenga un identificador único derivado de su contenido. Este identificador es útil para evitar duplicados y mantener la integridad de los datos durante procesos como la carga en una base de datos.

Ejemplo de Filtrado de Datos No Duplicados:

```python
# Obtener IDs existentes en la tabla
cursor.execute(f"SELECT id FROM {REDSHIFT_SCHEMA}.stock_data;")
existing_ids = {row[0] for row in cursor.fetchall()}

# Filtrar datos no duplicados basados en el ID
new_rows = block_df[~block_df['id'].isin(existing_ids)]
## Instalación y Configuración
```

## Configuración local del proyecto

1. **Clona el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. **Crea un entorno virtual y actívalo**

   - **Crea un entorno virtual:**

     ```bash
     python -m venv venv
     ```

   - **Activa el entorno virtual:**

     - En Windows:

       ```bash
       venv\Scripts\activate
       ```

     - En macOS y Linux:

       ```bash
       source venv/bin/activate
       ```

3. **Instala las dependencias**

    ```bash
    pip install -r dependencies/requirements.txt
    ```

4. **Configura el archivo `.env`**

    Asegúrate de que el archivo `.env` esté correctamente renombrado (elimina el guion bajo `_` del nombre del archivo), llena estas variables con la información requerida, como las credenciales de conexión a Redshift y otras configuraciones pertinentes, dentro del archivo `.env`.

5. **Ejecuta el proyectos**

    ```bash
    docker-compose up
    ```

## Configuración en GitHub Codespaces del proyecto

1. **Abre el repositorio en GitHub Codespaces

    Haz clic en el botón Code y selecciona Open with Codespaces.
    Crea un nuevo Codespace.
   
2. **Configura el archivo `.env`**

    Asegúrate de que el archivo `.env` esté correctamente renombrado (elimina el guion bajo `_` del nombre del archivo), llena estas variables con la información requerida, como las credenciales de conexión a Redshift y otras configuraciones pertinentes, dentro del archivo `.env`.

3. **Ejecuta el proyecto**

    Ejecuta el siguiente comando en la terminal integrada de Codespaces:

    ```bash
    docker-comnpose up
    ```