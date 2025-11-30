
# Sistema de Impressões Acadêmicas

Projeto web feito em Django para gerenciar pedidos de impressão de professores, com painel administrativo, controle de tarefas e acompanhamento de todo o fluxo. Desenvolvido como trabalho de P.I. 2025.

## Objetivo
Organizar e facilitar o processo de solicitação, acompanhamento e entrega de impressões na escola, conectando professores, bolsistas e administradores em um só sistema.

## Funcionalidades principais
- Cadastro e login de usuários (professor e admin)
- Envio de pedidos de impressão com vários arquivos
- Campos extras: quantidade de documentos, folhas, frente/verso, grampear, tipo de impressão
- Painel do professor: lista, filtro, status, download dos arquivos
- Painel do admin: aprovar, rejeitar, excluir, ver detalhes e todos os campos do pedido
- Paginação, busca e filtros dinâmicos
- Mensagens de feedback para todas as ações
- Layout responsivo e visual limpo (Bootstrap)
- Templates organizados com herança e includes
- Permissões e autenticação integradas
- (Em desenvolvimento) Notificação por e-mail e relatórios detalhados

## Estrutura do Projeto
- `usuarios/`: app de usuários e autenticação
- `impressoes/`: app principal dos pedidos de impressão
- `config/`: configurações do Django
- `templates/`: HTMLs organizados por app

## Como rodar
1. Clone o repositório:
   ```bash
   git clone https://github.com/andreff01/projeto-impressoes.git
   cd projeto-impressoes
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rode as migrações:
   ```bash
   python manage.py migrate
   ```
5. (Opcional) Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```
6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
7. Acesse em [http://localhost:8000](http://localhost:8000)

## Observações
- O sistema já está pronto para uso local. Para produção, configure variáveis de ambiente e banco PostgreSQL.
- O layout foi pensado para ser simples, direto e fácil de usar na rotina escolar.
- O código está comentado e organizado para facilitar manutenção e futuras melhorias.

## Autores
André Ferreira Farias e Larisse Pessoa Reis

---
Projeto desenvolvido para a disciplina de Programação para Internet - 2025.
