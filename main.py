### API desenvolvida em resposta ao desafio TechLabs para a vaga de estágio em Desenvolvimento no Itaú Unibando.
### Desenvolvido por: Pedro Ribeiro Silva.

### IMPORTAÇÕES ###
import re
from flask import Flask, make_response, jsonify, request
from bd import Pessoas
from datetime import datetime

# Instanciando variavel 
app = Flask(__name__)
app.json.sort_keys = False # Não ordenar o response em ordem alfabética


### FUNÇÕES ###
## FUNÇÕES > VALIDAÇÕES ( CREATE | UPDTAE ) ##
def valida_nome(nome):
    # Verifica se possui nome e sobrenome
    if nome.count(" ") < 1:
        return "Por favor, insira nome e sobrenome."
    
    # Verifica se o nome contém números ou caracteres especiais não permitidos
    if re.search(r'[0-9.,/\'":;!@#$%^&*()_+=-]', nome):
        return "O nome não deve conter números ou caracteres especiais."

    # Todas as validações foram aprovadas. Retorna sem erros
    return None

def valida_data_nascimento(data_nascimento):
    #Limpa a data de nascimento inserida, deixando apenas números
    data_nascimento = re.sub(r'[^0-9]', '', data_nascimento)
    print (data_nascimento)
    
    # Verifica se a data inserida possui 8 caracteres
    if not len(data_nascimento) == 8:
        return "Data de nascimento inválida. A data deve conter 8 números no padrão Dia/Mês/Ano. Com ou sem separador."
    
    # Verifica se a data condiz com o padrão DD/MM/AAAA,
                            # se o ano não é futuro e
                            # se a idade é menor que 122 anos.
    dia, mes, ano = int(data_nascimento[:2]), int(data_nascimento[2:4]), int(data_nascimento[4:8])
    
    # Obter a data atual
    data_atual = datetime.now()

    # Verificações básicas de validade da data
    if dia > 31:
        return "Data de nascimento inválida. Verifique o dia inserido."
    if mes > 12:
        return "Data de nascimento inválida. Verifique o mês inserido."
    
    if ano > data_atual.year or (ano == data_atual.year and mes > data_atual.month) or \
    (ano == data_atual.year and mes == data_atual.month and dia > data_atual.day):
        return f"Data de nascimento inválida. A data inserida é futura: {dia}/{mes}/{ano}."
    
    if (data_atual.year - ano) > 122 or ((data_atual.year - ano) == 122 and (data_atual.month < mes or (data_atual.month == mes and data_atual.day < dia))):
        return "Data de nascimento inválida. A idade supera os 122 anos."
    
    # Todas as validações foram aprovadas. Retorna a função sem erros
    return None

def valida_endereco(endereco):
    # Verifica se endereço possui pelo menos duas palavras
    if endereco.count(" ") < 1:
        return "Por favor, insira um endereço válido."
    
    # Todas as validações foram aprovadas. Retorna a função sem erros
    return None

def valida_cpf(cpf):
    # Limpa o cpf inserido, deixando apenas números
    cpf = re.sub(r'[^0-9]', '', cpf)

    # Verifica se o cpf inserido possui 11 caracteres
    if len(cpf) != 11:
        return "CPF inválido. Insira um CPF com 11 números com ou sem separadores."

    # Verifica validade do primeiro dígito verificador
    soma_produtos = sum(int(a)*b for a, b in zip(cpf[0:9], range(10, 1, -1)))
    digito_esperado = (soma_produtos * 10 % 11) % 10
    if int(cpf[9]) != digito_esperado:
        return "CPF inválido. Insira um CPF válido."

    # Verifica validade do segundo dígito verificador
    soma_produtos1 = sum(int(a)*b for a, b in zip(cpf[0:10], range(11, 1, -1)))
    digito_esperado1 = (soma_produtos1 * 10 % 11) % 10
    if int(cpf[10]) != digito_esperado1:
        return "CPF inválido. Insira um CPF válido."

    # Todas as validações foram aprovadas. Retorna a função sem erros
    return None

def valida_estado_civil(estado_civil):
    estados_civis_validos = [
    'solteiro', 'solteira',
    'casado', 'casada',
    'divorciado', 'divorciada',
    'viúvo', 'viúva',
    'viuvo', 'viuva',
    'separado','separada',
    'separado judicialmente', 'separada judicialmente'
    ]   

    #Verifica se estado civil inserido é válido
    if estado_civil.lower() not in estados_civis_validos:
        return "Estado civil inválido. Insira uma das opções: Solteiro(a), Casado(a), Divorciado(a), Viúvo(a) ou Separado(a) judicialmente."
    
    # Todas as validações foram aprovadas. Retorna a função sem erros
    return None

