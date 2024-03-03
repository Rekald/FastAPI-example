from src.main import app
from src.config import get_settings
import uvicorn

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(app, host=settings.HOSTNAME.host, port=settings.HOSTNAME.port, log_level="info")
