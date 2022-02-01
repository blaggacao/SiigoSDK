from dataclasses import dataclass


@dataclass
class AuthToken:
    type: str
    token: str

    def form(self) -> str:
        return f'{self.type} {self.token}'
