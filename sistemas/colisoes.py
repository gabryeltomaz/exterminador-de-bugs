
def colisao_circular(x1, y1, r1, x2, y2, r2):

    dx = x2 - x1
    dy = y2 - y1

    distancia_quadrada = dx * dx + dy * dy

    soma_raios = r1 + r2

    if distancia_quadrada <= soma_raios * soma_raios:
        return True

    return False
