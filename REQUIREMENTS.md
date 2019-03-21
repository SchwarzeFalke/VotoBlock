# Requerimientos

## Entorno virtual

Para desarrollar el proyecto en un entorno virtual. El propósito principal de los entornos virtuales de Python es crear un entorno aislado para los proyectos de Python. Esto significa que cada proyecto puede tener sus propias dependencias, independientemente de qué dependencias tenga cada otro proyecto ([más información](https://realpython.com/python-virtual-environments-a-primer/))

Para configurar un entorno virtual y activarlo:

### Linux

```
virtualenv -p /usr/bin/python3 env
source env/bin/activate
```

### Windows

```
pip install --user virtualenv
.\env\Scripts\activate

```

## Dependencias

```
(env) pip install mysql-connector-python
(env) pip install Flask
(env) pip install python-dotenv
(env) pip install pycrypto
```
