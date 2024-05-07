from tenacity import retry, wait_exponential, stop_after_delay, retry_if_exception_type
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("openai_api_key")
client = openai.OpenAI()


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_delay(60),
    retry=retry_if_exception_type(Exception),
)
def get_completion(prompt, model, temperature=0, type="text"):
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": type},
    )

    return completion


def schema_form_filler_prompt(messages, schema):
    prompt = f"""
    You are chatting with a medical expert that needs help filling out an insurance form. 
    The expert is with the patient and will ask or check whatever you need to fill out said form.
    Depending on the form, the schema will change, so here is the schema for the current form:
    ---
    {schema}
    ---

    Please take the following steps to help out the medical expert:
    - Your goal is to completely fill out the form with the expert's help,\
        using the defined schema.
    - When you have gathered all the necessary information, find the\
          "completed" key in the schema and set it to "true".
    - The form needs to be expertly filled, so ask for any follow up\
          questions if necessary to get good answers.
    - However, you should not ask for any personal information or\
          anything outside the scope of the form.
    - The expert will not see the full schema, he will only read the\
          instruction you give him in the "next_message" key.
    - However, you will be provided the full conversation you have had\
          with the expert to ensure you always have context.
    - You must send the answers using valid json using the schema given above.
    - When you are ready to send the form, set the "completed" key to "true" \
        and end the following message using the "next_message" key: \
        "I have gathered the necessary information, please click next."


    Here is the conversation so far, remember to send your next message\
          to the expert using the "next_message" key:
    <conv>
    {messages}
    </conv>
    """
    response = get_completion(
        prompt=prompt, model="gpt-4-1106-preview", type="json_object"
    )
    return response.choices[0].message.content


def form_fill_prompt(insurance_form_schema, data):
    prompt = f"""
      You need to fill out an insurance form for a patient.
      Here is the schema for the form or a set of examples of what the section\
        should look like:
      ---
      {insurance_form_schema}
      ---
      The patient has provided the following information:
      ---
      {data}
      ---
      Please take the following steps to fill out the form:
      - Your goal is to completely fill out the form using the provided data.
      - The form needs to be expertly filled
      - Follow the schema in the exact order it is presented
      - Give me the form between xml <form> tags
      - The actual form should be in markdown format. \
        Remember that sometimes, no format is necessary. \
        Just follow the schema and the examples.
      """

    response = get_completion(prompt=prompt, model="gpt-4-1106-preview")
    return response.choices[0].message.content


def form_grader_prompt(insurance_form_schema, data):
    prompt = f"""
      A medical expert filled out the near the end form but needs to ensure it will pass the insurance criteria.
      The goal is to ensure everything required by the insurance company is filled out correctly.

      The insurance form schema, guidelines, or examples you need to follow to grade the form are the following:
      ---
      {insurance_form_schema}
      ---
      
      Read the following form filled out by the expert:
      ---
      {data}
      ---

      

      Please take the following steps to grade the form:
      - Your goal is to completely grade the form using the provided schema.
      - The form needs to be expertly graded
      - Follow the schema, guidelines, or examples
      - Give me a A-F grade for the form
      - Give your reasoning, backing up your grade with the schema, guidelines, or examples

      A: The form is filled out perfectly according to the schema with no errors or omissions.
      B: The form is filled out well with minor errors or omissions that do not significantly impact the processing of the claim.
      C: The form has several errors or omissions, but these could be corrected without extensive rework.
      D: The form has significant errors or omissions that would require substantial rework to meet the insurance criteria.
      F: The form is incomplete or filled out incorrectly to the extent that it would likely be rejected by the insurance company.
      """

    response = get_completion(prompt=prompt, model="gpt-4-1106-preview")
    return response.choices[0].message.content
