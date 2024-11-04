import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class SummarizeLlm:
    def __init__(self, language: str):
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.language = language

    def summarize_section(
        self, title: str, section: str, summarized_sections: list[str]
    ) -> str:
        with open(
            os.path.join(os.path.dirname(__file__), "system_prompt.md"),
            "r",
            encoding="utf-8",
        ) as file:
            system_prompt = file.read()

        with open(
            os.path.join(os.path.dirname(__file__), "section_prompt.md"),
            "r",
            encoding="utf-8",
        ) as file:
            section_prompt = file.read()

        print(title)
        print(section)
        print(summarized_sections)

        messages = (
            [("system", system_prompt)]
            + list(map(lambda x: ("ai", x), summarized_sections))
            + [("human", section_prompt)]
        )
        prompt_template = ChatPromptTemplate.from_messages(messages)
        parser = StrOutputParser()

        chain = prompt_template | self.model | parser

        return chain.invoke(
            input={"language": self.language, "title": title, "section": section}
        )
