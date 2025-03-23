import json
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

model = init_chat_model("gpt-4o-mini", model_provider="openai")

def reading_json(filename: str) -> dict[str, str]:
    """
    Reads the JSON file and returns the data as a dictionary
    with original and AI 1st suggested draft argument
    """
    with open(filename, "r") as file:
        data = json.load(file)
    
    word_transcript = {}
    dif_roles = ""
    for speakers in data:
        if "Arguments" in speakers:
            word_transcript["Arguments"] = speakers["Arguments"]
        else:
            dif_roles += word_transcript[speakers] + ";"
    word_transcript["draft_prospectives"] = dif_roles
    return word_transcript

def assessing_bias(filename: str, model):
    """
    Convert system and user text into messages that can be used by langchain
    Return dict of the updated text with biases removed
    """
    given_dict = reading_json(filename)

    system_template = "You're an expert in {bias_finder}" \
    " Your job is to assess the argument recommended by another chatbot {draft_prospectives}. The other argument is based on" \
    " the triple-bottom-line framework. The triple-bottom-line framework is a theory that includes an organization's contributions" \
    " to social well-being, environmental health, and a just economy." \
    " You will compare the given user message {user} to the proposed argument the previous chatbot provided and assess it for ethical biases and concerns." \
    " Then, you should return a more ethically bound, less discriminatory response to further reinforce the rubrics while accounting for biases."

    prompt_template = ChatPromptTemplate.from_messages([
        {"role": "system", "content": system_template},
        {"role": "user", "content": given_dict["Arguments"]},  # User input for comparison
        {"role": "system", "content": given_dict["draft_prospectives"]}  # Old chatbot response
    ])

    prompt = prompt_template.invoke({
        "bias_finder": "An expert in detecting ethical biases, ensuring fairness, and refining arguments for inclusivity, social well-being, environmental health, and economic justice.",
        "draft_prospectives": "An argument generated by a previous chatbot for assessment and ethical refinement.",
        "user": given_dict["Arguments"]
    })
    response = model.invoke(prompt)
        
    return_json("ai_response.json", response)

def return_json(filename: str, new_argument: str):
    """
    Updating the JSON file with the suggestions
    """
    with open(filename, "r") as f:
        data = json.load(f)  # Parse JSON into a dictionary

        data[0]["filtered_response"].append({"response": new_argument})

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)