from fastapi import APIRouter, Depends, Path, Query, Response
from fastapi.responses import JSONResponse

from dtos.inserir_produto_dto import InserirProdutoDTO
from dtos.id_produto_dto import IdProdutoDTO
from dtos.alterar_produto_dto import AlterarProdutoDTO
from dtos.problem_details_dto import ProblemDetailsDTO
from repositories.produto_repo import ProdutoRepo
from models.produto_model import Produto

router = APIRouter(prefix="/manager")

@router.get("/obter_produtos")
async def obter_produtos() -> list[Produto]:
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.get("/obter_produto_por_id/{id_produto}")
async def obter_produto_por_id(id_produto: int = Path(..., title="Id do Produto", ge=1)) -> Produto:
    produto = ProdutoRepo.obter_um(id_produto)
    if produto:
        return produto
    
    pb = ProblemDetailsDTO(input="int", msg=f"O produto com id {id_produto} não foi encontrado", type="value_not_found", loc=["path", "id"])
    
    return JSONResponse(pb.to_dict(), status_code=404)

@router.post("/inserir_produto", status_code=201)
async def inserir_produto(inputDto: InserirProdutoDTO) -> Produto:
    novo_produto = Produto(None, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    novo_produto = ProdutoRepo.inserir(novo_produto)

    return novo_produto

@router.post("/excluir_produto", status_code=204)
async def excluir_produto(inputDto: IdProdutoDTO):
    if ProdutoRepo.excluir(inputDto.id):
        return None
    pb = ProblemDetailsDTO(input="int", msg=f"O produto com id {inputDto.id} não foi encontrado", type="value_not_found", loc=["body", "id"])
    
    return JSONResponse(pb.to_dict(), status_code=404)        

@router.post("/alterar_produto", status_code=204)
async def alterar_produto(inputDto: AlterarProdutoDTO):
    produto = Produto(inputDto.id, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    if ProdutoRepo.alterar(produto):
        return None
    
    pb = ProblemDetailsDTO(input="int", msg=f"O produto com id {inputDto.id} não foi encontrado", type="value_not_found", loc=["body", "id"])

    return JSONResponse(pb.to_dict(), status_code=404)