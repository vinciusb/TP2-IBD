-- Recuperar o nome e CPF dos funcionários com salário maior que 5000.
SELECT NOME, CPF_FUNC
FROM FUNCIONARIO
WHERE SALARIO > 5000 AND NOME = 'A DEFINIR';

SELECT NOME, CPF_FUNC
FROM (
    SELECT *
    FROM FUNCIONARIO
    WHERE NOME = 'A DEFINIR'
)
WHERE SALARIO > 5000;

-- Recuperar o código e nome dos produtos da marca A que estão fora do estoque.
SELECT COD_PROD, NOME_PROD
FROM PRODUTO
WHERE MARCA = 'AA' AND QUANTIDADE = 0;