-- ============================================
-- Tabela de produtos
-- ============================================
CREATE TABLE IF NOT EXISTS produtos (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    preco       NUMERIC(10,2) NOT NULL,
    categoria   VARCHAR(50) NOT NULL
);

-- ============================================
-- Tabela de clientes
-- ============================================
CREATE TABLE IF NOT EXISTS clientes (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    cidade      VARCHAR(80),
    criado_em   TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- Tabela de pedidos
-- ============================================
CREATE TABLE IF NOT EXISTS pedidos (
    id            SERIAL PRIMARY KEY,
    cliente_id    INT REFERENCES clientes(id),
    status        VARCHAR(20) DEFAULT 'pendente',
    valor_total   NUMERIC(10,2),
    criado_em     TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- Tabela de itens de cada pedido
-- ============================================
CREATE TABLE IF NOT EXISTS itens_pedido (
    id            SERIAL PRIMARY KEY,
    pedido_id     INT REFERENCES pedidos(id),
    produto_id    INT REFERENCES produtos(id),
    quantidade    INT NOT NULL,
    valor         NUMERIC(10,2) NOT NULL
);

-- ============================================
-- Dados: Produtos
-- ============================================
INSERT INTO produtos (nome, preco, categoria) VALUES
('Plano Starter',       300.00, 'assinatura'),
('Plano Pro Anual',     700.00, 'assinatura'),
('Plano Enterprise',   2000.00, 'assinatura'),
('Add-on Relatórios',   450.00, 'addon'),
('Suporte Premium',     200.00, 'servico');

-- ============================================
-- Dados: Clientes
-- ============================================
INSERT INTO clientes (nome, email, cidade, criado_em) VALUES
('Empresa Alpha',   'alpha@email.com',   'São Paulo',       NOW() - INTERVAL '90 days'),
('Empresa Beta',    'beta@email.com',    'Rio de Janeiro',  NOW() - INTERVAL '80 days'),
('Empresa Gamma',   'gamma@email.com',   'Belo Horizonte',  NOW() - INTERVAL '70 days'),
('Empresa Delta',   'delta@email.com',   'Curitiba',        NOW() - INTERVAL '60 days'),
('Empresa Epsilon', 'epsilon@email.com', 'Porto Alegre',    NOW() - INTERVAL '50 days'),
('Empresa Zeta',    'zeta@email.com',    'Brasília',        NOW() - INTERVAL '40 days'),
('Empresa Eta',     'eta@email.com',     'Fortaleza',       NOW() - INTERVAL '30 days'),
('Empresa Theta',   'theta@email.com',   'Recife',          NOW() - INTERVAL '20 days'),
('Empresa Iota',    'iota@email.com',    'Salvador',        NOW() - INTERVAL '10 days'),
('Empresa Kappa',   'kappa@email.com',   'Manaus',          NOW() - INTERVAL '5 days');

-- ============================================
-- Dados: Pedidos
-- ============================================
INSERT INTO pedidos (cliente_id, status, valor_total, criado_em) VALUES
(1,  'concluido', 1150.00, NOW() - INTERVAL '85 days'),
(2,  'concluido',  700.00, NOW() - INTERVAL '75 days'),
(3,  'concluido',  300.00, NOW() - INTERVAL '65 days'),
(4,  'concluido', 2000.00, NOW() - INTERVAL '55 days'),
(5,  'concluido',  950.00, NOW() - INTERVAL '45 days'),
(6,  'concluido',  700.00, NOW() - INTERVAL '35 days'),
(7,  'concluido',  450.00, NOW() - INTERVAL '25 days'),
(8,  'concluido', 2200.00, NOW() - INTERVAL '15 days'),
(9,  'concluido',  300.00, NOW() - INTERVAL '8 days'),
(10, 'pendente',   700.00, NOW() - INTERVAL '2 days');

-- ============================================
-- Dados: Itens dos pedidos
-- ============================================
INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, valor) VALUES
(1,  2, 1, 700.00),
(1,  4, 1, 450.00),
(2,  2, 1, 700.00),
(3,  1, 1, 300.00),
(4,  3, 1, 2000.00),
(5,  2, 1, 700.00),
(5,  5, 1, 200.00),
(5,  4, 1,  50.00),
(6,  2, 1, 700.00),
(7,  4, 1, 450.00),
(8,  3, 1, 2000.00),
(8,  4, 1, 200.00),
(9,  1, 1, 300.00),
(10, 2, 1, 700.00);
