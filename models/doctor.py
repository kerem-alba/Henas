class Doctor:
    def __init__(self, code: str, name: str, seniority: int, shift_count: int):
        self.code = code
        self.name = name
        self.seniority = seniority
        self.shift_count = shift_count

    def __repr__(self):
        return f"Doctor(code={self.code}, name={self.name}, seniority={self.seniority}, shift_count={self.shift_count})"
