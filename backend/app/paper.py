from dataclasses import asdict, dataclass
from typing import List
import uuid
import markdown
from bs4 import BeautifulSoup, Tag
import html2text

import pymupdf4llm


@dataclass
class Section:
    """PDFページのセクション"""

    id: str
    order: int
    heading: str
    level: int
    body: str


class Paper:
    def __init__(self, title: str, sections: List[Section]):
        self.title = title
        self.sections = sections

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "sections": [asdict(section) for section in self.sections],
        }


def load_paper(file_path: str) -> Paper:
    """
    論文を読み込見込んでPaperオブジェクトを返す

    Args:
        file_path (str): 論文のファイルパス

    Returns:
        Paper: ペーパーオブジェクト
    """

    markdown_text = pymupdf4llm.to_markdown(file_path)

    sections = _extract_markdown_sections(markdown_text)
    title = sections[0].heading

    # abstractセクションがある場合は最初のセクションを除外する
    if "abstract" in sections[1].heading.lower():
        sections = sections[1:]
    else:
        # 著者名などを除いて最後の本文のみをabstractとして抽出する
        lines = sections[0].body.split("\n\n")
        sections[0].body = lines[len(lines) - 1]

    paper = Paper(
        title=title,
        sections=sections,
    )

    return paper


def _extract_section_content(
    current_header: Tag, next_header: Tag | None = None
) -> str:
    """
    現在の見出しから次の見出しまでの内容をHTMLで取得

    Args:
        current_header: 現在の見出しのTag
        next_header: 次の見出しのTag（最後のセクションの場合はNone）

    Returns:
        str: セクションの本文（HTML形式）
    """
    content_html = []
    current = current_header.next_sibling

    while current and (not next_header or current != next_header):
        if isinstance(current, Tag):
            content_html.append(str(current))
        current = current.next_sibling

    return "\n".join(content_html)


def _extract_markdown_sections(markdown_text: str) -> List[Section]:
    """
    Markdownテキストからセクション構造を抽出する
    各セクションの本文もMarkdownフォーマットのまま保持する

    Args:
        markdown_text (str): 解析対象のMarkdownテキスト

    Returns:
        List[Section]: セクションのリスト
    """
    # MarkdownをHTMLに変換
    html = markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
    soup = BeautifulSoup(html, "html.parser")

    # HTML to Markdownコンバーターを設定
    h2t = html2text.HTML2Text()
    h2t.body_width = 0  # 行の折り返しを無効化
    h2t.protect_links = True  # URLをそのまま保持
    h2t.unicode_snob = True  # Unicode文字を維持

    sections = []
    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    for i, header in enumerate(headers):
        # 見出しレベルとテキストを取得
        level = int(header.name[1])
        heading_text = header.get_text().strip()

        # 次の見出しを取得（最後のセクションの場合はNone）
        next_header = headers[i + 1] if i < len(headers) - 1 else None

        # セクションの本文をHTML形式で取得
        content_html = _extract_section_content(header, next_header)

        # HTMLをMarkdownに変換
        body_markdown = h2t.handle(content_html).strip()

        # セクションを作成
        section = Section(
            id=str(uuid.uuid4()),
            order=i + 1,
            heading=heading_text,
            level=level,
            body=body_markdown,
        )
        sections.append(section)

    return sections
