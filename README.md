# GenAI_Tools_Agent
LLMs: Large language models is backbone of AI Application, 
These models are Trained on vast  amount of data enabling them
to undeestand human language, process context, and generate meaning full response. 
we often iteract with LLM's Throgh AI AI Assistant/ Application and chatbot

AI Assistants/Applications
These include tools like ChatGpt Copilot and other Gen AI Powered Solution that assist Tester to inhance productivity by providing intelligent suggestions and automation repeatative tasks

AI Agents: These is autonoumus system that precive their env and make decision and take actions to achive specific goals with minimal human iteractions



====================================================================================================
Prompt Engineering:

AI output quality depends on context constraints and clarity

Exact things are need only those questions can be fired on AI otherwose AI gives assumed ans and that
will be waste of time and waste of token 

1. Context: Role play Provide background like role play and scenarios
example: you are a test engineer in device domain / bamking domain
2. Constarints: Set a clear goal and limit
3. Be Explicit about output format

example : I am traveling by road from pune to mumbai in september list only historical place on route by car required <1 hour detour> provide in a table with name, location and estimation detour time


Poor vs Good Prompt exmaple

example 1. find bug in my login code

prompt example: You are QA Engineer reviving my login code for security check focus on sql injection login routine return bullet point with issue description and line no

example: You are my interview preparation trainer for python programming train me in such a way that I will ans all interview questions. focus on deep concept understanding and expanation write a bullet point with well intended and managed

lesson:-> Role Defination + constratinst + clarity

Type of Prompt engineering
1. Zero Shot Prompting:
2. Give an as much detail you can ans step for generation of test cases
poor Prompt:
write test case for login scenario

example
Add Role
you are a QA Enginner of e-commerese site

Specify FUnctionality
wrie a test case for login invald login and password feature

Add Constraints
Add 2 negative scenario for each feature and cover browser compatibity

add Format
provide result in table format with test case id, title, steps expected result

add prioritization
add priortization high low and medium


====================================================================================================

2. FEW SHOT PROMPTING
supplying the AI with few example of desirged output or format beore asking questions

PROMPT Template: You are QA Engineer here are 2 example of test case refer them and generate new test case for this feature on same format

====================================================================================================
3. CHAIN OF THOUGHT PROMPTING

asking the AI reason step by step before providing final ans
Prompts example
you are QA Engineer lets think step by step how would you design test case for login feature


####################################################################################################
What is a Token?

A token is the smallest unit of text that a language model (like GPT-5) processes or understands.

You can think of tokens as pieces of words — they’re not exactly words or characters, but something in between

# best practice to to save token

Best Practice:

Remove unnecessary words.

Don’t include large repeated instructions in every call.

Use short variable names and compact instructions.

❌ Bad example:

You are a helpful assistant. Please write a detailed explanation about Python lists with examples.


✅ Better:

Explain Python lists with examples.


💡 Tip: Once you set the system instruction (like “You are a helpful assistant”), you don’t need to repeat it each time — save it at session level.
