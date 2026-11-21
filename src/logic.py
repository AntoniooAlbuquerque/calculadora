import ast
import operator

OPERADORES_PERMITIDOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _avaliar_no(no):
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES_PERMITIDOS:
        esquerda = _avaliar_no(no.left)
        direita = _avaliar_no(no.right)
        return OPERADORES_PERMITIDOS[type(no.op)](esquerda, direita)
    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES_PERMITIDOS:
        return OPERADORES_PERMITIDOS[type(no.op)](_avaliar_no(no.operand))
    raise ValueError("Expressao invalida")


def calcular_expressao(expressao: str) -> str:
    """Avalia uma expressao matematica basica com seguranca e trata erros."""
    if not expressao.strip():
        return ""
    try:
        arvore = ast.parse(expressao, mode="eval")
        resultado = _avaliar_no(arvore.body)
        if isinstance(resultado, float) and resultado.is_integer():
            return str(int(resultado))
        return str(round(resultado, 10))
    except ZeroDivisionError:
        return "Erro: Divisao por 0"
    except Exception:
        return "Erro"
