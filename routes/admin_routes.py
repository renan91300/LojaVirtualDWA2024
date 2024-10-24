import asyncio
from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse

from dtos.alterar_pedido_dto import AlterarPedidoDTO
from dtos.entrar_dto import EntrarDTO
from dtos.inserir_produto_dto import InserirProdutoDTO
from dtos.id_produto_dto import IdProdutoDTO
from dtos.alterar_produto_dto import AlterarProdutoDTO
from dtos.problem_details_dto import ProblemDetailsDTO
from models.pedido_model import EstadoPedido, Pedido
from repositories.item_pedido_repo import ItemPedidoRepo
from repositories.pedido_repo import PedidoRepo
from repositories.produto_repo import ProdutoRepo
from models.produto_model import Produto
from repositories.usuario_repo import UsuarioRepo
from util.auth_jwt import conferir_senha, criar_token
from util.pydantic import create_validation_errors

router = APIRouter(prefix="/admin")

@router.get("/obter_produtos")
async def obter_produtos() -> list[Produto]:
    # Delay de 2 segundos
    await asyncio.sleep(2)
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.get("/obter_produto_por_id/{id_produto}")
async def obter_produto_por_id(id_produto: int = Path(..., title="Id do Produto", ge=1)) -> Produto:
    produto = ProdutoRepo.obter_um(id_produto)
    if produto:
        return produto
    
    pd = ProblemDetailsDTO(input="int", msg=f"O produto com id {id_produto} não foi encontrado", type="value_not_found", loc=["path", "id"])
    
    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/inserir_produto", status_code=201)
async def inserir_produto(inputDto: InserirProdutoDTO) -> Produto:
    novo_produto = Produto(None, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    novo_produto = ProdutoRepo.inserir(novo_produto)

    return novo_produto

@router.post("/excluir_produto/{id_produto}", status_code=204)
async def excluir_produto(id_produto: int = Path(..., title="Id do Produto", ge=1)):    
    if ProdutoRepo.excluir(id_produto):
        return None
    pd = ProblemDetailsDTO(input="int", msg=f"O produto com id {id_produto} não foi encontrado", type="value_not_found", loc=["body", "id"])
    
    return JSONResponse(pd.to_dict(), status_code=404)        

@router.post("/alterar_produto", status_code=204)
async def alterar_produto(inputDto: AlterarProdutoDTO):
    produto = Produto(inputDto.id, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    if ProdutoRepo.alterar(produto):
        return None
    
    pd = ProblemDetailsDTO(input="int", msg=f"O produto com id {inputDto.id} não foi encontrado", type="value_not_found", loc=["body", "id"])

    return JSONResponse(pd.to_dict(), status_code=404)

@router.get("/obter_pedido_por_id/{id_pedido}")
async def obter_pedido_por_id(id_pedido: int = Path(..., title="Id do Pedido", ge=1)) -> Pedido:
    pedido = PedidoRepo.obter_por_id(id_pedido)
    if pedido:
        return pedido
    
    pd = ProblemDetailsDTO(input="int", msg=f"O pedido com id {id_pedido} não foi encontrado", type="value_not_found", loc=["path", "id"])
    
    return JSONResponse(pd.to_dict(), status_code=404)

@router.get("/obter_pedido/{id_pedido}")
async def obter_pedido_por_id(id_pedido: int = Path(..., title="Id do Pedido", ge=1)) -> Pedido:
    pedido = PedidoRepo.obter_por_id(id_pedido)    
    if pedido:
        itens = ItemPedidoRepo.obter_por_pedido(pedido.id)
        cliente = UsuarioRepo.obter_por_id(pedido.id_cliente)
        pedido.itens = itens
        pedido.cliente = cliente
        return pedido
    
    pd = ProblemDetailsDTO(input="int", msg=f"O pedido com id {id_pedido} não foi encontrado", type="value_not_found", loc=["path", "id"])
    
    return JSONResponse(pd.to_dict(), status_code=404)

@router.get("/obter_pedidos_por_estado/{estado}")
async def obter_pedidos_por_estado(estado: EstadoPedido = Path(..., title="Estado do Pedido")):
    # delay de 2 segundos
    await asyncio.sleep(2)
    pedidos = PedidoRepo.obter_todos_por_estado(estado.value)
    return pedidos

@router.post("/alterar_pedido", status_code=204)
async def alterar_pedido(inputDto: AlterarPedidoDTO):
    if PedidoRepo.alterar_estado(inputDto.id, inputDto.estado.value):
        return None
    
    pd = ProblemDetailsDTO(input="int", msg=f"O pedido com id {inputDto.id} não foi encontrado", type="value_not_found", loc=["body", "id"])

    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/cancelar_pedido/{id_pedido}", status_code=204)
async def cancelar_pedido(id_pedido: int = Path(..., title="Id do Pedido", ge=1)):
    if PedidoRepo.alterar_estado(id_pedido, EstadoPedido.CANCELADO.value):
        return None
    
    pd = ProblemDetailsDTO(input="int", msg=f"O pedido com id {id_pedido} não foi encontrado", type="value_not_found", loc=["body", "id"])

    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/evoluir_pedido/{id_pedido}", status_code=204)
async def evoluir_pedido(id_pedido: int = Path(..., title="Id do Pedido", ge=1)):
    pedido = PedidoRepo.obter_por_id(id_pedido)
    if not pedido:
        pd = ProblemDetailsDTO(input="int", msg=f"O pedido com id {id_pedido} não foi encontrado", type="value_not_found", loc=["body", "id"])

        return JSONResponse(pd.to_dict(), status_code=404)

    estado_atual = pedido.estado
    estados = [estado.value for estado in EstadoPedido]    
    estados.remove(EstadoPedido.CANCELADO.value)
    indice = estados.index(estado_atual)
    indice += 1
    # se o indice for maior que o tamanho da lista, então o pedido está no último estado
    if indice < len(estados):
        # obter o próximo estado
        proximo_estado = estados[indice]
        # alterar o estado do pedido
        if PedidoRepo.alterar_estado(id_pedido, proximo_estado):
            return None

    pd = ProblemDetailsDTO(input="int", msg=f"O pedido com id {id_pedido} não pode ter seu estado evoluido para <b>cancelado</b>", type="status_change_invalid", loc=["body", "id"])

    return JSONResponse(pd.to_dict(), status_code=404)