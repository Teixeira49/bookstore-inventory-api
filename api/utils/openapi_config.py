
OPENAPI_DESCRIPTION = """
Bienvenido a la API de gestión de inventario. Aquí podrás administrar el catálogo de libros, 
controlar el stock y realizar cálculos de precios con divisas internacionales.

### 🛠️ Tecnologías utilizadas:
* **FastAPI** para el core de la API.
* **SQLAlchemy** para la persistencia.
* **Vercel** para el despliegue.

---
_Escribe `/docs` para probar los endpoints interactivamente._\n
_Escribe `/redoc` para acceder a la documentación._\n
_Escribe `/` para ver todas las opciones._\n
_FRONTEND: `https://neon-catalog-bookstore.lovable.app/`._"""

WEBSITE_URL = "https://neon-catalog-bookstore.lovable.app/"


TAGS_METADATA = [
    {
        "name": "Vistas de Libros",
        "description": "📦 **Consultas masivas**. Endpoints diseñados para obtener listados completos del catálogo.",
    },
    {
        "name": "CRUD de Libros",
        "description": "🔧 **Operaciones base**. Permite el ciclo de vida completo de un libro en el sistema.",
    },
    {
        "name": "Búsqueda e Inventario",
        "description": "🔍 **Filtros avanzados**. Localiza libros por categoría o identifica aquellos con bajo stock.",
    },
    {
        "name": "Integraciones Externas",
        "description": "🌍 **Servicios externos**. Conexión con APIs de terceros para cálculos financieros.",
    },
]
