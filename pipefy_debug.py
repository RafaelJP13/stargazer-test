#!/usr/bin/env python3
"""
pipefy_debug.py — Debug interativo das mutations GraphQL do Pipefy

Uso:
    python pipefy_debug.py
    python pipefy_debug.py --mode create
    python pipefy_debug.py --mode update
    python pipefy_debug.py --json          # output puro JSON (CI-friendly)
"""

import argparse
import json
import sys
import textwrap
from decimal import Decimal

# ── cores ANSI ────────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
BLUE   = "\033[34m"
MAGENTA= "\033[35m"
RED    = "\033[31m"
WHITE  = "\033[97m"
BG_DARK= "\033[48;5;235m"

def c(color, text):
    return f"{color}{text}{RESET}"

def supports_color():
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

# ── funções copiadas de app/integrations/pipefy.py ───────────────────────────

def build_create_card_mutation(customer: dict) -> str:
    return """mutation CreateCard($input: CreateCardInput!) {
    createCard(input: $input) {
        card {
            id
            title
            current_phase {
                name
            }
        }
    }
}"""

def build_create_card_variables(customer: dict) -> dict:
    return {
        "input": {
            "pipe_id": "PIPE_ID_AQUI",
            "fields_attributes": [
                {"field_id": "cliente_nome",     "field_value": customer["cliente_nome"]},
                {"field_id": "cliente_email",    "field_value": customer["cliente_email"]},
                {"field_id": "valor_patrimonio", "field_value": str(customer["valor_patrimonio"])},
                {"field_id": "tipo_solicitacao", "field_value": customer["tipo_solicitacao"]},
            ]
        }
    }

def build_update_card_field_mutation() -> str:
    return """mutation UpdateCardField($input: UpdateCardFieldInput!) {
    updateCardField(input: $input) {
        success
    }
}"""

def build_update_card_field_variables(card_id: str, prioridade: str, status: str) -> list:
    return [
        {"input": {"card_id": card_id, "field_id": "status",    "new_value": status}},
        {"input": {"card_id": card_id, "field_id": "prioridade", "new_value": prioridade}},
    ]

# ── helpers de prioridade ─────────────────────────────────────────────────────

PATRIMONIO_MINIMO_PRIORIDADE_ALTA = Decimal("200000.00")

def calcular_prioridade(valor_patrimonio) -> str:
    v = Decimal(str(valor_patrimonio))
    return "prioridade_alta" if v >= PATRIMONIO_MINIMO_PRIORIDADE_ALTA else "prioridade_normal"

# ── UI helpers ────────────────────────────────────────────────────────────────

def hr(char="─", width=64):
    print(c(DIM, char * width))

def header(title: str):
    print()
    hr("═")
    print(c(BOLD + CYAN, f"  {title}"))
    hr("═")
    print()

def section(title: str):
    print()
    print(c(BOLD + YELLOW, f"▶ {title}"))
    hr()

def print_graphql(query: str):
    """Syntax-highlights uma string GraphQL no terminal."""
    keywords  = {"mutation", "query", "fragment", "on"}
    types     = {"CreateCardInput", "UpdateCardFieldInput", "CreateCard", "UpdateCardField"}

    lines = query.strip().splitlines()
    for line in lines:
        stripped = line.strip()
        # keyword de abertura
        for kw in keywords:
            if stripped.startswith(kw):
                line = line.replace(kw, c(MAGENTA, kw), 1)
                break
        # nomes de tipo entre parênteses
        for tp in types:
            if tp in line:
                line = line.replace(tp, c(CYAN, tp))
        # campos (palavras sem : no início de linha com chaves)
        # abertura/fechamento de bloco
        line = line.replace("{", c(DIM, "{")).replace("}", c(DIM, "}"))
        # variáveis $
        if "$" in line:
            parts = line.split("$")
            rebuilt = parts[0]
            for p in parts[1:]:
                word_end = next((i for i, ch in enumerate(p) if not (ch.isalnum() or ch == "_")), len(p))
                rebuilt += c(GREEN, "$" + p[:word_end]) + p[word_end:]
            line = rebuilt
        # campos antes de (
        if "!" in line:
            line = line.replace("!", c(RED, "!"))
        print("    " + line)

