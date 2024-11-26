from parsimonious.grammar import Grammar

from pathlib import Path
orca_content = Path('orca.inp').open().read()
grammar_orca = Grammar(
    r"""
    file = (keyword_line / section / coord_line / newline)*
    keyword_line = "!" ~"[^\n]*" newline
    section = section_start section_body "end" newline
    section_start = "%" ~"[A-Za-z0-9_]+" newline
    section_body = (non_end_line newline)+
    non_end_line = ~"(?!end)[^\n]+"
    coord_line = "*" ~"[^\n]*" newline
    newline = ~"\n+"
    """
)
tree = grammar_orca.parse(orca_content)
