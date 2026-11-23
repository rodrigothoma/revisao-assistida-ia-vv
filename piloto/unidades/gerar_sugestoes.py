"""
Gera as sugestões do modelo para uma unidade de revisão, usando o gpt-oss-120b pela API do Groq.

O piloto 1 (Defects4J) usou o Gemini 3.8 Flash; a versão anterior deste script está no histórico do git.
Não precisa de pacotes extras: usa só a biblioteca padrão do Python.

Uso:
    export GROQ_API_KEY="sua-chave"
    python3 gerar_sugestoes.py ../C1_numerado.txt --execucoes 5 --prompt ../../prompt_sistema.txt --saida restrito
    python3 gerar_sugestoes.py ../C1_numerado.txt --execucoes 3 --inicio 3 ...   # completa as execuções 3 a 5

Para cada execução, salva em <saida>/<unidade>_exec<N>.json a resposta completa da API
(data, modelo devolvido, uso de tokens e o raciocínio do modelo) e em <saida>/<unidade>_exec<N>.txt
apenas o texto final, que é o que pode ir para o revisor.

Temperatura e demais parâmetros de amostragem ficam no padrão (não são enviados).
O esforço de raciocínio é fixado em "medium" (o plano gratuito do Groq limita a 8.000 tokens por minuto,
e com "high" o raciocínio esgota o limite e a resposta volta vazia).
Respostas cortadas por limite de tokens (finish_reason diferente de "stop") são guardadas à parte
(<unidade>_exec<N>_cortada<k>.json) e a execução é repetida.
"""
import argparse
import datetime
import json
import os
import pathlib
import time
import urllib.error
import urllib.request

URL = "https://api.groq.com/openai/v1/chat/completions"
MODELO = "openai/gpt-oss-120b"
RACIOCINIO = "medium"
MAX_TOKENS = 6800  # prompt (~1.100) + resposta cabem no limite de 8.000 tokens por minuto


def chamar(corpo, chave, tentativas=10):
    """Faz a requisição, esperando e repetindo quando a API limita a taxa ou está indisponível."""
    dados = json.dumps(corpo).encode()
    for t in range(1, tentativas + 1):
        req = urllib.request.Request(URL, data=dados, headers={
            "Authorization": "Bearer " + chave,
            "Content-Type": "application/json",
            "User-Agent": "experimento-vv",
        })
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            texto = e.read().decode(errors="replace")
            espera = int(e.headers.get("retry-after") or 30) + 2
            if e.code not in (413, 429, 500, 502, 503) or t == tentativas:
                raise SystemExit(f"Erro {e.code}: {texto}")
            if "tokens per day" in texto and espera > 300:
                raise SystemExit("Cota diária de tokens esgotada. Tente mais tarde ou use outra chave.\n" + texto)
            print(f"  API respondeu {e.code}; nova tentativa {t + 1}/{tentativas} em {espera}s", flush=True)
            time.sleep(espera)
        except (urllib.error.URLError, TimeoutError) as e:
            if t == tentativas:
                raise
            print(f"  falha de conexão ({e}); nova tentativa em 30s", flush=True)
            time.sleep(30)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unidade", help="arquivo numerado da unidade")
    ap.add_argument("--execucoes", type=int, default=5)
    ap.add_argument("--inicio", type=int, default=1,
                    help="número da primeira execução (para completar um lote interrompido)")
    ap.add_argument("--prompt", default="prompt_sistema.txt")
    ap.add_argument("--saida", default="saidas", help="pasta onde salvar as respostas")
    ap.add_argument("--modelo", default=MODELO)
    ap.add_argument("--raciocinio", default=RACIOCINIO, choices=["low", "medium", "high"])
    args = ap.parse_args()

    chave = os.environ.get("GROQ_API_KEY")
    if not chave:
        raise SystemExit("Defina GROQ_API_KEY no ambiente.")
    prompt = pathlib.Path(args.prompt)
    sistema = prompt.read_text(encoding="utf-8")
    unidade = pathlib.Path(args.unidade)
    conteudo = unidade.read_text(encoding="utf-8")
    pasta = pathlib.Path(args.saida)
    pasta.mkdir(parents=True, exist_ok=True)

    corpo = {
        "model": args.modelo,
        "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": conteudo}],
        "reasoning_effort": args.raciocinio,
        "max_completion_tokens": MAX_TOKENS,
    }

    for n in range(args.inicio, args.inicio + args.execucoes):
        base = pasta / f"{unidade.stem}_exec{n}"
        for k in range(1, 4):
            inicio = datetime.datetime.now().isoformat(timespec="seconds")
            resposta = chamar(corpo, chave)
            escolha = resposta["choices"][0]
            mensagem = escolha["message"]
            registro = {
                "unidade": unidade.name,
                "execucao": n,
                "data_hora": inicio,
                "prompt": prompt.name,
                "modelo_solicitado": args.modelo,
                "modelo_devolvido": resposta.get("model"),
                "system_fingerprint": resposta.get("system_fingerprint"),
                "raciocinio": args.raciocinio,
                "motivo_fim": escolha.get("finish_reason"),
                "uso": resposta.get("usage"),
                "raciocinio_modelo": mensagem.get("reasoning"),
                "resposta_completa": resposta,
            }
            if escolha.get("finish_reason") == "stop" and (mensagem.get("content") or "").strip():
                break
            cortada = pasta / f"{unidade.stem}_exec{n}_cortada{k}.json"
            cortada.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  execução {n} cortada ({escolha.get('finish_reason')}); repetindo", flush=True)
        else:
            raise SystemExit(f"Execução {n} cortada 3 vezes; aumente MAX_TOKENS ou use raciocínio 'low'.")

        base.with_suffix(".json").write_text(
            json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
        base.with_suffix(".txt").write_text(mensagem["content"].strip() + "\n", encoding="utf-8")
        uso = resposta.get("usage") or {}
        print(f"[{inicio}] {unidade.stem} execução {n}: {resposta.get('model')} | "
              f"{uso.get('total_tokens')} tokens | {uso.get('total_time', 0):.1f}s", flush=True)


if __name__ == "__main__":
    main()
