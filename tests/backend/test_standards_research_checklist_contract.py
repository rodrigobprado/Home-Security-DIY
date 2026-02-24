from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STANDARDS = ROOT / "standards" / "STANDARDS_TO_RESEARCH.md"


def test_standards_items_466_to_491_are_marked_complete():
    content = STANDARDS.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Certificação ISO 27001 registrada como não obrigatória para residência e recomendada como referência.",
        "- [x] Status da pesquisa ISO 27001 consolidado (2026-02-22, Agente_Pesquisador_Normas).",
        "- [x] Escopo NBR 9050 documentado para acessibilidade de interfaces.",
        "- [x] Relevância para dashboard e interfaces físicas registrada.",
        "- [x] Requisitos aplicáveis à interface digital mapeados:",
        "- [x] Contraste mínimo de texto definido na baseline de UI",
        "- [x] Tamanho mínimo de fonte definido para leitura operacional",
        "- [x] Alvos de toque/clique mínimos considerados para uso mobile",
        "- [x] Navegação por teclado prevista com foco visível",
        "- [x] Texto alternativo (`aria-label`) previsto para ícones e imagens críticos",
        "- [x] Referência complementar WCAG 2.1 Nível AA registrada.",
        "- [x] Obrigatoriedade da NBR 9050 registrada (voluntária para residencial privado, recomendada).",
        "- [x] Status da pesquisa NBR 9050 consolidado (2026-02-22, Agente_Pesquisador_Normas).",
    ]

    for item in expected_items:
        assert item in content
