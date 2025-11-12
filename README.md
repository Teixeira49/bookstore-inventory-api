# 📚 bookstore-inventory-api

API REST para un sistema de gestión de inventario de
librerías que incluyo validación de precios en tiempo real para precios locales
El sistema pertenece a una cadena de librerias financiada por Nextep Innovation, quien a su vez es su principal aliado tecnologico
Aqui se puede:
1. Gestionar Inventario de libros
2. Validar precios con la region local
3. Calcular precios de venta sugeridos

- Enunciado del ejercicio: [Nextep - Prueba Técnica - FullStack Developer.pdf](https://github.com/user-attachments/files/23508456/Nextep.-.Prueba.Tecnica.-.FullStack.Developer.pdf)

---

## 🧪 Instalación

- ✅ Descarga el repositorio (Comando de ayuda: git clone https://github.com/Teixeira49/bookstore-inventory-api).
- ✅ Instala Python en tu equipo (Tutorial: https://www.youtube.com/watch?v=QvQgKagWKYk).
- ✅ Abre el Terminal.
- ✅ Instala Uvicorn con el comando pip install uvicorn (Mas informacion en: https://pypi.org/project/uvicorn/).
- ✅ LISTO.

## 🚀 Ejecución

- ✅ En tu terminal Ejecuta el comando: uvicorn api.main:app --reload
- ⚠️ Si no funciona utiliza python -m uvicorn api.main:app --reload

El codigo abre por defecto el servicio en la siguiente ruta: 
```
http://127.0.0.1:8000/
```
Tambien puedes probar los endpoints en el siguiente enlace: 
```
https://bookstore-inventory-api-nine.vercel.app/
```
## ⚙️ Dependencias Requeridas

- pydanctic
- os
- fastapi
- requests
- uvicorn
- sqlalchemy
- typing
- datetime
- re
- traceback
- dotenv
  
---

## 💾 Features del programa

- Ver todos los libros
- Buscar un libro por ID
- Buscar libro por categoria
- Buscar libros de stock escaso
- Crear un nuevo libro en el sistema
- Editar información de un libro del sistema
- Eliminar un libro del sistema
- Asignar precio local a un libro del sistema

## 📄 Acceso a la documentación & Ejemplos de uso

- En la ruta escribir /docs para acceder a la documentacion, ejemplo:
```
http://127.0.0.1:8000/docs
```
- Tambien puedes exportar la siguiente coleccion de postman:
```
https://drive.google.com/file/d/1uA1dMTYQrgzKxmyfuJEHsaUcmtb2GStc/view?usp=drive_link
```
