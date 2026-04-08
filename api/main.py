import traceback
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import FileResponse, HTMLResponse
from dotenv import load_dotenv

from api.utils.openapi_config import OPENAPI_DESCRIPTION, TAGS_METADATA, WEBSITE_URL
from api.utils.html_templates import get_success_html, get_error_html

load_dotenv()

# Inicializamos la app bloqueando las rutas de docs por defecto para personalizarlas
app = FastAPI(
    title="📖 Bookstore Inventory API",
    description=OPENAPI_DESCRIPTION,
    version="1.0.2",
    openapi_tags=TAGS_METADATA,
    docs_url=None, 
    redoc_url=None
)

# Montamos la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.png")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_favicon_url="/static/favicon.png",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_favicon_url="/static/favicon.png",
    )

try:
    from api.controller.v1.books_controller import router as controller_app

    # Configuración de CORS
    cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8000")
    origins = [origin.strip() for origin in cors_origins_env.split(",")]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(controller_app)

    @app.get("/", response_class=HTMLResponse)
    def root():
        return get_success_html("Bookstore Inventory API", "1.0.2", WEBSITE_URL)

except Exception as e:
    # Si algo falla en las importaciones, reconfiguramos la app para mostrar el error
    tb = traceback.format_exc()
    app.title = "bookstore-inventory-api - Import Error"

    @app.get("/", response_class=HTMLResponse)
    async def root():
        return get_error_html("Error de Inicialización", "No se pudo cargar el controlador o los servicios principales.")

    @app.get("/__import_error", response_class=HTMLResponse)
    async def import_error():
        return get_error_html("Python Import Error", tb)