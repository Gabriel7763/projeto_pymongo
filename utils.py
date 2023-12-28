import bson.errors
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as berrors

def conectar():
    """
    Função para conectar ao servidor
    """
    connection = MongoClient('localhost', 27017)
    return connection

def desconectar(connection):
    """
    Função para desconectar do servidor.
    """
    if connection:
        connection.close()


def listar():
    """
    Função para listar os produtos
    """
    connection = conectar()
    db = connection.pmongo

    try:
        if db.produtos.count_documents({}) > 0:
            produtos = db.produtos.find()
            print('Listando produtos...')
            print('--------------------')
            for produto in produtos:
                print(f"ID: {produto['_id']}")
                print(f"Produto: {produto['nome']}")
                print(f"Preço: {produto['preco']}")
                print(f"Estoque: {produto['estoque']}")
                print('-----------------------------')
        else:
            print('Não existem produtos cadastrados')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
        desconectar(connection)


def inserir():
    """
    Função para inserir um produto
    """  
    connection = conectar()
    db = connection.pmongo

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preco do produto: '))
    estoque = int(input('Informe o estoque do produto: '))

    try:
        db.produtos.insert_one(
            {
                "nome": nome,
                "preco": preco,
                "estoque": estoque
            }
        )
        print(f'O produto {nome} foi sinserido com sucesso')
    except errors.PyMongoError as e:
        print(f'Não foi possível inserir o produto. {e}')
    desconectar(connection)

def atualizar():
    """
    Função para atualizar um produto
    """
    connection = conectar()
    db = connection.pmongo

    _id = input('Informe o ID do produto: ')
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque de produtos: '))

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }
                }
            )
            if res.modified_count == 1:
                print(f'O produto {nome} foi atualizado com sucesso!')
            else:
                print('Não foi possível atualizar o produto.')
        else:
            print('Não existem documento para serem atualizados')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    except bson.errors.InvalidId as f:
        print(f'OjbectID inválido: {f}')
    desconectar(connection)

def deletar():
    """
    Função para deletar um produto
    """  
    connection = conectar()
    db = connection.pmongo

    _id = input('Informe o ID do produto: ')
    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            if res.deleted_count > 0:
                print('Produto deletado!')
            else:
                print('Não foi possível deletar o produto')
        else:
            print('Não existem produtos para serem deletados')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    except bson.errors.InvalidId as f:
        print(f'OjbectID inválido: {f}')
    desconectar(connection)

def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