## FUNÇÕES > FORMATAÇÕES ( CREATE | UPDTAE ) ##
def formata_cpf(cpf):
    # Limpa o cpf inserido
    cpf = re.sub(r'[^0-9]', '', cpf)

    # Retorna o cpf formatado no padrão nacional
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formata_data_nascimento(data_nascimento):
    #Limpa a data de nascimento inserida, deixando apenas números
    data_nascimento = re.sub(r'[^0-9]', '', data_nascimento)
    return data_nascimento[:2] + "/" + data_nascimento[2:4] + "/" + data_nascimento[4:]

def formata_estado_civil(estado_civil):
    return estado_civil[0].upper() + estado_civil[1:].lower()

## FUNÇÕES > DEMAIS FUNÇÕES ##
def sobe_estrtura_formatada (nome,data_nascimento,endereco,cpf,estado_civil): # Gera estrutura de dados formatados e insere no "BD"
    
    # Verifica se a lista importatada do "BD" nao esta vazia e gera ID da pessoa
    if Pessoas:  
        novo_id = max(pessoa['id'] for pessoa in Pessoas) + 1
    else:
        novo_id = 1 

    # Montando estrtura de dados validada
    estrutura_de_dados_validada = {'id': novo_id,
                                  'nome': nome.title(),
                                  'data_nascimento': data_nascimento,
                                  'endereco': endereco.title(),
                                  'cpf': cpf,
                                  'estado_civil': estado_civil}

    # Adiciona ao "BD"
    Pessoas.append(estrutura_de_dados_validada)

    return estrutura_de_dados_validada


### ROTAS CRUD ###
## CREATE | Cadastro
@app.route('/cadastro', methods=['POST'])
def create():
    # Converte body do request
    dados_inseridos = request.json

    # Associa respostas inseridas às variáveis de controle
    nome = dados_inseridos.get('nome', '').strip()
    data_nascimento = dados_inseridos.get('data_nascimento', '').strip()
    endereco = dados_inseridos.get('endereco', '').strip()
    cpf = dados_inseridos.get('cpf', '').strip()
    estado_civil = dados_inseridos.get('estado_civil', '').strip()

    # Cria dicionário com a estrutura de dados e as respostas do usuário
    estrutura_e_dados_inseridos = { 
        "nome": nome,
        "data de nascimento": data_nascimento,
        "endereço": endereco,
        "CPF": cpf,
        "estado civil": estado_civil
    }

    # VALIDAÇÕES #
    # Campos preenchidos
    for campo, valor in estrutura_e_dados_inseridos.items(): # Loop pelos itens do dicionário de respostas
        if valor == '': # Se algum campo estiver vazio:
            return make_response(jsonify(Mensagem=f"Por favor, preencha o campo de {campo} para continuar."), 400) #Bad Request
            
    # Loop pelas demais funções de validações (nome, data_nascimento, endereço, cpf e estado_civil)
    for validar, valor in [(valida_nome, nome),
                           (valida_data_nascimento, data_nascimento),
                           (valida_endereco, endereco),
                           (valida_cpf, cpf),
                           (valida_estado_civil, estado_civil)]:
        erro = validar(valor)

        if erro:
            return make_response(jsonify(Mensagem= erro), 400)

    # FORMATAÇÕES #
    data_nascimento = formata_data_nascimento(data_nascimento)
    cpf = formata_cpf(cpf)
    estado_civil = formata_estado_civil(estado_civil)

    # FINALIZAÇÃO DO CREATE #
    pessoa_validada = sobe_estrtura_formatada (nome, data_nascimento, endereco, cpf, estado_civil)

    # Solicitando e tratando retorno
    return make_response (jsonify (Mensagem = f"Pessoa '{pessoa_validada['nome']}' cadastrada com sucesso!",
                                   Dados_cadastrados = pessoa_validada), 201) # Created
    
## READ | Listagem
@app.route('/listagem', methods=['GET'])
def read():
    return make_response(
        jsonify (
            Solicitação='Listagem de pessoas cadastradas no banco de dados',
            Resposta=Pessoas)
        ) 

