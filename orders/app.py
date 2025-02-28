from pathlib import Path
from orders.api.api import router
import yaml
from fastapi import FastAPI

app = FastAPI(
    debug=True,
    openapi_url="/openapi/orders.json",
    docs_url="/docs/orders"
)
oas_doc = yaml.safe_load(
    (Path(__file__).parent/'../oas.yaml').read_text()
)
app.openapi = lambda: oas_doc
app.include_router(router)
