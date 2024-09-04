from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dtos.inserir_produto_dto import InserirProdutoDTO
from dtos.excluir_produto_dto import ExcluirProdutoDTO
from dtos.problem_details_dto import ProblemDetailsDTO
from repositories.produto_repo import ProdutoRepo
from models.produto_model import Produto

router = APIRouter(prefix="/manager")

@router.get("/obter_produtos")
async def obter_produtos() -> list[Produto]:
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.post("/inserir_produto")
async def inserir_produto(inputDto: InserirProdutoDTO) -> Produto:
    novo_produto = Produto(None, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    novo_produto = ProdutoRepo.inserir(novo_produto)

    return novo_produto

@router.post("/excluir_produto")
async def excluir_produto(inputDto: ExcluirProdutoDTO):
    if ProdutoRepo.excluir(inputDto.id):
        return
    
    pb = ProblemDetailsDTO(input="int", msg=f"O produto com id {inputDto.id} não foi encontrado", type="value_not_found", loc=["body", "id"])
    
    return JSONResponse(pb.to_dict(), status_code=404)