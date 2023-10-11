import re

def validar_rg(numero_rg):
    # Remover possíveis pontos e traços do RG
    numero_rg = re.sub(r'[.-]', '', numero_rg)

    # Verificar se o RG tem o formato correto (duas letras seguidas de números e um dígito verificador)
    if not re.match(r'^[A-Z]{2}\d{6}(\d|[A-Z])?$', numero_rg):
        return False

    # Verificar o dígito verificador (se houver)
    if len(numero_rg) == 9:
        digito_verificador_calculado = calcular_digito_verificador(numero_rg[:-1])
        digito_verificador_fornecido = numero_rg[-1]

        if digito_verificador_calculado != digito_verificador_fornecido:
            return False

    return True

def calcular_digito_verificador(numero_rg):
    soma = 0
    multiplicador = 2

    for caractere in numero_rg[::-1]:
        if caractere.isdigit():
            soma += int(caractere) * multiplicador
        else:
            # Atribuir valores numéricos para as letras A=10, B=11, C=12, ... , Z=35
            valor_letra = ord(caractere) - 55
            soma += valor_letra * multiplicador

        multiplicador += 1

    resto = soma % 11
    if resto == 0:
        return '0'
    elif resto == 1:
        return 'X'
    else:
        return str(11 - resto)

# Exemplo de uso:
numero_rg = "32150711-3"
if validar_rg(numero_rg):
    print("RG válido.")
else:
    print("RG inválido.")
