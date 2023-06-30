import sqlite3, datetime

conexao = sqlite3.connect('db.sqlite')
cursor = conexao.cursor()

# INSERT e UPDATE precisam de try catch por causa da possibilidade dos dados fornecidos não atenderem as restrições
# DELETE e SELECT não precisam de try catch
class Clients:
    def validate(self, nome=None, cpf=None):
        if not nome and not cpf:
            return False

        #if nome and len(nome.split(' ')) < 3:
                #return False

        if cpf:
            if len(self.get(cpf= cpf)) == 0 and len(str(cpf))==11:
                try:
                    int(cpf)
                except ValueError:
                    return False
            else:
                return False
        
        return True
    

    def _qstring(self, nome= None, cpf= None, id=None):
        qstring = ''

        if not nome and not cpf and not id:
            return False
        
        if id:
            qstring = f'id = {id}'
            return qstring

        if nome:
            qstring += f"nome like '%{nome}%'"
            if cpf:
                qstring += f" and "
        if cpf:
            qstring += f"cpf = {cpf}"

        return qstring


    def insert(self, nome, cpf):
        if self.validate(nome, cpf):
            cursor.execute(f"INSERT INTO clientes(nome, cpf) VALUES('{nome}', {cpf})")
            conexao.commit()

    def get(self, nome=None, cpf=None, id=None):
        qstring = self._qstring(nome, cpf, id)
        if qstring:
            cursor.execute(f"SELECT nome, cpf FROM clientes WHERE {qstring}")
            return cursor.fetchall()
        else:
            return False

    def update(self, old_cpf=None, old_nome=None, newdata=None):
        if isinstance(newdata, dict):
                qstring = ''
                new_nome = None
                new_cpf = None
                key = list(newdata.keys())[0]
                if old_cpf:
                    qstring += f'cpf = {old_cpf}'
                elif old_nome:
                    qstring += f'nome = {old_nome}'
                else:
                    return False

                if 'nome' in newdata.keys():
                    new_nome = newdata['nome']
                elif 'cpf' in newdata.keys():
                    new_cpf = newdata['cpf']
                else:
                    return False

                if not self.validate(new_nome, new_cpf):
                    return False

                cursor.execute(f"UPDATE clientes SET {key} = '{new_nome if new_nome else new_cpf}' WHERE {qstring}")
                conexao.commit()
                return True
        else:
            return False


    def delete(self, cpf):
            cursor.execute(f'DELETE FROM clientes WHERE cpf = {cpf}')
            conexao.commit()



