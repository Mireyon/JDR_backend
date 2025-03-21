import warnings

# suppress UserWarning from pydantic
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from .main import app