def print_json_block(data, title: str = "variables"):
    print(c(DIM, f"  // {title}"))
    raw = json.dumps(data, indent=2, ensure_ascii=False)
    for line in raw.splitlines():
        # chaves
        if '": ' in line or '":' in line:
            key_end = line.index('"', line.index('"') + 1) + 1
            print("    " + c(BLUE, line[:key_end]) + line[key_end:])
        # strings valor
        elif line.strip().startswith('"'):
            print("    " + c(GREEN, line))
        else:
            print("    " + line)

def badge(label: str, value: str, color=GREEN):
    print(f"  {c(DIM, label+':')} {c(color + BOLD, value)}")

def ask(prompt: str, default: str = "") -> str:
    hint = f" [{c(DIM, default)}]" if default else ""
    try:
        val = input(f"  {c(CYAN, '›')} {prompt}{hint}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)
    return val if val else default

def ask_decimal(prompt: str, default: str = "250000") -> Decimal:
    while True:
        raw = ask(prompt, default)
        try:
            return Decimal(raw.replace(",", ".").replace("_", ""))
        except Exception:
            print(c(RED, "  Valor inválido. Use números, ex: 250000 ou 199999.99"))

# ── fluxo 1: createCard ───────────────────────────────────────────────────────

def flow_create(json_only=False):
    if not json_only:
        header("FLUXO 1 — createCard  (POST /clientes)")
        print(c(DIM, "  Preencha os dados do cliente para ver a mutation gerada.\n"))

        nome      = ask("cliente_nome",     "João Silva")
        email     = ask("cliente_email",    "joao.silva@example.com")
        solicit   = ask("tipo_solicitacao", "Atualização cadastral")
        patrimonio = ask_decimal("valor_patrimonio", "250000")
    else:
        nome, email, solicit, patrimonio = "João Silva", "joao.silva@example.com", "Atualização cadastral", Decimal("250000")

    customer = {
        "id":               1,
        "cliente_nome":     nome,
        "cliente_email":    email,
        "tipo_solicitacao": solicit,
        "valor_patrimonio": patrimonio,
        "status":           "Aguardando Análise",
    }

    mutation  = build_create_card_mutation(customer)
    variables = build_create_card_variables(customer)
    prioridade = calcular_prioridade(patrimonio)

    if json_only:
        print(json.dumps({"mutation": mutation, "variables": variables}, indent=2, ensure_ascii=False))
        return

    section("GraphQL Mutation")
    print_graphql(mutation)

    section("Variables (payload enviado ao Pipefy)")
    print_json_block(variables, "createCard variables")

    section("Estado salvo no banco local")
    badge("status",    customer["status"],      YELLOW)
    badge("prioridade", "(calculada no webhook — ainda None)", DIM)

    section("Requisição HTTP para o Pipefy")

    print(c(DIM, "  POST https://api.pipefy.com/graphql"))
    print(c(DIM, "  Authorization: Bearer <PIPEFY_TOKEN>"))
    print(c(DIM, "  Content-Type: application/json"))

    section("Query enviada ao Pipefy")
    print_graphql(mutation)

    section("Variables enviadas")
    print_json_block(variables, "variables")

# ── fluxo 2: updateCardField ──────────────────────────────────────────────────

def flow_update(json_only=False):
    if not json_only:
        header("FLUXO 2 — updateCardField  (POST /webhooks/pipefy/card-updated)")
        print(c(DIM, "  Simula o webhook recebido após o operacional mover o card."))
        print(c(DIM, "  (valor_patrimonio vem do banco — escolha a prioridade resultante)\n"))

        email    = ask("cliente_email", "joao.silva@example.com")
        card_id  = ask("card_id",       "card_456")
        event_id = ask("event_id",      "evt_123")

        print(f"\n  {c(DIM, 'prioridade resultante:')}")
        print(f"  {c(CYAN + BOLD, '[1]')}  prioridade_alta   (patrimônio ≥ R$ 200.000)")
        print(f"  {c(CYAN + BOLD, '[2]')}  prioridade_normal (patrimônio < R$ 200.000)")
        escolha  = ask("opção", "1")
        prioridade = "prioridade_normal" if escolha == "2" else "prioridade_alta"
    else:
        email, card_id, event_id, prioridade = "joao.silva@example.com", "card_456", "evt_123", "prioridade_alta"

    status = "Processado"

    mutation  = build_update_card_field_mutation()
    variables = build_update_card_field_variables(card_id, prioridade, status)

    if json_only:
        print(json.dumps({"mutation": mutation, "variables": variables}, indent=2, ensure_ascii=False))
        return

    section("Regra de Negócio")
    color_prio = GREEN if prioridade == "prioridade_alta" else YELLOW
    badge("prioridade calculada", prioridade, color_prio)
    badge("status",               status,     GREEN)

    section("Idempotência")
    print(f"  {c(DIM, 'event_id recebido →')} {c(WHITE, event_id)}")
    print(f"  {c(DIM, 'já existe na tabela events? →')} {c(RED, 'NÃO')} {c(DIM, '(evento novo, segue processamento)')}")

    section("GraphQL Mutation")
    print_graphql(mutation)

    section("Variables — chamada 1 de 2  (status)")
    print_json_block(variables[0], "updateCardField: status → Processado")

    section("Variables — chamada 2 de 2  (prioridade)")
    print_json_block(variables[1], f"updateCardField: prioridade → {prioridade}")

    section("Estado final no banco local")
    badge("status",    status,    GREEN)
    badge("prioridade", prioridade, color_prio)

    print()
    print(c(GREEN + BOLD, "  ✔ Mutation updateCardField montada com sucesso."))
    print()

# ── menu interativo ───────────────────────────────────────────────────────────

def menu():
    while True:
        header("Pipefy Mutation Debugger")
        print(c(WHITE,  "  Escolha o fluxo para inspecionar:\n"))
        print(f"  {c(CYAN + BOLD, '[1]')}  createCard       — POST /clientes")
        print(f"  {c(CYAN + BOLD, '[2]')}  updateCardField  — POST /webhooks/pipefy/card-updated")
        print(f"  {c(DIM,  '[q]')}  sair")
        print()

        choice = ask("opção", "1")

        if choice == "1":
            flow_create()
        elif choice == "2":
            flow_update()
        elif choice.lower() in ("q", "quit", "exit", "0"):
            print(c(DIM, "\n  tchau!\n"))
            sys.exit(0)
        else:
            print(c(RED, "\n  Opção inválida. Digite 1, 2 ou q.\n"))

# ── entrypoint ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Debug interativo das mutations GraphQL do Pipefy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            exemplos:
              python pipefy_debug.py                  # menu interativo
              python pipefy_debug.py --mode create    # só fluxo 1
              python pipefy_debug.py --mode update    # só fluxo 2
              python pipefy_debug.py --json           # output JSON puro (CI)
        """)
    )
    parser.add_argument(
        "--mode",
        choices=["create", "update"],
        help="executa diretamente um fluxo sem menu"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="imprime o payload GraphQL em JSON puro e sai (não interativo)"
    )
    args = parser.parse_args()

    if args.json:
        if args.mode == "update":
            flow_update(json_only=True)
        else:
            flow_create(json_only=True)
        return

    if args.mode == "create":
        flow_create()
    elif args.mode == "update":
        flow_update()
    else:
        menu()

if __name__ == "__main__":
    main()