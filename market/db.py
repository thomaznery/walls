
import psycopg2
from .helper.AcumuladorHelper import preco_to_float
from .helper.ClockHelper import dia

HOST = '127.0.0.1'
DATABASE = 'wss'
USER = 'postgres'
PASSWORD = 'loira'
conn_string = "host={0} user={1} dbname={2} password={3}".format(HOST, USER, DATABASE, PASSWORD)


class Conexao(object):
    _db = None

    def __init__(self) -> None:
        self.con = psycopg2.connect(conn_string)

    def incluir_negocio(self, neg, ativo):
        cursor = self.con.cursor()
        tabela = ativo[0:3]
        try:
            agressor = neg['agressor'][0]
            hora = f"{dia('%Y/%m/%d ') }{neg['hora']}"
            sql = f"insert into marketdata_{tabela}_book (ativo,  hora, preco, quantidade, comprador, vendedor, agressor, numero)\
                values {ativo,  hora, preco_to_float(neg['preco'], ativo), int(neg['qntd']), int(neg['comprador']), int(neg['vendedor']), agressor, int(neg['numero'])}"
            cursor.execute(sql)
            self.con.commit()
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print(f"Erro ao executar query incluir_negocio_wdo \n{error}")

    def close(self):
        # closing database connection.
        if self.con:
            self.con.close()
            print("PostgreSQL connection is closed")
