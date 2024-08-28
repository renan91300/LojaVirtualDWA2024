from fastapi import APIRouter


router = APIRouter(prefix="/manager")

@router.get("/")
async def admin_home():
    return {"message": "Bem-vindo à área administrativa!"}