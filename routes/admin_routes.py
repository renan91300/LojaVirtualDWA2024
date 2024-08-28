from fastapi import APIRouter

from dtos.novo_produto_dto import NovoProdutoDTO
from repositories.produto_repo import ProdutoRepo
from models.produto_model import Produto

router = APIRouter(prefix="/manager")

@router.get("/obter_produtos")
async def obter_produtos() -> list[Produto]:
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.get("/inserir_produto")
async def inserir_produto(produto: NovoProdutoDTO):
    pass