clientes = {
    'id': '',
    'nome': '',
    'cpf': '',
}

motocicletas = {
    'id': '',
    'fabricante': '',
    'modelo': '',
    'placa': '',
    'preço': '',
    'venda': ''
}

pagamentos = {
    'id': '',
    'cliente': '',
    'produto': '',
    'valor': '',
    'tipo de pagamento': '',
    'parcela': '',
    'total de parcelas': '',
    'emissão': '',
    'vencimento': '',
    'situação': ''
}



"""

CREATE TABLE clientes (
	id integer Not Null,
	nome varchar(50) Not Null,
	cpf integer(11) Not Null,
  	Primary Key(id)
);


CREATE TABLE motocicletas (
	id integer Not Null PRIMARY KEY,
  	fabricante varchar(10) Not Null,
  	modelo varchar(11) Not Null,
    placa varchar(7) Not Null,
	preço DECIMAL(10,2) Not Null,
  	venda int,

  	foreign key (venda) references clientes(id) On Delete CASCADE
    CHECK ( placa = UPPER(placa) )
    CHECK ( modelo = UPPER(modelo) )
);


CREATE TABLE pagamentos (
    id integer Not Null PRIMARY KEY,
    cliente_id INT Not Null,
    produto_id INT Not Null,
    valor DECIMAL(10,2) Not Null,
    tipo_pagamento VARCHAR(50) Not Null,
    parcela INT Not Null,
    total_parcelas INT Not Null,
    emissao DATE Not Null,
    vencimento DATE Not Null,
    situaçao varchar(8),

    CHECK(situaçao = 'pago' or situaçao = 'pendente'),
    CHECK(parcela <= total_parcelas),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES motocicletas(id)
);



"""