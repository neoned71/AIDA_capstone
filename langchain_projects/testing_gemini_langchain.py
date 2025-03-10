from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")
prompt = "Tell me what is"
answer=llm.invoke(prompt)


import argparse

import json
parser = argparse.ArgumentParser( description="My script")
parser.add_argument('-up', '--user_prompt', type=str, 
                    help="What is it that you would like to make today?", required=False)

args = parser.parse_args()


llm = ChatGoogleGenerativeAI(model="gemini-pro")
print(args.user_prompt)
print(llm)

#templating
from langchain_core.prompts import PromptTemplate

u_input ="create a shell script to create a simple C code with a makefile with some boilerplat code to compile a basic main file"
prompt_template = PromptTemplate.from_template("Can you generate instructions for commands to {user_input}, but all the instructions should follow the schema. ")
u_input = args.user_prompt
# prompt_template.invoke({"topic": "cats"})
prompt = prompt_template.format(user_input=u_input) 
print("The prompt is:",prompt) 


# schema = {"commands":"List of commands in the format of dictionaries comntaining the command to be executed."}
# llm = llm.with_structured_output(schema)
# print("invoking \n")


#adding a schema 
prompt+="And the schema of the output should be in the following format strictly {commands:[{command:str}]}. do not use any gui application in any of the instructions but do run all the initialization code like npm install or any if needed, all blocking commands should be run in the background, make sure it is a small and perfectly valid legally valid JSON string"

l=llm.invoke(prompt)
commands_str = l.content[l.content.index("{"):l.content.rindex("}")+1]

print(commands_str)
commands = json.loads(commands_str)['commands']

import os

import pexpect

# Start a shell session
shell = pexpect.spawn('/bin/sh', encoding='utf-8', echo=True,timeout=50)

# # Run commands
# shell.sendline('cd /path/to/directory')
# shell.sendline('pwd')  # Prints the current directory
# shell.sendline('ls')   # Lists files in the directory

for i in commands:
    print("running: ",i['command'])
    shell.sendline(i['command'])
    shell.expect_exact("(py")
    output = shell.before.strip().split('\n', 1)[-1]
    print(output)

import time
time.sleep(4)
# Close the shell
shell.close()



