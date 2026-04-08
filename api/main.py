from fastapi import FastAPI
import traceback
from dotenv import load_dotenv

load_dotenv()

try:
    from api.controller.v1.books_controller import router as controller_app

    import os
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="bookstore-inventory-api")

    # Obtener orígenes permitidos desde variables de entorno
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
    tb = traceback.format_exc()
    app = FastAPI(title="bookstore-inventory-api - Import Error")
    exception = e

    @app.get("/")
    async def root():
        return {"error": "import_failed", "message": str(exception)}

    @app.get("/__import_error")
    async def import_error():
        # endpoint temporal para ver la traza completa en los logs/response
        return {"traceback": tb}