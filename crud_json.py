import json, os

class CRUD:
    def __init__(self, path):
        self._data = []
        complete_path = f'src/{path}/'
        if os.path.exists(complete_path):
            for nome_arquivo in os.listdir(complete_path):
                if nome_arquivo.endswith('.json'):
                    #try:
                        int(nome_arquivo[0:len(nome_arquivo)-5])
                        with open(complete_path+nome_arquivo) as arquivo:
                            i = json.load(arquivo)
                            print(i)
                            if i not in self._data:
                                self._data.append(i)
                    #except:
                        #pass


    def insert(self, **kwargs):
        entry_id = len(self._data) + 1
        content = kwargs
        content['id'] = entry_id
        if self._validate(content) and content not in self._data:
            self._data.append(content)
            if not os.path.exists('src'):
                os.makedirs('src')
                os.makedirs('client')
                os.makedirs('motocicletas')
                os.makedirs('pagamentos')
            self.save_to_json(content)
        else:
            print(f'Error creating {content}')

    def get(self, **kwargs):
        results = []
        for indice in self._data:
            match = True
            for key, value in kwargs.items():
                if key in indice.keys():
                    if isinstance(value, str) and isinstance(indice[key], str):
                        if value not in indice[key] or indice in results:
                            match = False
                    else:
                        if value != indice[key] or indice in results:
                            match = False

            if match:
                results.append(indice)

        return results

    def update(self, old_value, newdata):
        key = list( newdata.keys() )[0]
        new_value = list( newdata.values() )[0]
        if self._validate(newdata):
            for indice in self._data:
                if old_value in indice.values():
                    indice[key] = new_value
                    self.save_to_json(indice)
        else:
            print(f'\nError updating {old_value, newdata}\n')

    def delete(self, key, value):
        for indice in self._data:
            if value == indice[key]:
                self._data.remove(indice)
                self.delete_json(indice['id'])

    def save_to_json(self, content_entry, path):
        if len(content_entry) > 0:
            filename = path + str(content_entry['id']) + '.json'
            with open(filename, 'w') as file:
                json.dump(content_entry, file)
                print('Inserted!')
        else:
            print(f'Failed to create {content_entry}')

    def delete_json(self, id, path):
        filename = path + str(id) + '.json'
        try:
            os.remove(filename)
        except OSError:
            print(f'Failed to delete {filename}')


class Cliente(CRUD):
    def __init__(self):
        super().__init__('client')

    def update(self, old_cpf, newdata):
        return super().update(old_cpf, newdata)

    def delete(self, cpf):
        return super().delete('cpf', cpf)

    def save_to_json(self, c):
        return super().save_to_json(c, 'src/client/')

    def delete_json(self, id):
        return super().delete_json(id, 'src/client/')

    def _validate(self, content):
        if 'cpf' in content.keys():
            try:
                if len(str(content['cpf'])) == 11:
                    if isinstance(content['cpf'], int) and len( client.get(cpf= content['cpf']) ) <= 0:
                        return True
            except ValueError:
                return False

        elif 'nome' in content.keys():
            return True

        else:
            return False


class Motocicleta(CRUD):
    def __init__(self):
        super().__init__('motocicletas')

    def update(self, placa, newdata):
        return super().update(placa, newdata)

    def delete(self, placa):
        return super().delete('placa', placa)

    def insert(self, **kwargs):
        if 'venda' not in kwargs.keys():
            kwargs['venda'] = ''

        return super().insert(**kwargs)

    def save_to_json(self, c):
        return super().save_to_json(c, 'src/motocicletas/')

    def delete_json(self, id):
        return super().delete_json(id, 'src/motocicletas/')

    def get(self, **kwargs):
        qdict = {}
        for key, value in kwargs.items():
            if key != 'preço' and key != 'venda':
                qdict[key] = value

        res = super().get(**qdict)
        venda = None

        if 'preço' in kwargs.keys():
            res = list( filter(lambda i: kwargs['preço']-50 <= i['preço'] <= kwargs['preço']+50, res) )

        if 'venda' in kwargs.keys():
            venda = kwargs['venda']
        else:
            return res
        
        if isinstance(venda, int):
            return list( filter(lambda i: i['venda'] == venda, res) )
        
        elif venda == True:
            return list( filter(lambda i: i['venda'] != '', res) )
        
        elif venda == False:
            return list( filter(lambda i: i['venda'] == '', res) )


    def _validate(self, content):
        keys = [ 'id', 'fabricante', 'modelo', 'placa', 'preço', 'venda' ]
        t1 = [ 'fabricante', 'modelo', 'placa' ]
        for key in content.keys():
            if key not in keys and key != 'venda':
                return False

        if 'preço' in content.keys():
            try:
                format(content['preço'], '.2f')
            except:
                return False


        for i in t1:
            if i in content.keys():
                if not isinstance(content[i], str):
                    return False

        if 'venda' in content.keys():
            if content['venda'] != '':
                if not isinstance(content['venda'], int) or len( client.get(id= content['venda']) ) <= 0:
                    return False
        
        if 'placa' in content.keys():
            if len( motocicletas.get(placa= content['placa']) ) > 0:
                return False

        return True


class Venda:
    def __init__(self):
        CRUD.__init__(self, 'pagamentos')
    def emit(self, **kwargs):
        kwargs['situaçao'] = 'pendente'
        CRUD.insert(self, **kwargs)
    def save_to_json(self, c):
        return CRUD.save_to_json(self, c, 'src/pagamentos/')

    def _validate(self, content):
        keys = [ 'id', 'cliente', 'produto', 'valor', 'tipo_pagamento', 'parcela', 'total_parcelas', 'emissão', 'vencimento', 'situaçao' ]
        for key in content.keys():
            if key not in keys and key != 'situaçao':
                print('dada')
                return False

        try:
            format(content['valor'], '.2f')
        except:
            return False

        if isinstance(content['parcela'], int) and isinstance(content['total_parcelas'], int):
            if content['parcela'] > content['total_parcelas']:
                return False
        else:
            return False

        if 'situacão' in content.keys():
            if content['situaçao'] != 'pago' and content['situaçao'] != 'pendente':
                return False
        
        product = motocicletas.get(id= content['produto'])[0]
        if len( client.get(id= content['cliente']) ) <= 0 or len(product) <= 0:
            return False

        if product['venda'] != content['cliente']:
            return False

        return True
    
    def get(self, clientId):
        for indice in self._data:
            if indice['id'] == clientId:
                return indice
        
        return []
    
    def update(self, id, sit):
        for indice in self._data:
            if indice['id'] == id and sit == 'pago':
                indice['situaçao'] = sit


client = Cliente()
motocicletas = Motocicleta()
pagamentos = Venda()
