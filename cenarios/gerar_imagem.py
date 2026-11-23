"""
Gera, a partir de um arquivo .java, a imagem com linhas numeradas que vai no Forms
e o texto numerado que vai para o modelo.

Uso (Python do sistema, que já tem Pygments e Pillow):
    python3 cenarios/gerar_imagem.py cenarios/C1/V_bug/CalculadoraEstacionamento.java cenarios/C1/C1

Saídas:
    <prefixo>.png           imagem do código, linhas numeradas, fonte monoespaçada
    <prefixo>_numerado.txt  mesmo código com "  N | " no início de cada linha
"""
import pathlib
import sys

from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import JavaLexer


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    fonte = pathlib.Path(sys.argv[1])
    prefixo = pathlib.Path(sys.argv[2])
    codigo = fonte.read_text(encoding="utf-8")

    formatador = ImageFormatter(
        font_name="DejaVu Sans Mono",
        font_size=20,
        line_numbers=True,
        line_number_bg="#eeeeee",
        line_number_fg="#555555",
        line_number_pad=10,
        image_pad=16,
        style="default",
    )
    prefixo.with_suffix(".png").write_bytes(highlight(codigo, JavaLexer(), formatador))

    linhas = codigo.rstrip("\n").split("\n")
    largura = len(str(len(linhas)))
    numerado = "\n".join(f"{i:>{largura}} | {l}" for i, l in enumerate(linhas, 1))
    pathlib.Path(f"{prefixo}_numerado.txt").write_text(numerado + "\n", encoding="utf-8")
    print(f"{prefixo}.png e {prefixo}_numerado.txt ({len(linhas)} linhas)")


if __name__ == "__main__":
    main()
