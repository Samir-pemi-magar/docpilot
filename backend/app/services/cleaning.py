import re


class TextCleaningService:
    def clean(self, text: str) -> str:
        text = text.replace("\x00", "")
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        lines = [
            line.rstrip()
            for line in text.split("\n")
        ]

        text = "\n".join(lines)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()


text_cleaning_service = TextCleaningService()