class Motos:
    def validate(self, venda=None, preço=None):
        if not venda and not preço:
            return False

        elif venda and isinstance(venda, int) and len(client.get(id= venda)) > 0:
            return True
        
        elif preço:
            try:
                format(preço, '.2f')
                return True
            except:
                return False
        
        else:
            return False

    def _qstring(self, fabricante=None, modelo=None, placa=None, preço=None, venda=None, id=None):
        qstring = ''
        if not fabricante and not modelo and not placa and not preço and not venda and not id:
            return False

        if id:
            qstring += f'id = {id}'
            return qstring

        if fabricante:
            qstring += f"fabricante like '%{fabricante}%'"
            if modelo or preço or venda:
                qstring += ' and '

        if modelo:
            qstring += f"modelo like '%{modelo}%'"
            if placa or preço or venda:
                qstring += ' and '

        if placa:
            qstring += f"placa like '%{placa}%'"
            if preço or venda:
                qstring += ' and '

        if preço:
            qstring += f"preço {preço}"
            if venda:
                qstring += ' and '

        if isinstance(venda, str) or isinstance(venda, int):
            qstring += f'venda = {venda}'
        elif venda is False:
            qstring += 'venda IS NULL'
        elif venda is True:
            qstring += 'venda IS NOT NULL'
        
        return qstring

    def insert(self, fabricante, modelo, placa, preço):
        try:
            cursor.execute(f"INSERT INTO motocicletas(fabricante, modelo, placa, preço) VALUES('{fabricante.capitalize()}', '{modelo.upper()}', '{placa.upper()}', {preço:.2f})")
            conexao.commit()
            return True
        except:
            return False

    def get(self, fabricante=None, modelo=None, placa=None, preço=None, venda=None, id= None):
        qstring = self._qstring(fabricante, modelo, placa, preço, venda, id)
        if qstring:
            cursor.execute(f"SELECT * FROM motocicletas WHERE {qstring}")
            return cursor.fetchall()
        else:
            return False
        
    def delete(self, id=None, placa=None):
        qstring = ''
        if id:
            qstring += f"id = {id}"
        elif placa:
            qstring += f"placa = '{placa}'"
        else:
            return False

        cursor.execute(f'DELETE FROM motocicletas WHERE {qstring}')
        conexao.commit()

    def update(self, placa, fabricante=None, modelo=None, preço=None, venda=None, newdata=None):
        qstring = self._qstring(fabricante, modelo, placa, preço, venda)
        if qstring and isinstance(newdata, dict):
            new_value = list(newdata.values())[0]
            key = list(newdata.keys())[0]
            if 'venda' in newdata.keys():
                if not self.validate(venda= new_value):
                    return False

            elif 'preço' in newdata.keys():
                if not self.validate(preço== new_value):
                    return False
            else:
                return False

            if len(client.get(id= new_value)) > 0:
                cursor.execute(f"UPDATE motocicletas SET {key} = {new_value} WHERE {qstring}")
                conexao.commit()
                return True
            else:
                return False

        else:
            return False


class Payments:
    # INSERT INTO pagamentos(cliente_id, produto_id, valor, tipo_pagamento, parcela, total_parcelas, emissao, vencimento, situaçao) VALUES(1, 1, 1.00, 'à vista', 1, 1, '25/05/2023', '25/06/2023', 'pendente')
    def emit(self, clienteId, produto, valor, tipo, parcela, total):
        q1 = client.get(id= clienteId)
        q2 = motocicletas.get(id= produto)
        data_atual = datetime.date.today()
        data_futura = data_atual + datetime.timedelta(days=30)
        if len(q1) == 0 or len(q2) == 0:
            return False
        if q2[0][len(q2[0])-1] == clienteId and parcela <= total:
            try:
                cursor.execute(f"INSERT INTO pagamentos(cliente_id, produto_id, valor, tipo_pagamento, parcela, total_parcelas, emissao, vencimento, situaçao) VALUES({clienteId}, {produto}, {valor:.2f}, '{tipo}', {parcela}, {total}, '{data_atual.strftime('%d/%m/%Y')}', '{data_futura.strftime('%d/%m/%Y')}', 'pendente')")
                conexao.commit()
            except:
                return False
        else:
            return False

    def update(self, id, sit):
            try:
                cursor.execute(f"UPDATE pagamentos SET situaçao = '{sit}' WHERE id = {id}")
                conexao.commit()
            except:
                return False

    def get(self, clientId):
        cursor.execute(f"""
            SELECT clientes.*, motocicletas.fabricante, motocicletas.modelo, motocicletas.placa, motocicletas.preço, pagamentos.*
            FROM clientes
            JOIN motocicletas ON clientes.id = motocicletas.venda
            JOIN pagamentos ON clientes.id = pagamentos.cliente_id
            WHERE clientes.id = {clientId}

        """)
        return cursor.fetchall()


client = Clients()
motocicletas = Motos()
pagamentos = Payments()


# Anotações para teste
#cursor.execute("SELECT * FROM clientes")
#print( cursor.fetchall() )

#pagamentos.emit(clienteId= 1, produto= 2, valor= 1.00, tipo= 'à vista', parcela= 1, total= 1)
# preço= '<= 5'  sqlite version