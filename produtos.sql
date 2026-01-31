CREATE TABLE Produtos (
    ProdutoID INT PRIMARY KEY,
    NomeProduto VARCHAR(100),
    Quantidade INT,
    Preco DECIMAL(10,2)
);

INSERT INTO Produtos (ProdutoID, NomeProduto, Quantidade, Preco) VALUES
(1, 'Camisa', 50, 79.90),
(2, 'Calça', 30, 149.90),
(3, 'Tênis', 20, 299.90);
