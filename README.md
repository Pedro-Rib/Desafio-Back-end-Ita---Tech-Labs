# Desafio Backend - Itaú Unibanco

---

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/b1426c89-decf-4a8a-ae27-4afdc51fe236" width="150px" />
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/22234698-83de-4f65-a490-3c5653ed2aae" width="200px" />
</div>

---

**Objetivo:** Desenvolver uma API em Python para cadastro e gestão de pessoas. Seguindo o padrão CRUD, a aplicação deve **registrar, consultar, atualizar** e **excluir** informações básicas de pessoas, como **nome, data de nascimento, endereço, CPF** e **estado civil**. 

<br>

### 📋 Pré-requisitos

---

✅ | **Python 3.12.1**

✅ | **Framework Flask 3.0.2**

✅ | **Postman** (ou qualquer outra plataforma de colaboração para desenvolvimento de APIs)

<br>

### 🏗️  Estruturas de dados:

---

A seguinte **estrutura de dados** deve ser utilizada no corpo das *requests* de **cadastro** e **atualização:**

```python
{
  "nome": "Nome da Silva",
  "data_nascimento": "12/07/1997",
  "endereco": "Av. do Estado, 200",
  "cpf": "643.124.040-54",
  "estado_civil": "solteiro"
}
```

**→ Atualizações:**

Para as operações de **atualização** você pode preencher a estrutura apenas com os campos que quer atualizar:

```python
{
  "endereco": "Av. Paulista, 225",
  "estado_civil": "casado"
}
```

<br>

### **⚙️ Como testar**

---

**1.** Clone o repositório, abra o diretório com sua IDE de preferência e crie um ambiente virtual através do seguinte comando no terminal da IDE:

```python
python3 -m venv venv
```

**2.** Ative o ambiente virtual:

- Windows
    
    ```python
    .\venv\Scripts\activate
    ```
    
- MacOS e Linux
    
    ```python
    source venv/bin/activate
    ```
    

**3.** Instale as bibliotecas e dependências necessárias através do seguinte comando no terminal:

```python

pip install -r requirements.txt
```

**4.**  Execute o scrip **"main.py”** e copie seu link de hospedagem local para usarmos na *request*:

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/4addc7a4-f0cc-4a90-a73d-f28bbf2ac182" width="626px" />
</div>

