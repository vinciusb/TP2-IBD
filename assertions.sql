-- Checa quantidade de produto da seção
CREATE OR REPLACE FUNCTION MUDA_PRODUTO() RETURNS TRIGGER AS $$
    DECLARE
        cod INTEGER;
        qnt INTEGER;
    BEGIN
        -- Quando for apagar
        IF NEW.COD_SECAO IS NULL THEN
            cod := OLD.COD_SECAO;
        -- Quando for dar update ou inserir
        ELSE
            cod := NEW.COD_SECAO;
        END IF;

        qnt := (SELECT SUM(QUANTIDADE) FROM PRODUTO WHERE COD_SECAO = cod);
        IF qnt IS NULL THEN
            qnt:= 0;
        END IF;

        UPDATE SECAO SET QUANTIDADE_PROD = qnt WHERE COD_SECAO = cod;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRIGGER_QNT_PRODUTOS
AFTER INSERT OR UPDATE OR DELETE ON PRODUTO
FOR EACH ROW
EXECUTE PROCEDURE MUDA_PRODUTO();

-- raise notice '%', qnt;

-- Assertion pra reduzir quantidade de produto numa venda
CREATE OR REPLACE FUNCTION QNT_VENDEU() RETURNS TRIGGER AS $$
    DECLARE
        qnt INTEGER;
    BEGIN
        qnt := (SELECT QUANTIDADE FROM PRODUTO WHERE COD_PROD = NEW.COD_PROD);

        IF qnt < NEW.QUANTIDADE_VENDIDA THEN
            raise exception 'Não é possivel fazer compras com mais produtos do que o numero registrado no estoque.';
        END IF;

        UPDATE PRODUTO 
        SET QUANTIDADE = qnt - NEW.QUANTIDADE_VENDIDA 
        WHERE COD_PROD = NEW.COD_PROD;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRIGGER_QNT_VENDEU
AFTER INSERT OR UPDATE ON VENDE
FOR EACH ROW
EXECUTE PROCEDURE QNT_VENDEU();



-- Asserção dos tipos dos funcionários
CREATE OR REPLACE FUNCTION UM_TIPO_POR_FUNC() RETURNS TRIGGER AS $$
    BEGIN
        IF (
            (NEW.TIPO_FUNC = 1 AND ((NEW.NUMERO_CAIXA IS NOT NULL) OR (NEW.COD_SECAO_AUXILIADA IS NOT NULL))) OR
            (NEW.TIPO_FUNC = 2 AND ((NEW.NUMERO_CAIXA IS NULL) OR (NEW.COD_SECAO_AUXILIADA IS NOT NULL))) OR
            (NEW.TIPO_FUNC = 3 AND ((NEW.NUMERO_CAIXA IS NOT NULL) OR (NEW.COD_SECAO_AUXILIADA IS NULL)))
        ) THEN
            raise exception 'Funcionário deve ter atributos do seu tipo e unicamente deste.';
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRIGGER_TIPO_FUNC
BEFORE INSERT OR UPDATE ON FUNCIONARIO
FOR EACH ROW
EXECUTE PROCEDURE UM_TIPO_POR_FUNC();



-- Garante que apenas organizadores podem organizar
CREATE OR REPLACE FUNCTION SO_ORGANIZADOR_ORGANIZA() RETURNS TRIGGER AS $$
    DECLARE
        tipo INTEGER;
    BEGIN
        tipo = (SELECT TIPO_FUNC FROM FUNCIONARIO WHERE CPF_FUNC = NEW.CPF_FUNC);

        IF tipo = 2 OR tipo = 3 THEN
            raise exception 'Apenas funcionários que são organizadores podem organizar.';
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRIGGER_SO_ORGANIZADOR_ORGANIZA
BEFORE INSERT OR UPDATE ON ORGANIZA
FOR EACH ROW
EXECUTE PROCEDURE SO_ORGANIZADOR_ORGANIZA();



-- Garante que apenas caixas possam vender
CREATE OR REPLACE FUNCTION SO_CAIXA_VENDE() RETURNS TRIGGER AS $$
    DECLARE
        tipo INTEGER;
    BEGIN
        tipo := (SELECT TIPO_FUNC FROM FUNCIONARIO WHERE CPF_FUNC = NEW.CPF_FUNC);

        IF tipo = 1 OR tipo = 3 THEN
            raise exception 'Apenas funcionários que são caixas podem vender.';
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRIGGER_SO_CAIXA_VENDE
BEFORE INSERT OR UPDATE ON VENDE
FOR EACH ROW
EXECUTE PROCEDURE SO_CAIXA_VENDE();