# CTF Project

## Autores
- Franco Niderhaus
- Joaquin Chanquia
- Bruno Zanetti

## Dockerfile y docker-compose.yml
El proyecto incluye un `Dockerfile` para construir la imagen de la aplicación Flask y un `docker-compose.yml` para levantar tanto la aplicación como la base de datos MySQL fácilmente. Tambien se incluye un archivo `run.sh`, el cual ejecuta los comandos necesarios para levantar la aplicacion.

- Para construir y levantar el entorno completo:
  ```bash
  sudo docker compose up --build
  ```
- El servicio web estará disponible en: http://localhost:50000

## Cómo setear una flag
La flag está almacenada en la base de datos MySQL, en la tabla `subjects`, columna `secret`, en la entrada de la materia de nombre `Estadistica`, encriptada usando la clave publica PGP que se encuentra en la ruta `www/static/files/public_key.asc`.

Para cambiar una flag:
1. Copia la clave PGP pública en `www/static/files/public_key.asc`.
2. Ve a `https://cyberchef.org/` (para mantener el formato de todas las entradas de la base de datos)
3. Busca la opcion `PGP Encrypt` y arrastrala a la receta.
4. Pega la clave pública en la casilla `Public key of recipient`.
5. Escribe la flag deseada en el input.
6. Copia el resultado de la encriptacion en el output.
7. Edita el archivo `database/ctf.sql` y reemplaza el valor de la columna `secret` en la materia `Estadistica` por la flag encriptada.


## Forma de explotarlo

Para encontrar la flag en el sistema se deben vulnerar todas las secciones de la aplicacion. La aplicacion esta pensada para que las paginas se vean y vulneren en orden, tener en cuenta que el resultado obtenido para cada vulneración se deberá usar en la pagina siguiente para obtener la siguiente parte de la información.

### XSS

1. Ve a la sección `XSS` en la aplicación.
2. En el buscador, ingresa un payload como:
   ```
   <script>alert(document.cookie)</script>
   ```
3. El script se ejecutará, demostrando la vulnerabilidad. Y en la cookie `secret` de la pagina se encontrará la contraseña del administrador que se usará mas adelante.
4. La contraseña se encuentra codificada en JSFuck, por lo que deberá ser decodificada.

### Encriptacion

1. Ve a la sección `Encriptacion`.
2. Deshashea el ejemplo de hash inseguro para obtener en que materia se encuentra la flag en la siguiente pagina.
3. Inicie sesión como administrador con el usuario `admin` y la contraseña obtenida en la cookie de la pagina anterior.
4. Descargue la clave privada para usar en la siguiente pagina.

### SQLI

1. Ve a la sección `SQLI`.
2. Buscar algo en la base de datos, por ejemplo `1`.
3. Copiar el link de la pagina con la busqueda y utilizarlo para realizar consultas con sqlmap hasta lograr hacer un dump de la tabla `subjects`. La consulta final utilizada es:
   ```
   sqlmap -u "http://localhost:50000/sqli/database?search=1" -D ctf -T subjects --dump
   ```
4. Copiar el mensaje encriptado que se encuentra en la columna secret de la entrada de `Estadistica`.
5. Desencriptar el mensaje con la clave privada obtenida en la pagina anterior. (Se puede usar `https://cyberchef.org/` con la opcion `PGP Decrypt`). El resultado obtenido será la flag. (A veces puede pasar que al copiar el texto directamente desde el dump de sqlmap los enter se vean como `\\n`, si pasa esto reemplazar cada `\\n` por un enter)
