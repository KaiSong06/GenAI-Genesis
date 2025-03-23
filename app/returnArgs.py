import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

model = init_chat_model("command-r-plus", model_provider="cohere", API_KEY=API_KEY)


def returnArguments(argument: str):
    
    ##Prompts
    system_template = "You are an expert in  {specialization}" \
    "Another expert is arguing their point of view of a topic and you are tasked to judge their argument " \
    "based on your experience and specialization. After judging, provide your own argument against them in 200-300 words. " 
    
    #economics and issues dealing with economics, both globally and domestically in various specific countries in the world.
    #environmental sciences and issues.
    #sociology and human rights advocacy.

    ##Individual templates
    templateECON = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "This is their argument: {text}")]
    )

    templateENV = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "This is their argument: {text}")]
    )

    templateSOC = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "This is their argument: {text}")]
    )
    ##Run templates
    promptECON = templateECON.invoke({"specialization": 
                                      "economics and issues dealing with economics,"
                                      " both globally and domestically in various specific "
                                      "countries in the world.", "text": argument})
    promptENV = templateECON.invoke({"specialization": "environmental sciences and issues.",
                                        "text": argument})
    promptSOC = templateSOC.invoke({"specialization": "sociology and human rights advocacy.",
                                    "text": argument})
    
    ##Get responses
    responseECON = model.invoke(promptECON)
    responseENV = model.invoke(promptENV)
    responseSOC = model.invoke(promptSOC)

    ##Create result json
    result = {
        "Economics": responseECON.content,
        "Environment": responseENV.content,
        "Sociology": responseSOC.content,
        "Argument": argument
    }

    # Ensure conversations.json exists
    if os.path.exists("AI_Arguments.json") and os.path.getsize("AI_Arguments.json") > 0:
        with open("AI_Arguments.json", "r") as file:
            data = json.load(file)
        data.append(result)
    else:
        data = [result]

    with open("AI_Arguments.json", "w") as file:
        json.dump(data, file, indent=4)

    return result

if __name__ == "__main__":
    argument = "College tuition should be free for all students. " \
    "In doing this, the workforce will be more educated and skilled. " \
    "In combination with this, competition is driven increasing the productivity of students."
    result = returnArguments(argument)
    print(json.dumps(result, indent=4))