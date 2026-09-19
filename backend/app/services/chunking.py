import re


class TextChunkingService:
    def __init__(
        self,
        max_chunk_size: int = 1000,
        overlap: int = 200,
    ):
        if max_chunk_size <= 0:
            raise ValueError("max_chunk_size must be greater than 0")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= max_chunk_size:
            raise ValueError(
                "overlap must be smaller than max_chunk_size"
            )

        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        text = text.strip()

        if not text:
            return []

        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(r"\n{2,}", text)
            if paragraph.strip()
        ]

        chunks: list[str] = []
        current = ""

        for paragraph in paragraphs:
            if len(paragraph) > self.max_chunk_size:
                if current:
                    chunks.append(current)
                    current = ""

                chunks.extend(self._split_long_paragraph(paragraph))
                continue

            candidate = (
                paragraph
                if not current
                else f"{current}\n\n{paragraph}"
            )

            if len(candidate) <= self.max_chunk_size:
                current = candidate
                continue

            chunks.append(current)

            available_overlap = max(
                0,
                self.max_chunk_size - len(paragraph) - 2,
            )

            overlap_length = min(
                self.overlap,
                available_overlap,
            )

            if overlap_length > 0:
                overlap_text = current[-overlap_length:]
                current = f"{overlap_text}\n\n{paragraph}"
            else:
                current = paragraph

        if current:
            chunks.append(current)

        return chunks

    def _split_long_paragraph(self, paragraph: str) -> list[str]:
        chunks: list[str] = []
        start = 0

        while start < len(paragraph):
            end = min(
                start + self.max_chunk_size,
                len(paragraph),
            )

            if end < len(paragraph):
                split_position = paragraph.rfind(" ", start, end)

                if split_position > start:
                    end = split_position

            chunk = paragraph[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(paragraph):
                break

            start = max(end - self.overlap, start + 1)

        return chunks


text_chunking_service = TextChunkingService()
