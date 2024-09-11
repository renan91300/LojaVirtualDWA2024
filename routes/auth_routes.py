from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from dtos.entrar_dto import EntrarDTO
from dtos.problem_details_dto import ProblemDetailsDTO
from repositories.usuario_repo import UsuarioRepo
from util.auth_jwt import conferir_senha, criar_token

router = APIRouter(prefix="/auth")

@router.post("/entrar")
async def entrar(entrarDto: EntrarDTO):
    cliente_entrou = UsuarioRepo.obter_por_email(entrarDto.email)
    if (
        (not cliente_entrou)
        or (not cliente_entrou.senha)
        or (not conferir_senha(entrarDto.senha, cliente_entrou.senha))
    ):
        pd = ProblemDetailsDTO(input="str", msg=f"Credenciais inválidas. Certifique-se de que está cadastrado e de que sua senha está correta.", type="value_not_found", loc=["body", "email", "senha"])
        return JSONResponse(pd.to_dict(), status_code=status.HTTP_404_NOT_FOUND)
    
    token = criar_token(cliente_entrou.id, cliente_entrou.nome, cliente_entrou.email, cliente_entrou.perfil)
    return JSONResponse({"token": token}, status_code=status.HTTP_200_OK)