## UPDATE | Atualização
@app.route('/atualizar/<int:pessoa_id>', methods=['PUT'])
def update(pessoa_id):
    global Pessoas

    # Converte body do request
    dados_para_atualizar = request.json

    # Iniciar a variavel de controle
    pessoa_encontrada = None
    
    # Procura pela pessoa com o ID fornecido na lista de pessoas
    for pessoa in Pessoas:
        if pessoa['id'] == pessoa_id:
            pessoa_encontrada = pessoa
            break  # Se encontrada interrompe o loop

    # Verifica se a pessoa foi encontrada
    if pessoa_encontrada:
        # Campos que podem ser atualizados
        campos = ['nome', 'data_nascimento', 'endereco', 'cpf', 'estado_civil']
        
        # Dicionário para armazenar os valores atualizados
        valores_atualizados = {}
        
        # Atualiza os dados da pessoa encontrada
        for campo in campos:
            valor_atualizado = dados_para_atualizar.get(campo, pessoa_encontrada[campo]).strip()
            pessoa_encontrada[campo] = valor_atualizado
            valores_atualizados[campo] = valor_atualizado
        
        # Atualiza as variáveis locais
        nome = valores_atualizados['nome']
        data_nascimento = valores_atualizados['data_nascimento']
        endereco = valores_atualizados['endereco']
        cpf = valores_atualizados['cpf']
        estado_civil = valores_atualizados['estado_civil']

        # VALIDAÇÕES #
        # Loop pelas funções de validações (nome, data_nascimento, endereço, cpf e estado_civil)
        for validar, valor in [(valida_nome, nome),
                            (valida_data_nascimento, data_nascimento),
                            (valida_endereco, endereco),
                            (valida_cpf, cpf),
                            (valida_estado_civil, estado_civil)]:
            erro = validar(valor)

            if erro:
                return make_response(jsonify(Mensagem= erro), 400)

        # FORMATAÇÕES #
        data_nascimento = formata_data_nascimento(data_nascimento)
        cpf = formata_cpf(cpf)
        estado_civil = formata_estado_civil(estado_civil)

        # Montando e atualizando estrutura de dados validada
        pessoa_encontrada.update({
            'nome': nome.title(),
            'data_nascimento': data_nascimento,
            'endereco': endereco.title(),
            'cpf': cpf,
            'estado_civil': estado_civil
        })

        # Retorna resposta de sucesso
        return make_response(jsonify({'Mensagem': f"Pessoa '{pessoa_encontrada['nome']}' atualizada com sucesso!",
                              'Ficha_atualizada': pessoa_encontrada}), 200) #OK

    else:
        # Caso a pessoa com o ID fornecido não seja encontrada
        return make_response(jsonify(Mensagem="Pessoa não encontrada."), 404)       

## DELETE | Exclusão
@app.route('/excluir/<int:pessoa_id>', methods=['DELETE'])
def delete(pessoa_id):
    global Pessoas

    pessoa_encontrada = None # Iniciar a variavel de controle
    
    # Procura pela pessoa com o ID fornecido na lista de pessoas
    for pessoa in Pessoas:
        if pessoa['id'] == pessoa_id:
            pessoa_encontrada = pessoa
            break  # Se encontrada interrompe o loop

    if pessoa_encontrada:
        # Cria uma nova lista excluindo a pessoa com o ID fornecido
        nova_lista = []
        for pessoa in Pessoas:
            if pessoa['id'] != pessoa_id:
                nova_lista.append(pessoa)
        Pessoas = nova_lista  # Atualiza a lista global 'Pessoas' com a nova lista

        # Retorna resposta de sucesso
        return make_response(jsonify({'Mensagem': f"Pessoa '{pessoa_encontrada['nome']}' excluída com sucesso!"}), 200)

    else:
        # Caso a pessoa com o ID fornecido não seja encontrada
        return make_response(jsonify(Mensagem="Pessoa não encontrada."), 404)       


### TRATAMENTO DE ERROS GLOBAIS ###
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": "Sintaxe inválida."}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "O servidor não pode encontrar o recurso solicitado."}), 404

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({"error": "Unprocessable Entity", "message": "O servidor entende o tipo de conteúdo da solicitação e a sintaxe está correta, mas não foi capaz de processar as instruções contidas."}), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "message": "O servidor encontrou uma situação com a qual não sabe lidar."}), 500

@app.errorhandler(501)
def not_implemented(error):
    return jsonify({"error": "Not Implemented", "message": "O método da solicitação não é suportado pelo servidor e não pode ser manipulado."}), 501

@app.errorhandler(503)
def service_unavailable(error):
    return jsonify({"error": "Service Unavailable", "message": "Servidor em sobrecarga ou manutenção."}), 503

@app.errorhandler(504)
def gateway_timeout(error):
    return jsonify({"error": "Gateway Timeout", "message": "O servidor não recebeu uma resposta a tempo."}), 504


# Iniciar API
app.run()