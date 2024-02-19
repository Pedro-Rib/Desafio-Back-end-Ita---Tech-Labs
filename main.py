# Importacoes
import re
from flask import Flask, make_response, jsonify, request
from bd import Pessoas
from datetime import datetime


# Instanciando variavel 
app = Flask(__name__)
# Não ordenar o response em ordem alfabética
app.json.sort_keys = False 

### ROTAS CRUD ###

## CREATE | Cadastro
@app.route('/cadastro', methods=['POST'])
def create():
    dados_inseridos = request.json

    ## Validaçoes ##
    
    ## Validacao de campos inseridos
    ############################################################
    nome = dados_inseridos.get('nome', '').strip()
    print (nome)
    data_nascimento = dados_inseridos.get('nascimento', '').strip()
    endereco = dados_inseridos.get('endereco', '').strip()
    cpf = dados_inseridos.get('cpf', '').strip()
    estado_civil = dados_inseridos.get('estado_civil', '').strip()

    # Cria uma lista
    valores = [nome, data_nascimento, endereco, cpf, estado_civil]

    # Verificação se algum campo está vazio
    if any(valor == '' for valor in valores): # Se sim
        return make_response(
            jsonify(
                Mensagem="Por favor, preencha todos os valores solicitados: Nome completo, data de nascimento, endereço, CPF e estado civil."
            ), 400  # Cód. Bad Request
        )
    
    ## Validação de Nome completo e válido
    ############################################################
    # Verifica se possui nome e sobrenome
    if nome.count(" ") < 1:  
        return make_response(
            jsonify(
                Mensagem="Por favor, insira nome e sobrenome."
            ), 400  # Cód. Bad Request
        )
    
    # Verifica se o nome contém números ou caracteres especiais não permitidos
    if re.search(r'[0-9.,/\'":;!@#$%^&*()_+=-]', nome):
        return make_response(
            jsonify(
                Mensagem="O nome não deve conter números ou caracteres especiais."
            ), 400
        )



    ## Validação de data de nascimento 
    ############################################################
    # Checa a existência de letras ou caracteres diferentes de / ou -
    if re.search(r"[^0-9/\-]", data_nascimento):
        return make_response(
            jsonify(Mensagem="Data de nascimento inválida. Utilize apenas números e (/) ou (-) como divisores."), 400
        )

    # Remove separadores para demais validações
    data_nascimento = data_nascimento.replace("/", "").replace("-", "")

    # Verifica se a data inserida possui 8 caracteres
    if not len(data_nascimento) == 8:
        return make_response(
            jsonify(Mensagem="Data de nascimento inválida. O formato deve ser DD/MM/AAAA."), 400
        )

    # Verifica se data condiz com o padrão DD/MM/AAAA e se a idade é menor que 122 anos
    dia_inserido = int(data_nascimento[:2])
    # Dia
    if dia_inserido > 31:
        return make_response(
            jsonify(Mensagem="Data de nascimento inválida. O dia inserido não é válido."), 400
        )
    mes_inserido = int(data_nascimento[2:4])
    # Mês
    if mes_inserido > 12:
        return make_response(
            jsonify(Mensagem="Data de nascimento inválida. O mês inserido não é válido."), 400
        )
    # Ano
    ano_inserido = int(data_nascimento[4:8]) 
    ano_atual = datetime.now().year # Obtém o ano atual
    if ano_inserido >= ano_atual: # Verifica presente ou data futura
        return make_response(
            jsonify(Mensagem="Data de nascimento inválida. O ano inserido não é válido."), 400
        )
    if ((ano_atual - ano_inserido) >= 122 ): # Verifica idade ultrapassa 122 anos
        return make_response(
            jsonify(Mensagem="Data de nascimento inválida. Idade supera os 122 anos."), 400
        )
    
    # Inserindo as barras para formar a data no formato DD/MM/AAAA
    data_nascimento = data_nascimento[:2] + "/" + data_nascimento[2:4] + "/" + data_nascimento[4:]



    ## Validação de endereço
    ############################################################
    # Verifica se endereço possui pelo menos duas palavras
    if endereco.count(" ") < 1:  
        return make_response(
            jsonify(
                Mensagem="Por favor, insira um endereço válido."
            ), 400  # Cód. Bad Request
        )



    ## Validação de CPF
    ############################################################
    # Checa a existência de letras ou caracteres diferentes de . ou -
    if re.search(r"[^0-9.\-]", cpf):
        return make_response(
            jsonify(Mensagem="CPF inválido. Utilize apenas números e (.) ou (-) como divisores se desejar."), 400
        )

    # Remove separadores para demais validações
    cpf = cpf.replace(".", "").replace("-", "")

    # Verifica se o cpf inserido possui 11 caracteres
    if not len(cpf) == 11:
        return make_response(
            jsonify(Mensagem="CPF inválido. Insira um CPF com 11 números com ou sem separadores"), 400
        )

    # Inserindo as separações
    cpf = cpf[:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]



    ## Validação de Estado Civil
    ############################################################
    estado_civil = estado_civil.lower() # Padroniza

    #Verifica se estado civil inserido é válido
    estados_civis = [
    'solteiro', 'solteira',
    'casado', 'casada',
    'divorciado', 'divorciada',
    'viúvo', 'viúva',
    'viuvo', 'viuva',
    'separado','separada',
    'separado judicialmente', 'separada judicialmente'
    ]
    if not estado_civil in estados_civis:
        return make_response(
            jsonify(Mensagem="Estado civil inválido. Insira uma das opções: Solteiro(a), Casado(a), Divorciado(a), Viúvo(a) ou Separado(a) judicialmente."), 400
        )
    
    # Formata a primeira letra como maiuscula para inserção no BD
    estado_civil = estado_civil[0].upper() + estado_civil[1:]
    ############################################################
    ## Fim das validações



    # Gerando nova ID para inserção no BD
    if Pessoas:  # Verifica se a lista nao esta vazia
        novo_id = max(pessoa['id'] for pessoa in Pessoas) + 1
    else:
        novo_id = 1 

    # Adicionando o 'ID' como primeira linha do item
    pessoa_com_id = {'id': novo_id,
                     'nome': nome,
                     'data_nascimento': data_nascimento,
                     'endereco': endereco,
                     'cpf': cpf,
                     'estado_civil': estado_civil}

    # Adiciona ao BD
    Pessoas.append(pessoa_com_id)

    # Solicitando e tratando retorno
    return make_response (
        jsonify (
            Mensagem = 'Pessoa cadastrada com sucesso!',
            Pessoa = pessoa_com_id), 201
    ) 

