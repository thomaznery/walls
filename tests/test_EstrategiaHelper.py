from market.ClockHelper import CHelper
import pytest
import re



def test_hora_formato():
    eh = CHelper()
    horario_format = re.compile(r'[0-9]{2}')
    assert horario_format.match(eh.hora())

def test_minuto_formato():
    eh = CHelper()
    horario_format = re.compile(r'[0-9]{2}')
    assert horario_format.match(eh.min())