**5.** Utilizando o **[Postman](https://www.postman.com/downloads/),** você deve criar uma nova workspace e depois uma *request* do tipo HTTP.

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/01dadc8b-5100-4955-bc30-12cd0a97baf1" width="626px" />
</div>

**6.** Monte seu link da *request* com o endereço copiado no terminal da IDE e adicione ao seu final o *endpoint* de uma das quatro opções da operação CRUD. Não se esqueça de selecionar o tipo de *request* também:

**1. CREATE:** Cadastro de pessoa  
&nbsp;&nbsp;&nbsp;&nbsp;**Request:** POST  
&nbsp;&nbsp;&nbsp;&nbsp;**Final:** /cadastro  
&nbsp;&nbsp;&nbsp;&nbsp;**Exemplo:** [http://127.0.0.1:5000/cadastro](http://127.0.0.1:5000/cadastro)

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/f7fcd1ab-f632-475c-9af1-50d169803e4b" width="626px" />
</div>

<br>

**2. READ:** Listagem de itens no Banco de Dados  
&nbsp;&nbsp;&nbsp;&nbsp;**Request:** GET  
&nbsp;&nbsp;&nbsp;&nbsp;**Final:** /listagem  
&nbsp;&nbsp;&nbsp;&nbsp;**Exemplo:** [http://127.0.0.1:5000/listagem](http://127.0.0.1:5000/listagem)

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/1017b740-f46d-4f05-8ac8-08ad39d9655a" width="626px" />
</div>

<br>

**3. UPDATE:** Atualização de dados de pessoas já cadastradas  
&nbsp;&nbsp;&nbsp;&nbsp;**Request:** PUT  
&nbsp;&nbsp;&nbsp;&nbsp;**Final:** /atualizar/**n_id**   **(← Substituir pelo ID em questão)**  
&nbsp;&nbsp;&nbsp;&nbsp;**Exemplo:** [http://127.0.0.1:5000/atualizar/1](http://127.0.0.1:5000/atualizar/1)

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/cb8b48c2-d10b-4b0c-b975-18c5e9847e85" width="626px" />
</div>

<br>

**4. DELETE:** Operação para deletar pessoas cadastradas  
&nbsp;&nbsp;&nbsp;&nbsp;**Request:** DEL  
&nbsp;&nbsp;&nbsp;&nbsp;**Final:** /excluir/**n_id**   **(← Substituir pelo ID em questão)**  
&nbsp;&nbsp;&nbsp;&nbsp;**Exemplo:** [http://127.0.0.1:5000/excluir/2](http://127.0.0.1:5000/excluir/2)

<div align="center">
  <img src="https://github.com/Pedro-Rib/Desafio_Backend_Itau_TechLabs/assets/140509507/89711d81-58eb-4801-8d73-293aba08c060" width="626px" />
</div>

<br>

### ✅ Validações, tratamentos de **exceções e** formatação de dados recebidos

---

**1. Geral**

- Tratamentos de exceções:
    - Espaços no começo e no fim das entradas são descartados para evitar problemas.
- Validações:
    - No **cadastramento**, todos os campos da estrutura de dados precisam ser preenchidos para continuar.

<br>

**2. Nome**

- Validações:
    - Para garantir a inserção de **nomes completos** é necessário que o nome inserido possua pelo menos **nome** e **sobrenome**;
    - Todos os caracteres devem ser **letras**.
- Formatações:
    - A primeira letra de cada nome é formatada para maiúscula caso inserido em caixa baixa;

<br>

**3.** **Data de nascimento**

- Tratamentos de exceções:
    - Ignora qualquer caracter diferente de números, portanto, as datas podem ser inseridas com quaisquer tipos de separadores (11/22/3333, 11.22.3333, etc…);
    - As datas podem ser inseridas sem separadores (11223333).
- Validações:
    - Valida a existência de oito números na data inserida;
    - Valida se a data condiz com o padrão DD/MM/AAAA;
    - Verifica se o mês supera 31 dias;
    - Se o ano supera 12 meses;
    - Se o ano inserido é futuro;
    - Valida se a idade ultrapassa ou 122 anos (maior idade já registrada no mundo).
- Formatações:
    - Formata a data com os divisores "/” (22022000 → 22/02/2000) antes de inserir no banco de dados.

<br>

**4.** **Endereço**

- Validações:
    - Valida se o endereço possui pelo menos duas palavras.
- Formatações:
    - Formata a primeira letra de cada nome para maiúscula caso inserido em caixa baixa.

<br>

**5.** **CPF**

- Tratamentos de exceções:
    - Ignora qualquer caractere diferente de números, descartando possíveis erros de digitação;
    - Os CPF's podem ser inserido sem separadores (33261471874).
- Validações:
    - Verifica se o CPF possui 11 dígitos;
    - Verifica separadamente a validade dos dígitos verificadores.
- Formatações:
    - Formata o CPF para o padrão nacional (33261471874 → 332.614.718-74) antes de inserir no banco de dados.
 
<br>

**6.** **Estado Civil**

- Tratamentos de exceções:
    - Os dados pode ser escritos em maiúsculo ou minúsculo;
    - ”Viúvo(a)” pode ser escrito com ou sem acento.
- Validações:
    - Valida se o valor é compatível com as opções oficiais:
        - Solteiro(a);
        - Casado(a);
        - Divorciado(a);
        - Viúvo(a);
        - Separado(a) judicialmente.
- Formatações:
    - A primeira letra da inserção é formatada para maiúscula antes de ser inserida no banco de dados.

<br>

### **🛠️ Construído com**

---

- Linguagem: **Python 3.12.1**
    
    [Download Python](https://www.python.org/downloads/)
    
- Framework: **Flask 3.0.2**
    
    ```python
    $ pip install Flask
    ```
    
- Banco de dados: **Em memória**
    - Scrip "bd.py” com dicionário simulando um Banco de Dados
- Bibliotecas: **2 Nativas**
    - **re**
        
        ```python
        import re
        ```
        
    - **datetime**
        
        ```python
        from datetime import datetime
        ```
        
<br>

### **✒️ Autor**

---

- Pedro Ribeiro Silva
