# CTF Project Fix

## Autores
- Franco Niderhaus
- Joaquin Chanquia
- Bruno Zanetti

## Dockerfile y docker-compose.yml
El proyecto incluye un `Dockerfile` para construir la imagen de la aplicación Flask y un `docker-compose.yml` para levantar tanto la aplicación como la base de datos MySQL fácilmente.

- Para construir y levantar el entorno completo:
  ```bash
  sudo docker compose up --build
  ```
- El servicio web estará disponible en: http://localhost:50001

## Cómo setear una flag
La flag está almacenada en la base de datos MySQL, en la tabla `subjects`, columna `secret`, en la entrada de la materia de nombre `Estadistica`, encriptada usando la clave publica PGP que se encuentra en la ruta `www/static/files/public_key.asc`.

Para cambiar una flag:
1. Copia la clave PGP pública en `www/static/files/public_key.asc`.
2. Ve a `https://cyberchef.org/` (para mantener el formato de todas las entradas de la base de datos)
3. Busca la opcion `PGP Encrypt` y arrastrala a la receta.
4. Pega la clave pública en la casilla `Public key of recipient`.
5. Escribe la flag deseada en el input.
6. Copia el resultado de la encriptacion en el output.
7. Edita el archivo `database/ctfix.sql` y reemplaza el valor de la columna `secret` en la materia `Estadistica` por la flag encriptada.


## Forma de arreglar las vulnerabilidades



### XSS

# Encriptar la cookie

Para evitar que la cookie sea encontrada facilmente del lado del usuario se encripto la misma con una funcion XOR.
Tambien se agregaron los parametros secure y httponl, para evitar que la misma sea accesible con XSS.

# Evitar que si hay un payload ejecutable se ejecute

Se modifico el html (sacando el |safe del punto vulnerable), para que si se ingresa un script este no sea ejecutado.

### Encriptacion

Como la forma de encontrar la contraseña del admin era mediante la cookie de la pagina anterior, esta pagina ya no es vulnerable porque la información ya no se encuentra disponible a los usuarios.

### SQLI

Para solucionar las inyecciones SQL se elimino la anterior busqueda con inyeccion directa de los parametros recibidos en la aplicacion y se implemento una consulta parametrizada. Ademas de primero verificar que los parametros recibidos sean realmente numeros enteros.
