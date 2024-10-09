from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Limitador Global de Peticiones
limiter = Limiter(
    get_remote_address, 
    default_limits=["20000 per day", "5000 per hour"]
)