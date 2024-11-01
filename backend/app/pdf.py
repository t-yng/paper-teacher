from app.paper import load_paper


if __name__ == "__main__":
    pdf_path = "test/pdf/genmma.pdf"

    paper = load_paper(pdf_path)

    # TODO: LLMに論文の内容を逐次的に送信して段階的に要約を取得
    # TODO: 論文のPDFを受け取ってセクションごとに要約を生成するAPIの実装
    # TODO: フロント側の実装
