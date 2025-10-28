# Medora — Sistema de Agenda Médica

> **Agende, gerencie e acompanhe consultas médicas de qualquer especialidade em 
um só lugar.**

O **Medora** é um sistema web desenvolvido com **Django** e **PostgreSQL**, 
criado para facilitar o agendamento de consultas médicas, o gerenciamento de 
agendas de profissionais de saúde e o acompanhamento de pacientes.  
Ideal para **clínicas, consultórios ou sistemas de telemedicina**, o Medora 
oferece uma experiência moderna, ágil e segura.

---

## Funcionalidades Principais

- **Cadastro de médicos** com especialidade, horário de atendimento e dados 
profissionais.  
- **Cadastro de pacientes** com histórico médico e informações de contato.  
- **Agendamento de consultas** com verificação automática de conflito de 
horários.  
- **Controle de status** (Agendada, Confirmada, Cancelada, Realizada).  
- **Busca por médico, paciente ou data**.  

---

## Arquitetura

| Camada | Tecnologia |
|---------|-------------|
| **Backend** | Django 5 + Django ORM |
| **Banco de Dados** | PostgreSQL 15 |
| **Frontend** | HTML5, Bootstrap 5 (ou Django Templates) |
| **Autenticação** | Django Auth (usuários: médico, paciente, admin) |
| **APIs (futuro)** | Django REST Framework |
| **Tarefas assíncronas (futuro)** | Celery + Redis |
| **Infraestrutura (opcional)** | Docker + Docker Compose |

---

## Estrutura do Projeto

```bash
medora/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── core/ # Configurações principais do projeto
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── agenda/ # App principal: agendamento de consultas
│ ├── models.py # Modelos: Médico, Paciente, Consulta, Especialidade
│ ├── views.py # Lógica de listagem e criação de consultas
│ ├── urls.py
│ ├── forms.py
│ └── templates/agenda/
│ ├── agenda_list.html
│ └── consulta_form.html
└── static/
├── css, js, images
├── .gitignore
├── LICENSE
└── README.md

```

---

## Modelagem de Dados (Resumo)

**Entidades principais:**
- `Medico` → vinculado a um usuário (`User`)
- `Paciente` → dados pessoais + histórico médico (`JSONField`)
- `Especialidade` → lista de áreas médicas
- `Consulta` → relaciona médico + paciente + data + horário + status

**Regras importantes:**
- Um médico não pode ter duas consultas no mesmo horário (`unique_together`)
- Consultas só podem ser criadas dentro do horário de atendimento do médico

---

## Como Rodar o Projeto

### Instalação manual (sem Docker)

```bash
    # 1. Clone o repositório
    git clone https://github.com/MariaNatalia2003/medora.git
    cd medora

    # 2. Crie e ative o ambiente virtual
    python -m venv venv
    source venv/bin/activate   # (Linux/macOS)
    venv\Scripts\activate      # (Windows)

    # 3. Instale as dependências
    pip install -r requirements.txt

    # 4. Configure o banco de dados no settings.py
    # (ou use o PostgreSQL local com user/password padrão)

    # 5. Execute as migrações
    python manage.py migrate

    # 6. Crie um superusuário
    python manage.py createsuperuser

    # 7. Rode o servidor
    python manage.py runserver
```

## Contribuição

Quer contribuir? Fique à vontade!

1. Faça um fork do projeto
2. Crie uma branch com sua feature:
```bash
    git checkout -b feature/nome-da-feature
```

3. Faça o commit e push:
```bash
git push origin feature/nome-da-feature
```

4. Abra um Pull Request.

## Autor

O **Medora** é um sistema de agendamento médico desenvolvido como um projeto de 
demonstração, com o intuito principal de evoluir minhas habilidades técnicas 
com **Django**, **Python** e **Desenvolvimento Web**.

- **Contato**: [Conecte-se comigo no LinkedIn](https://www.linkedin.com/in/maria-natalia-cardim/)

## Licença

Este projeto é distribuído sob a licença MIT
Consulte o arquivo [LICENSE](LICENSE) para mais informações.
