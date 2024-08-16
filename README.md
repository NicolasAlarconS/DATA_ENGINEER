# Data_Engineer 2da entrega

Este proyecto de ingeniería de datos se encarga de extraer, transformar, filtrar duplicados y cargar datos financieros a una base de datos en Redshift desde una API. A continuación, se detalla cómo configurar y ejecutar el proyecto tanto localmente como en GitHub Codespaces.

## Estructura del Proyecto

- **config**: Contiene el archivo `.env` para las variables de entorno.
- **dependencies**: Contiene el archivo `requirements.txt` para las dependencias del proyecto.
- **modules**: Contiene los archivos Python (`api.py`, `config.py`, `database.py`, `etl.py`, `transform.py`) que gestionan la lógica del proyecto.
- **main.py**: Archivo principal que ejecuta el flujo de trabajo del proyecto.
- **.gitignore**: Archivo para excluir archivos y directorios del control de versiones.
- **README.md**: Este archivo de documentación.

### CreCreación de un ID unico para el control de datos duplicados

  ```python
  import hashlib

  def generate_id(row):
      # Crear una cadena que represente los datos de la fila
      data_string = f"{row['symbol']}-{row['date']}-{row['opening_price']}-{row['closing_price']}-{row['category']}-{row['description']}"
      
      # Generar un hash MD5 de la cadena
      return hashlib.md5(data_string.encode()).hexdigest()
  ```

#### Creación de una Cadena Representativa de los Datos

- La función toma un registro (`row`) del DataFrame como entrada.
- Se crea una cadena (`data_string`) que concatena los valores de varias columnas del registro, separadas por guiones (`-`). Estas columnas incluyen:
  - `'symbol'`: El símbolo de la acción.
  - `'date'`: La fecha del registro.
  - `'opening_price'`: El precio de apertura.
  - `'closing_price'`: El precio de cierre.
  - `'category'`: La categoría del registro.
  - `'description'`: Una descripción del registro.

#### Generación del Hash MD5

- La cadena `data_string` se codifica a bytes utilizando `data_string.encode()`.
- Se utiliza `hashlib.md5()` para generar el hash MD5 de la cadena codificada.
- La función `hexdigest()` convierte el hash en una cadena hexadecimal.

#### Retorno del Hash MD5

- La función devuelve el hash MD5 generado como una cadena hexadecimal, que sirve como un identificador único para el registro basado en los datos proporcionados.

#### Propósito

La generación de un hash MD5 asegura que cada registro tenga un identificador único derivado de su contenido. Este identificador es útil para evitar duplicados y mantener la integridad de los datos durante procesos como la carga en una base de datos.

### Proceso de Control de Duplicados

1. **Conexión a Redshift**
   - El script establece una conexión a la base de datos Redshift utilizando las credenciales proporcionadas en el archivo de configuración.

2. **Creación de la Tabla**
   - Antes de insertar datos, el script verifica si la tabla `stock_data` existe en el esquema especificado. Si no existe, se crea con una definición que incluye una columna `id` como clave primaria. La clave primaria no asegura que los identificadores en esta columna sean únicos en la tabla ya que Redshift permite claves primarias repetidas, por lo que el control de suplicados se hace antes del ingreso de los datos.

3. **División de Datos en Bloques**
   - Los datos del DataFrame (`df`) se dividen en bloques de tamaño especificado (`block_size`). Esto se hace para manejar grandes volúmenes de datos de manera más eficiente y para realizar la inserción en lotes.

4. **Obtención de IDs Existentes**
   - Para cada bloque de datos, se ejecuta una consulta SQL para obtener todos los `id` existentes en la tabla `stock_data`. Estos IDs se almacenan en un conjunto (`existing_ids`), que facilita la búsqueda rápida.

5. **Filtrado de Datos No Duplicados**
   - Con el conjunto de IDs existentes, el script filtra el bloque de datos actual para excluir aquellas filas cuyos IDs ya están en la tabla. Esto se hace utilizando la función `isin` de pandas combinada con una negación (`~`) para seleccionar solo las filas con IDs que no están en `existing_ids`.

6. **Inserción de Nuevos Registros**
   - Después de filtrar los datos, se preparan las filas que deben ser insertadas en la base de datos. Si no hay registros nuevos para insertar, se omite la inserción para ese bloque de datos.
   - Si hay registros nuevos, se realiza la inserción en bloque utilizando la función `execute_values` de `psycopg2`, que permite insertar múltiples filas de manera eficiente.

7. **Confirmación y Cierre de Conexión**
   - Después de cada inserción en bloque, se confirma la transacción con `conn.commit()`.
   - Finalmente, se cierra la conexión a la base de datos.

Ejemplo de Filtrado de Datos No Duplicados:

```python
# Obtener IDs existentes en la tabla
cursor.execute(f"SELECT id FROM {REDSHIFT_SCHEMA}.stock_data;")
existing_ids = {row[0] for row in cursor.fetchall()}

# Filtrar datos no duplicados basados en el ID
new_rows = block_df[~block_df['id'].isin(existing_ids)]
## Instalación y Configuración
```

## Configuración Local del proyecto

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

4. **Configura el archivo .env**

    Asegúrate de que el archivo .env en la carpeta config contiene las variables de entorno necesarias, como la URL de conexión a Redshift y otras configuraciones.

5. **Ejecuta el proyectos**

    ```bash
    python main.py
    ```

## Configuración en GitHub Codespaces del proyecto

1. **Abre el repositorio en GitHub Codespaces

    Navega a tu repositorio en GitHub.
    Haz clic en el botón Code y selecciona Open with Codespaces.
    Crea un nuevo Codespace.

2. **Configura el entorno virtual**

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

3. **Instalación de dependencias en Codespaces**

    Instala las dependencias del proyecto ejecutando:

    ```bash
    pip install -r dependencies/requirements.txt
    ```

4. **Configura el archivo .env**

    Asegúrate de que el archivo .env está correctamente configurado con las variables de entorno necesarias.

5. **Ejecuta el proyecto**

    Ejecuta el siguiente comando en la terminal integrada de Codespaces:

    ```bash
    python main.py
    ```