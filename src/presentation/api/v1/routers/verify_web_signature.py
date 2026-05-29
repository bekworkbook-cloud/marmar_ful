from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse

from presentation.api.v1.dependencies.init_data import verify_webapp_signature_dynamic
from src.core.application.use_cases.verify_web_app_signature import VerifyWebAppSignatureUseCase



router = APIRouter()


# @router.get("/")
# async def get_loader_page(
#         bot: str,
#         parsed_data: dict = Depends(verify_webapp_signature_dynamic),
#         use_case: VerifyWebAppSignatureUseCase = Depends()
#     ):

#     return await use_case.execute(parsed_data)