import re
from typing import Dict

class SimpleLemmatizer:
    def __init__(self):
        self.irregular_verbs: Dict[str,str] = {
            "was": "be", "were": "be", "am": "be", "is": "be", "are": "be",
            "been": "be", "being": "be",
            "had": "have", "has": "have",
            "did": "do",  "done": "do",  "doing": "do",
            "went": "go", "gone": "go", "doing":"do",
            "saw": "see", "seen":"see",
            "ate": "eat", "eaten":"eat",
        }
        self.irregular_nouns: Dict[str,str] = {
            "mice": "mouse", "geese": "goose", "feet": "foot",
            "teeth":"tooth", "children":"child", "men":"man", "women":"woman",
        }

    def lemmatize(self, word: str, pos: str = "n") -> str:
        """
        pos: 'n' for noun, 'v' for verb, 'a' for adjective (only minimal handling).
        """
        w = word.lower()
        if pos.startswith("v") and w in self.irregular_verbs:
            return self.irregular_verbs[w]
        if pos.startswith("n") and w in self.irregular_nouns:
            return self.irregular_nouns[w]


        if pos.startswith("n"):
            if w.endswith("ies") and len(w) > 4:
                return w[:-3] + "y"
            if w.endswith("ves") and len(w) > 4:
                stem = w[:-3]
                return stem + ("f" if stem[-1] not in "aeiou" else "fe")
            if w.endswith("ses") or w.endswith("xes") or w.endswith("zes"):
                return w[:-2]
            if w.endswith("s") and len(w) > 1 and not w.endswith("ss"):
                return w[:-1]
            return w
        
        if pos.startswith("v"):
            if w.endswith("ied") and len(w) > 4:
                return w[:-3] + "y"
            if w.endswith("ing") and len(w) > 5:
                stem = w[:-3]
                if stem.endswith(stem[-1]*2):
                    stem = stem[:-1]
                return stem + ("e" if not stem.endswith("e") else "")
            if w.endswith("ed") and len(w) > 3:
                stem = w[:-2]
                if stem.endswith(stem[-1]*2):
                    stem = stem[:-1]
                return stem + ("e" if not stem.endswith("e") else "")
            if w.endswith("s") and len(w) > 1 and not w.endswith("ss"):
                return w[:-1]
            return w
        

        if pos.startswith("a"):
            if w.endswith("er") and len(w) > 4:
                return w[:-2]
            if w.endswith("est") and len(w) > 5:
                return w[:-3]
            return w

        return w


if __name__ == "__main__":
    lem = SimpleLemmatizer()
    tests = [
        ("wolves","n"), ("children","n"), ("buses","n"), ("dogs","n"),
        ("mice","n"),   ("geese","n"),    ("cars","n"),   ("batches","n"),
        ("running","v"),("ran","v"),     ("hated","v"),  ("making","v"),
        ("studies","v"),("studied","v"), ("studies","n"),
        ("quicker","a"),("biggest","a"), ("happy","a"),
    ]
    for w,pos in tests:
        print(f"{w}/{pos} → {lem.lemmatize(w,pos)}")
