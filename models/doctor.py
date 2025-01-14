class Doctor:
    def __init__(self, code: str, name: str, seniority: int, shift_count: int, shift_areas: list = None):
        self.code = code
        self.name = name
        self.seniority = seniority
        self.shift_count = shift_count
        self.shift_areas = shift_areas if shift_areas else []

    def __repr__(self):
        return (
            f"Doctor(code={self.code}, name={self.name}, seniority={self.seniority}, "
            f"shift_count={self.shift_count}, shift_areas={self.shift_areas})"
        )
