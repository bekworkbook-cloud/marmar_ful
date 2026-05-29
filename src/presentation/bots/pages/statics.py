from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path
router = APIRouter(prefix="/statics", tags=["Statics"])

stat_path = {
    "customer": "src/static/pages/customer/",
    "operator": "src/static/pages/operator/",
    "courier": "src/static/pages/courier/",
    "admin": "src/static/pages/admin/"
}

react_pathes = {
    "admin_bot": "static/admin/",
    "operator_bot": "static/operator/",
    "courier_bot": "static/courier/",
    "customer_bot": "static/customer/"
}



@router.get("/{role}/{path:path}")
async def get_customer_page(path: str, role: str):
    return FileResponse(path=Path(react_pathes.get(role)+path))