import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

#model = init_chat_model("command-r-plus", model_provider="cohere", API_KEY=API_KEY)

def getFeedback(model):
    input = []

    ##Parse through json
    with open("conversations.json", "r") as ConversationFile:
        with open("AI_Arguments.json","r") as aiArgFile:
            ConversationData = json.load(ConversationFile)
            aiArgData = json.load(aiArgFile)
            for i in range(len(ConversationData[0]['messages'])):
                input.append(ConversationData[0]['messages'][i]['text'])
                input.append(aiArgData[0]['filtered_responses'][i]['response'])

    ##System template
    system_template = "You are an expert in debating, " \
    "critiquing a student eager to learn about their debate skills. Your task is to {specialization}."


    ##Main template
    templateWeak = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "This is the conversation "
        "with every odd index being the student and every even index being an AI Expert: {text}")]
    )

    templateStrong = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "This is the conversation "
        "with every odd index being the student and every even index being an AI Expert: {text}")]
    )

    templateGrade = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "This is the conversation "
        "with every odd index being the student and every even index being an AI Expert: {text}")]
    )

    ##Main Prompt
    promptWeak = templateWeak.invoke({"specialization": "point out the student's weaknessess in jot notes", "text": input})
    promptStrong = templateStrong.invoke({"point out the student's strengths in jot notes": "debating", "text": input})
    promptGrade = templateGrade.invoke({"specialization": "grade the over all strength of the student's debating out of 10", "text": input})

    result = {
        "Strengths": model.invoke(promptStrong).content,
        "Weaknesses": model.invoke(promptWeak).content,
        "Grade": model.invoke(promptGrade).content
    }

    if os.path.exists("feedback.json") and os.path.getsize("feedback.json") > 0:
        with open("feedback.json", "r") as file:
            data = json.load(file)
        data.append(result)
    else:
        data = [result]

    with open("feedback.json", "w") as file:
        json.dump(data, file, indent=4)

    return result

if __name__ == "__main__":
    res = getFeedback()
    print(res)


    


