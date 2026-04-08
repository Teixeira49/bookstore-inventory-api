
def get_base_css():
    return """
    :root {
        --bg-color: #0A0A0C;
        --glow-color: #0D1B2A;
        --neon-green: #00E676;
        --electric-purple: #651FFF;
        --bright-blue: #00B0FF;
        --text-primary: #FFFFFF;
        --text-secondary: rgba(255, 255, 255, 0.85);
        --font-main: 'Plus Jakarta Sans', sans-serif;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: radial-gradient(circle at bottom, var(--glow-color) 0%, var(--bg-color) 70%);
        background-attachment: fixed;
        min-height: 100vh;
        color: var(--text-primary);
        font-family: var(--font-main);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 24px;
        text-align: center;
    }

    .brand-shape {
        width: 60px;
        height: 60px;
        background: var(--bright-blue);
        clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
        margin-bottom: 32px;
        filter: drop-shadow(0 0 15px var(--bright-blue));
        animation: float 4s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    h1 {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 16px;
        text-transform: uppercase;
    }

    .version-tag {
        font-size: 0.9rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 4px 12px;
        border-radius: 9999px;
        margin-bottom: 32px;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    p {
        color: var(--text-secondary);
        max-width: 600px;
        line-height: 1.6;
        margin-bottom: 64px;
        font-size: 1.1rem;
    }

    .button-container {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        justify-content: center;
    }

    .btn {
        text-decoration: none;
        color: white;
        padding: 12px 24px;
        border-radius: 9999px;
        border: 1px solid white;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.85rem;
    }

    .btn:hover {
        background: white;
        color: black;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }

    .btn.neon-green:hover {
        border-color: var(--neon-green);
        background: var(--neon-green);
        box-shadow: 0 0 20px var(--neon-green);
    }

    .btn.electric-purple:hover {
        border-color: var(--electric-purple);
        background: var(--electric-purple);
        box-shadow: 0 0 20px var(--electric-purple);
    }

    .btn.bright-blue:hover {
        border-color: var(--bright-blue);
        background: var(--bright-blue);
        box-shadow: 0 0 20px var(--bright-blue);
    }

    /* Error styles */
    .error-container {
        background: rgba(255, 50, 50, 0.05);
        border: 1px solid rgba(255, 50, 50, 0.3);
        padding: 40px;
        border-radius: 24px;
        max-width: 800px;
        width: 100%;
    }

    .terminal {
        background: #000;
        color: #ff5555;
        padding: 20px;
        border-radius: 12px;
        text-align: left;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin-top: 32px;
        border-left: 4px solid #ff5555;
        white-space: pre-wrap;
    }
    """

def get_success_html(title, version, website_url):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
        <style>{get_base_css()}</style>
    </head>
    <body>
        <div class="brand-shape"></div>
        <h1>{title.replace('o', '✦').replace('O', '✦')}</h1>
        <div class="version-tag">v{version}</div>
        <p>Potente sistema de gestión de inventario para librerías con integración de divisas internacionales y documentación automatizada.</p>
        
        <div class="button-container">
            <a href="/docs" class="btn bright-blue">Swagger Docs</a>
            <a href="/redoc" class="btn electric-purple">ReDoc</a>
            <a href="{website_url}" target="_blank" class="btn neon-green">Visitar Website</a>
        </div>
    </body>
    </html>
    """

def get_error_html(error_msg, traceback_str):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error de Sistema</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
        <style>{get_base_css()}</style>
    </head>
    <body>
        <div class="error-container">
            <h1 style="color: #ff5555;">SYSTEM FAILURE</h1>
            <p>Se ha detectado una anomalía crítica en la inicialización del sistema. Por favor, revisa el log técnico a continuación.</p>
            
            <div class="terminal">
[FATAL ERROR]: {error_msg}

{traceback_str}
            </div>
            
            <div class="button-container" style="margin-top: 40px;">
                <a href="/" class="btn">Reintentar Conexión</a>
            </div>
        </div>
    </body>
    </html>
    """
