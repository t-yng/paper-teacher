from app.paper import load_paper


if __name__ == "__main__":
    pdf_path = "test/pdf/genmma.pdf"

    paper = load_paper(pdf_path)

    # LLMに論文の内容を逐次的に送信して段階的に要約を取得
