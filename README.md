# Proyecto Administración de tecnologías de la información

## ¿Como ejecutar este proyecto?

```bash
# clona el proyecto
git clone https://github.com/alanfvn/admin-tecnologias

# dirigete al directorio de "website"
cd admin-tecnologias/website

# crea un nuevo entorno de python
py -m venv env

# activa el entorno
./env/Scripts/activate

# instala las dependencias
pip install -r req.txt

# ejecuta el servidor
py ./src/manage.py runserver
```

## Mediante Docker

```bash
# construir la build
cd admin-tecnologias/website/
docker build -t admin_tec .

# ejecutar la build
docker run -d -p 80:8000 admin_tec
```
