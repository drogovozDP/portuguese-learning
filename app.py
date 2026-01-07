import random
import re
import unicodedata
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT_DIR = Path(__file__).parent
DICT_DIR = ROOT_DIR / "dicts"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def normalize(s: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize("NFD", s.lower().strip())
        if unicodedata.category(c) != "Mn"
    )


def collect_word_pairs(dict_name: str):
    regex_pattern = re.compile(r'#[^\n]*', re.MULTILINE)
    with open(DICT_DIR / dict_name, encoding="utf-8") as f:
        lines = [
            w.strip()
            for w in regex_pattern.sub('', f.read()).splitlines()
            if w.strip() and w != "---"
        ]

    def gen_sentences(parts):
        if not parts:
            return [""]
        result = []
        for w in parts[0]:
            for tail in gen_sentences(parts[1:]):
                result.append(f"{w} {tail}".strip())
        return result

    pairs = []
    for line in lines:
        pt, ru = line.split("|")
        pt_var = [w.split("/") for w in pt.strip().split()]
        ru_var = [w.split("/") for w in ru.strip().split()]
        pairs.append({
            "pt": gen_sentences(pt_var),
            "ru": gen_sentences(ru_var),
        })
    return pairs


@app.get("/", response_class=HTMLResponse)
def index():
    return (ROOT_DIR / "static/index.html").read_text(encoding="utf-8")


@app.get("/api/dicts")
def list_dicts():
    return sorted(p.name for p in DICT_DIR.glob("*.txt"))


@app.post("/api/session/start")
def start_session(dict_name: str):
    pairs = collect_word_pairs(dict_name)
    random.shuffle(pairs)
    return {
        "pairs": pairs,
        "total": len(pairs),
    }


class AnswerPayload(BaseModel):
    answer: str
    pt: list[str]
    ru: str


@app.post("/api/check")
def check_answer(payload: AnswerPayload):
    user = normalize(payload.answer)
    correct = any(normalize(p) == user for p in payload.pt)
    return {
        "correct": correct,
        "ru": payload.ru,
        "pt": payload.pt,
    }
