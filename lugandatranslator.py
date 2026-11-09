import re
import tkinter as tk
from tkinter import font


WORD_DICTIONARY = {
    "hello": "ki kati",
    "goodbye": "weeraba",
    "please": "nsaba",
    "thank": "webale",
    "you": "ggwe",
    "yes": "yee",
    "no": "nedda",
    "good": "lungi",
    "bad": "kibi",
    "friend": "mukwano",
    "family": "amaka",
    "house": "ennyumba",
    "home": "eka",
    "food": "emmere",
    "water": "amazzi",
    "book": "ekitabo",
    "school": "essomero",
    "work": "omulimu",
    "love": "okwagala",
    "cat": "empeewo",
    "dog": "embwa",
    "child": "omwana",
    "mother": "maama",
    "father": "taata",
    "i": "nze",
    "we": "ffe",
    "they": "bo",
    "eat": "okulya",
    "drink": "okunywa",
    "want": "njagala",
    "where": "wa",
    "what": "ki",
    "today": "leero",
    "tomorrow": "enkya",
}

PHRASE_DICTIONARY = {
    "how are you": "oli otya",
    "thank you": "webale nnyo",
    "good morning": "wasuze otya",
    "good night": "sula bulungi",
    "i love you": "nkwagala",
}

_PHRASE_PATTERN = re.compile(
    r"\b(?:how\s+are\s+you|thank\s+you|good\s+morning|good\s+night|i\s+love\s+you)\b",
    re.IGNORECASE,
)
_WORD_PATTERN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def _match_case(source: str, translated: str) -> str:
    if source.isupper():
        return translated.upper()
    if source.istitle() or (source and source[0].isupper()):
        return translated.capitalize()
    return translated


def translate_text(text: str) -> str:
    """Translate dictionary words and phrases; keep unknown text unchanged."""
    with_phrases = _PHRASE_PATTERN.sub(
        lambda match: _match_case(
            match.group(0),
            PHRASE_DICTIONARY[" ".join(match.group(0).lower().split())],
        ),
        text,
    )
    return _WORD_PATTERN.sub(
        lambda match: _match_case(
            match.group(0),
            WORD_DICTIONARY[match.group(0).lower()],
        )
        if match.group(0).lower() in WORD_DICTIONARY
        else match.group(0),
        with_phrases,
    )


class LugandaTranslator:
    BACKGROUND = "#f4f3ec"
    CARD = "#fffefa"
    GREEN = "#174a3b"
    MUTED = "#65766e"
    BORDER = "#dce3db"
    ACCENT = "#d6edb8"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Luganda Translator")
        self.root.geometry("760x700")
        self.root.minsize(580, 600)
        self.root.configure(bg=self.BACKGROUND)

        self.body_font = font.Font(family="Segoe UI", size=11)
        self.heading_font = font.Font(family="Segoe UI", size=27, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=10, weight="bold")

        self._build_ui()

    def _build_ui(self) -> None:
        page = tk.Frame(self.root, bg=self.BACKGROUND, padx=38, pady=30)
        page.pack(fill="both", expand=True)

        tk.Label(
            page,
            text="A LITTLE LANGUAGE TOOL",
            bg=self.BACKGROUND,
            fg=self.GREEN,
            font=(self.body_font.actual("family"), 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            page,
            text="Luganda Translator",
            bg=self.BACKGROUND,
            fg=self.GREEN,
            font=self.heading_font,
        ).pack(anchor="w", pady=(5, 2))
        tk.Label(
            page,
            text="A simple English-to-Luganda dictionary, made for everyday words.",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=self.body_font,
        ).pack(anchor="w", pady=(0, 20))

        card = tk.Frame(
            page,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=22,
            pady=20,
        )
        card.pack(fill="both", expand=True)

        language_row = tk.Frame(card, bg=self.CARD)
        language_row.pack(fill="x", pady=(0, 14))
        self._language_badge(language_row, "ENGLISH").pack(side="left")
        tk.Label(
            language_row,
            text="→",
            bg=self.CARD,
            fg=self.MUTED,
            font=(self.body_font.actual("family"), 15, "bold"),
            padx=12,
        ).pack(side="left")
        self._language_badge(language_row, "LUGANDA").pack(side="left")

        tk.Label(
            card,
            text="Your text",
            bg=self.CARD,
            fg=self.GREEN,
            font=self.label_font,
        ).pack(anchor="w", pady=(0, 7))
        self.input_box = tk.Text(
            card,
            height=5,
            wrap="word",
            undo=True,
            font=self.body_font,
            bg="#ffffff",
            fg="#20342d",
            insertbackground=self.GREEN,
            relief="flat",
            padx=12,
            pady=10,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.GREEN,
        )
        self.input_box.pack(fill="x")
        self.input_box.insert("1.0", "Hello, friend! How are you?")

        actions = tk.Frame(card, bg=self.CARD)
        actions.pack(fill="x", pady=14)
        tk.Button(
            actions,
            text="Translate",
            command=self._translate,
            bg=self.GREEN,
            fg="#ffffff",
            activebackground="#24634f",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            font=self.label_font,
        ).pack(side="left")
        tk.Button(
            actions,
            text="Clear",
            command=self._clear,
            bg=self.CARD,
            fg=self.GREEN,
            activebackground=self.ACCENT,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            font=self.label_font,
        ).pack(side="left", padx=(8, 0))

        tk.Label(
            card,
            text="LUGANDA TRANSLATION",
            bg=self.CARD,
            fg=self.GREEN,
            font=self.label_font,
        ).pack(anchor="w", pady=(2, 7))
        self.output_box = tk.Text(
            card,
            height=5,
            wrap="word",
            font=self.body_font,
            bg="#f1f7e9",
            fg=self.GREEN,
            relief="flat",
            padx=12,
            pady=10,
            highlightthickness=1,
            highlightbackground="#e1ebd6",
            state="disabled",
        )
        self.output_box.pack(fill="both", expand=True)
        self._set_output("Your translation will appear here.")

        tk.Label(
            page,
            text=f"{len(WORD_DICTIONARY) + len(PHRASE_DICTIONARY)} dictionary entries  ·  "
            "Words not found in the dictionary stay in English.",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=(self.body_font.actual("family"), 9),
            wraplength=680,
            justify="left",
        ).pack(anchor="w", pady=(14, 0))

        self.root.bind("<Control-Return>", lambda _event: self._translate())

    def _language_badge(self, parent: tk.Frame, text: str) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            bg=self.ACCENT,
            fg=self.GREEN,
            padx=10,
            pady=5,
            font=(self.body_font.actual("family"), 9, "bold"),
        )

    def _set_output(self, text: str) -> None:
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.configure(state="disabled")

    def _translate(self) -> None:
        source = self.input_box.get("1.0", "end-1c").strip()
        if not source:
            self._set_output("Type a word or sentence above to get started.")
            self.input_box.focus_set()
            return
        self._set_output(translate_text(source))

    def _clear(self) -> None:
        self.input_box.delete("1.0", "end")
        self._set_output("Your translation will appear here.")
        self.input_box.focus_set()


def main() -> None:
    root = tk.Tk()
    LugandaTranslator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
