import traceback
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Inicializamos la app en el nivel superior para que Uvicorn pueda encontrarla siempre
app = FastAPI(title="bookstore-inventory-api")

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

    @app.get("/")
    def root():
        return {
            "title": "bookstore-inventory-api",
            "version": "1.0.0",
            "message": "Un pequeño consejo, escribe /docs en la ruta para ver todas mis funciones"
        }

except Exception as e:
    # Si algo falla en las importaciones, reconfiguramos la app para mostrar el error
    tb = traceback.format_exc()
    app.title = "bookstore-inventory-api - Import Error"

    @app.get("/")
    async def root():
        return {"error": "import_failed", "message": str(e)}

    @app.get("/__import_error")
    async def import_error():
        return {"traceback": tb}