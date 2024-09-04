from fastapi import APIRouter

from dtos.inserir_produto_dto import InserirProdutoDTO
from repositories.produto_repo import ProdutoRepo
from models.produto_model import Produto

router = APIRouter(prefix="/manager")

@router.get("/obter_produtos")
async def obter_produtos() -> list[Produto]:
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.post("/inserir_produto")
async def inserir_produto(produto: InserirProdutoDTO) -> Produto:
    novo_produto = Produto(None, produto.nome, produto.preco, produto.descricao, produto.estoque)
    novo_produto = ProdutoRepo.inserir(novo_produto)

    return novo_produto

@router.post("/excluir_produto")
async def excluir_produto(id_produto: int):
    if ProdutoRepo.excluir(id_produto):
        return {"mensagem": "Produto excluído com sucesso!"}
    
    return {"mensagem": "Produto não encontrado!"}  
    