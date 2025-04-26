#!/usr/bin/env python3

import re

class PorterStemmer:
    def __init__(self):
        # regex shortcuts
        self.vowel = re.compile(r"[aeiou]")
        self.m_gr0 = re.compile(r"^([^aeiou]+[aeiou]+)+[^aeiou]+$")
        self.m_eq1 = re.compile(r"^([^aeiou]+[aeiou]+)[^aeiou]+$")
        self.m_gt1 = re.compile(r"^([^aeiou]+[aeiou]+){2,}[^aeiou]+$")
        self.c_v_c = re.compile(r"[^aeiou][aeiou][^aeiou]$")

    def _measure(self, stem: str) -> int:
        return len(re.findall(r"(?:[^aeiou]+[aeiou]+)", stem))

    def _contains_vowel(self, stem: str) -> bool:
        return bool(self.vowel.search(stem))

    def _ends_with_double(self, word: str) -> bool:
        return len(word) >= 2 and word[-1] == word[-2] and word[-1] not in "aeiou"

    def _cvc(self, word: str) -> bool:
        return bool(self.c_v_c.search(word[-3:])) if len(word) >= 3 else False

    def _step1a(self, word: str) -> str:
        if word.endswith("sses"): return word[:-2]
        if word.endswith("ies"):  return word[:-2]
        if word.endswith("ss"):   return word
        if word.endswith("s"):    return word[:-1]
        return word

    def _step1b(self, word: str) -> str:
        if word.endswith("eed"):
            stem = word[:-3]
            if self._measure(stem) > 0:
                return stem + "ee"
            return word

        for suf in ("ed", "ing"):
            if word.endswith(suf):
                stem = word[:-len(suf)]
                if self._contains_vowel(stem):
                    word = stem
                    break
        else:
            return word

        if word.endswith(("at","bl","iz")):
            return word + "e"
        if self._ends_with_double(word):
            return word[:-1]
        if self._measure(word) == 1 and self._cvc(word):
            return word + "e"
        return word

    def _step1c(self, word: str) -> str:
        if word.endswith("y") and self._contains_vowel(word[:-1]):
            return word[:-1] + "i"
        return word

    def _step2(self, word: str) -> str:
        pairs = {
            "ational":"ate", "tional":"tion", "enci":"ence", "anci":"ance",
            "izer":"ize", "abli":"able", "alli":"al", "entli":"ent",
            "eli":"e", "ousli":"ous", "ization":"ize", "ation":"ate",
            "ator":"ate", "alism":"al", "iveness":"ive", "fulness":"ful",
            "ousness":"ous", "aliti":"al", "iviti":"ive", "biliti":"ble"
        }
        for suf, rep in pairs.items():
            if word.endswith(suf) and self._measure(word[:-len(suf)]) > 0:
                return word[:-len(suf)] + rep
        return word

    def _step3(self, word: str) -> str:
        pairs = {"icate":"ic","ative":"","alize":"al","iciti":"ic","ical":"ic","ful":"","ness":""}
        for suf, rep in pairs.items():
            if word.endswith(suf) and self._measure(word[:-len(suf)]) > 0:
                return word[:-len(suf)] + rep
        return word

    def _step4(self, word: str) -> str:
        suffixes = ["al","ance","ence","er","ic","able","ible","ant","ement","ment","ent","ion","ou","ism","ate","iti","ous","ive","ize"]
        for suf in suffixes:
            if word.endswith(suf) and self._measure(word[:-len(suf)]) > 1:
                stem = word[:-len(suf)]
                if suf == "ion" and not stem.endswith(("s","t")):
                    return word
                return stem
        return word

    def _step5a(self, word: str) -> str:
        if word.endswith("e"):
            stem = word[:-1]
            m = self._measure(stem)
            if m > 1 or (m == 1 and not self._cvc(stem)):
                return stem
        return word

    def _step5b(self, word: str) -> str:
        if self._measure(word) > 1 and self._ends_with_double(word) and word.endswith("l"):
            return word[:-1]
        return word

    def stem(self, word: str) -> str:
        word = word.lower()
        for step in (self._step1a, self._step1b, self._step1c,
                     self._step2,  self._step3,  self._step4,
                     self._step5a, self._step5b):
            word = step(word)
        return word

if __name__ == "__main__":
    stemmer = PorterStemmer()
    tests = [
        "caresses","ponies","ties","caress","cats",
        "feed","agreed","plastered","bled","motoring",
        "sing","conflated","troubled","sized","hopping",
        "tanned","falling","hissing","fizzed","failing",
        "filing"
    ]
    for w in tests:
        print(f"{w} → {stemmer.stem(w)}")
