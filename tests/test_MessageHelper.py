import pytest
from saida.MessageHelper import MHelper


def test_extract_ticket_sem_tickets():
    assert MHelper().extract_tickets("Um teste de mensagem enviada\
        pelo usuario solicitando acoes como") == []

def test_extract_ticket_com_tickets():
    assert MHelper().extract_tickets("Um teste de mensagem enviada\
        pelo usuario solicitando vale3 , bidi4 acoes como") == ['VALE3', 'BIDI4']

def test_extract_ticket_sem_parametros():
    assert MHelper().extract_tickets(None) == []