async function getDados() {
    const response = await fetch('http://127.0.0.1:5000/');
    if (response.ok) {
        const dados = await response.text();
        document.getElementById('saida').textContent = dados;
    } else {
        console.error('Erro ao chamar o endpoint Flask.');
    }
}

async function buscaCliente() {
    const doc_cpf = document.getElementById('cpf').value;
    if (!doc_cpf) {
        alert('Por favor, insira um CPF');
        return;
    }

    const response = await fetch(`http://127.0.0.1:5000/consulta?doc=${doc_cpf}`);
    if (response.ok) {
        const dados = await response.json();
        document.getElementById('nome').textContent = dados.nome;
        document.getElementById('nasc').textContent = dados.data_nascimento;
        document.getElementById('email').textContent = dados.email;
    } else {
        alert('Erro ao buscar cliente.');
    }
}

async function Login() {
    const cpf_login = document.getElementById('loginCpf').value;
    const email_login = document.getElementById('loginEmail').value;  
    
    if (!cpf_login || !email_login) {
        alert('Por favor, insira tanto o CPF quanto o Email');
        return;
    }

    const response = await fetch(`http://127.0.0.1:5000/login?doc=${cpf_login}&email=${email_login}`);
    
    if (response.ok) {
        const dados = await response.json();
        
        if (dados.email === email_login) {
            window.location.href = 'index.html';  
        }
    } else {
        const dados = await response.json();
        alert(dados.erro);  
    }
}

async function deletarCliente() {
    const cpf = document.getElementById('deleteCpf').value;
    
    if (!cpf) {
        document.getElementById('deleteResult').textContent = 'Por favor, insira um CPF.';
        return;
    }

    const response = await fetch(`http://127.0.0.1:5000/deletar?cpf=${cpf}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        const result = await response.text();
        document.getElementById('deleteResult').textContent = result;
    } else {
        document.getElementById('deleteResult').textContent = 'Erro ao deletar cliente.';
    }
}

async function cadastrarCliente() {
    const cpf = document.getElementById('cadcpf').value;
    const nome = document.getElementById('cadnome').value;
    const data_nascimento = document.getElementById('cadnascimento').value;
    const email = document.getElementById('cademail').value;

    const payload = {
        cpf,
        dados: {
            nome,
            data_nascimento,
            email
        }
    };

    const response = await fetch('http://127.0.0.1:5000/cadastro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        alert('Cliente cadastrado com sucesso!');
    } else {
        alert('Erro ao cadastrar cliente. CPF já existente');
    }
}
