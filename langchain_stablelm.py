from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import LLMChain

tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-zephyr-1_6b')
model = AutoModelForCausalLM.from_pretrained(
    'stabilityai/stablelm-2-zephyr-1_6b',
    device_map="auto"
)

# Create the pipeline
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    # You can add optional parameters here to control generation:
    # max_new_tokens=50,  # Limit the length of the generated text
    # temperature=0.7,    # Control the randomness of the output
    # top_k=50,          # Limit the number of tokens considered at each step
    # top_p=0.95,         # Limit the cumulative probability of tokens considered
    # repetition_penalty=1.2  # Penalize the repetition of token sequences
)

# Initialize your LLM
llm = HuggingFacePipeline(pipeline=generator)

# Define your prompt
template = """Answer the user's question in JSON format.

Question: {question}
"""

prompt = [{'role': 'user', 'content': 'can you imgine that you are a web server that only responses in html back? if yes then only give output in pure html and ask a user to enter their name after a greeting in the center of the screen'}]


inputs = tokenizer.apply_chat_template(
    prompt,
    add_generation_prompt=True,
    return_tensors='pt'
)
# prompt = PromptTemplate(template=template, input_variables=["question"])

# Define the expected output format
output_parser = StructuredOutputParser.from_response_schemas(
    {
        "answer": {"type": "string"},
        "source": {"type": "string"},
    }
)

# Combine the prompt and output parser

chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain
response = chain.run("What is the capital of France?")


print(response)
# # Parse the output
# print(response.get('answer')) 
# print(response.get('source'))




# prompt = [{'role': 'user', 'content': 'can you imgine that you are a web server that only responses in html back? if yes then only give output in pure html and ask a user to enter their name after a greeting in the center of the screen'}]


# inputs = tokenizer.apply_chat_template(
#     prompt,
#     add_generation_prompt=True,
#     return_tensors='pt'
# )



# tokens = model.generate(
#     inputs.to(model.device),
#     max_new_tokens=1024,
#     temperature=0.5,
#     do_sample=True
# )

# print(len(tokens))

# print(tokenizer.decode(tokens[0], skip_special_tokens=False))

