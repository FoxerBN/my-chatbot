from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask-Limiter
# It will track requests by IP address and limit to 15 requests per hour
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["15 per hour"],
    storage_uri="memory://",  # Use in-memory storage for simplicity
)