## READ | Listagem
@app.route('/listagem', methods=['GET'])
def read():
    return make_response(
        jsonify (
            Titulo='Pessoas Cadastradas',
            Pessoas=Pessoas)
        ) 

## UPDATE | Atualização
@app.route('/atualizar/<int:pessoa_id>', methods=['PUT'])
def update(pessoa_id):
    global Pessoas
    dados_atualizados = request.json

    # Iniciar a variavel de controle
    pessoa_encontrada = None
    
    # Procura pela pessoa com o ID fornecido na lista de pessoas
    for pessoa in Pessoas:
        if pessoa['id'] == pessoa_id:
            pessoa_encontrada = pessoa
            break  # Se encontrada interrompe o loop

    if pessoa_encontrada:
        # Atualiza os dados, verificando se cada campo foi fornecido
        pessoa_encontrada['nome'] = dados_atualizados.get('nome', pessoa['nome']).strip()
        pessoa_encontrada['nascimento'] = dados_atualizados.get('nascimento', pessoa['nascimento']).strip()
        pessoa_encontrada['endereco'] = dados_atualizados.get('endereco', pessoa['endereco']).strip()
        pessoa_encontrada['cpf'] = dados_atualizados.get('cpf', pessoa['cpf']).strip()
        pessoa_encontrada['estado_civil'] = dados_atualizados.get('estado_civil', pessoa['estado_civil']).strip()
        
        ## Validaçoes ##
        ## Validacao de campos inseridos
        ############################################################
        nome = dados_atualizados.get('nome', pessoa_encontrada['nome']).strip()
        data_nascimento = dados_atualizados.get('nascimento', pessoa_encontrada['nascimento']).strip()
        endereco = dados_atualizados.get('endereco', pessoa_encontrada['endereco']).strip()
        cpf = dados_atualizados.get('cpf', pessoa_encontrada['cpf']).strip()
        estado_civil = dados_atualizados.get('estado_civil', pessoa_encontrada['estado_civil']).strip()


        ## Validação de Nome completo e válido
        ############################################################
        # Verifica se possui nome e sobrenome
        if nome.count(" ") < 1:  
            return make_response(
                jsonify(
                    Mensagem="Por favor, insira nome e sobrenome."
                ), 400  # Cód. Bad Request
            )
        
        # Verifica se o nome contém números ou caracteres especiais não permitidos
        if re.search(r'[0-9.,/\'":;!@#$%^&*()_+=-]', nome):
            return make_response(
                jsonify(
                    Mensagem="O nome não deve conter números ou caracteres especiais."
                ), 400
            )



        ## Validação de data de nascimento 
        ############################################################
        # Checa a existência de letras ou caracteres diferentes de / ou -
        if re.search(r"[^0-9/\-]", data_nascimento):
            return make_response(
                jsonify(Mensagem="Data de nascimento inválida. Utilize apenas números e (/) ou (-) como divisores."), 400
            )

        # Remove separadores para demais validações
        data_nascimento = data_nascimento.replace("/", "").replace("-", "")
        print (data_nascimento)

        # Verifica se a data inserida possui 8 caracteres
        if not len(data_nascimento) == 8:
            return make_response(
                jsonify(Mensagem="Data de nascimento inválida. O formato deve ser DD/MM/AAAA."), 400
            )
        print (data_nascimento)

        # Verifica se data condiz com o padrão DD/MM/AAAA e se a idade é menor que 122 anos
        dia_inserido = int(data_nascimento[:2])
        # Dia
        if dia_inserido > 31:
            return make_response(
                jsonify(Mensagem="Data de nascimento inválida. O dia inserido não é válido."), 400
            )
        mes_inserido = int(data_nascimento[2:4])
        # Mês
        if mes_inserido > 12:
            return make_response(
                jsonify(Mensagem="Data de nascimento inválida. O mês inserido não é válido."), 400
            )
        # Ano
        ano_inserido = int(data_nascimento[4:8]) 
        ano_atual = datetime.now().year # Obtém o ano atual
        if ano_inserido >= ano_atual: # Verifica presente ou data futura
            return make_response(
                jsonify(Mensagem="Data de nascimento inválida. O ano inserido não é válido."), 400
            )
        if ((ano_atual - ano_inserido) >= 122 ): # Verifica idade ultrapassa 122 anos
            return make_response(
                jsonify(Mensagem="Data de nascimento inválida. Idade supera os 122 anos."), 400
            )
        print (data_nascimento)

        # Inserindo as barras para formar a data no formato DD/MM/AAAA
        data_nascimento = data_nascimento[:2] + "/" + data_nascimento[2:4] + "/" + data_nascimento[4:]
        print (data_nascimento)


        ## Validação de endereço
        ############################################################
        # Verifica se endereço possui pelo menos duas palavras
        if endereco.count(" ") < 1:  
            return make_response(
                jsonify(
                    Mensagem="Por favor, insira um endereço válido."
                ), 400  # Cód. Bad Request
            )



        ## Validação de CPF
        ############################################################
        # Checa a existência de letras ou caracteres diferentes de . ou -
        if re.search(r"[^0-9.\-]", cpf):
            return make_response(
                jsonify(Mensagem="CPF inválido. Utilize apenas números e (.) ou (-) como divisores se desejar."), 400
            )

        # Remove separadores para demais validações
        cpf = cpf.replace(".", "").replace("-", "")

        # Verifica se o cpf inserido possui 11 caracteres
        if not len(cpf) == 11:
            return make_response(
                jsonify(Mensagem="CPF inválido. Insira um CPF com 11 números com ou sem separadores"), 400
            )

        # Inserindo as separações
        cpf = cpf[:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]



        ## Validação de Estado Civil
        ############################################################
        estado_civil = estado_civil.lower() # Padroniza

        #Verifica se estado civil inserido é válido
        estados_civis = [
        'solteiro', 'solteira',
        'casado', 'casada',
        'divorciado', 'divorciada',
        'viúvo', 'viúva',
        'viuvo', 'viuva',
        'separado','separada',
        'separado judicialmente', 'separada judicialmente'
        ]
        if not estado_civil in estados_civis:
            return make_response(
                jsonify(Mensagem="Estado civil inválido. Insira uma das opções: Solteiro(a), Casado(a), Divorciado(a), Viúvo(a) ou Separado(a) judicialmente."), 400
            )
        
        # Formata a primeira letra como maiuscula para inserção no BD
        estado_civil = estado_civil[0].upper() + estado_civil[1:]
        ############################################################
        ## Fim das validações

        # Atualizando variaveis
        pessoa_encontrada['nome'] = nome
        pessoa_encontrada['nascimento'] = data_nascimento
        pessoa_encontrada['endereco'] = endereco
        pessoa_encontrada['cpf'] = cpf
        pessoa_encontrada['estado_civil'] = estado_civil

        # Retorna resposta de sucesso
        return make_response(jsonify({'Mensagem': f"Pessoa '{pessoa_encontrada['nome']}' atualizada com sucesso!"}), 200)

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
    return jsonify({"error": "Bad Request", "message": "O servidor não conseguiu entender a requisição devido a sintaxe inválida."}), 400

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