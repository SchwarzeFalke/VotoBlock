# Requerimientos
## libmysqlclient
Librería de Python para realizar conexiones con MySQL. Para Ubuntu, instalar con:
```
sudo apt-get install libmysqlclient-dev
```
## Entorno virtual
Para desarrollar el proyecto en un entorno virtual. El propósito principal de los entornos virtuales de Python es crear un entorno aislado para los proyectos de Python. Esto significa que cada proyecto puede tener sus propias dependencias, independientemente de qué dependencias tenga cada otro proyecto ([más información](https://realpython.com/python-virtual-environments-a-primer/))

Para configurar un entorno virtual y activarlo:
```
virtualenv -p /usr/bin/python3 env
source env/bin/activate
```
## Dependencias
```
(env) pip install mysqlclient
(env) pip install python-dotenv
```
