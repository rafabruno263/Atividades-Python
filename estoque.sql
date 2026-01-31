CREATE TABLE Estoque (
    EstoqueID INT AUTO_INCREMENT PRIMARY KEY,
    ProdutoID INT,
    FornecedorID INT,
    Quantidade INT,
    DataEntrada DATE,

    FOREIGN KEY (ProdutoID) REFERENCES Produtos(ProdutoID),
    FOREIGN KEY (FornecedorID) REFERENCES Fornecedores(FornecedorID)
);
