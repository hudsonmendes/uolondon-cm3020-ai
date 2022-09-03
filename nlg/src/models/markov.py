    from typing import Dict, List, Union
    import re
    import random


    class MarkovNLG:
        transitions: Dict[str, List[str]]

        def __init__(self):
            self.transitions = {}

        def train(self, ds: Union[str, List[str]]) -> None:
            ds = self._normalise_and_split(ds)
            for dsi in ds:
                tokens = dsi.split(" ")
                for i in range(len(tokens)-1):
                    token1 = tokens[i]
                    token2 = tokens[i+1]
                    if token1 and token2:
                        if token1 not in self.transitions:
                            self.transitions[token1] = []
                        self.transitions[token1].append(token2)

        def generate(self, n: int, context: str = None) -> str:
            assert n is not None and n > 0
            context = self._normalise_and_split(context)[0]
            context_tokens = context.split(" ")
            state = context_tokens[-1] if context else self._random_valid_state()
            tokens = []
            if context_tokens:
                tokens.extend(context_tokens)
            for _ in range(n):
                if state not in self.transitions:
                    break
                next_state = random.choice(self.transitions[state])
                tokens.append(next_state)
                state = next_state
            return ' '.join(tokens)

        def _random_valid_state(self) -> str:
            return random.choice(list(self.transitions.keys()))

        def _normalise_and_split(self, ds: Union[str, List[str]]) -> List[str]:
            if isinstance(ds, str):
                ds = ds.split("\n") if "\n" in ds else [ds]
            for i in range(len(ds)):
                ds[i] = ds[i].lower()
                ds[i] = re.sub(r'[^0-9a-z]+', ' ', ds[i])
            return ds
