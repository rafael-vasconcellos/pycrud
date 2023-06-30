from crud_json import *


def clientTest():
    client.insert(nome= 'rafael', cpf= 12345678910)
    client.insert(nome= 'bea', cpf= 12345678900)
    client.insert(nome= 'juliana', cpf= 12345678000)
    print( client.get(nome= 'a') )  # retorna nomes que contenham 'a'
    client.update(old_cpf= 12345678900, newdata= {
        'nome': 'ana'
    })

    client.delete(cpf= 12345678000)


    print(client._data)


def motosTest():
    motocicletas.insert(fabricante= 'Honda', modelo= 'DADA', placa= 'DAD1234', preço= 1.00)
    motocicletas.insert(fabricante= 'Yamaha', modelo= 'DADA2', placa= 'MOM1234', preço= 1.00)
    motocicletas.insert(fabricante= 'Suzuki', modelo= 'DADA3', placa= 'MOM4321', preço= 1.00)
    print(
        # retorna os resultados, deve retornar um array vazio
        motocicletas.get(fabricante= 'Honda', modelo= 'DADA', placa= 'DAD1234', preço= 5, venda= True)
        # venda= True: retorna todos que possuem um campo 'venda' não nulo
        # venda= False: retorna todos que possuem um campo 'venda' nulo
        # venda= Inteiro: retorna todos vendidos ao id (cliente) informado
    )

    print('*'*100, '\n\n\n')
    motocicletas.update(placa= 'DAD1234', newdata= {
        'preço': 2.00
    } )
    motocicletas.update(placa= 'DAD1234', newdata= {
        'venda': 1  # cliente de id 1
    } )
    print(
        # retorna os resultados, deve retornar 1 resultado agora
        motocicletas.get(fabricante= 'Honda', modelo= 'DADA', placa= 'DAD1234', preço= 5, venda= True)
    )
    motocicletas.delete(placa= 'DAD1234')
    motocicletas.update(placa= 'MOM1234', newdata= {
        'venda': 1
    } )

    # tendando atribuir o campo venda a um cliente que não existe
    motocicletas.update(placa= 'MOM4321', newdata= {
        'venda': 5
    } )


    print(motocicletas._data, '\n')


def paymentsTest():
    
    pagamentos.emit(cliente= 1, produto= 2, valor= 1.00, tipo_pagamento= 'à vista', parcela= 1, total_parcelas= 1)
    pagamentos.emit(cliente= 5, produto= 3, valor= 1.00, tipo_pagamento= 'à vista', parcela= 1, total_parcelas= 1) 
    # tentando emitir um pagamento com dados incongruentes com a tabela "motocicletas"
    # o cliente 5 não existe e muito menos comprou o produto 3
    print( pagamentos.get(clientId= 1), '\n' ) # id do cliente
    pagamentos.update(id= 1, sit= 'pago') # id do pagamento


    print(pagamentos._data)


clientTest()
os.system('cls')
motosTest()
#os.system('cls')
#paymentsTest()

