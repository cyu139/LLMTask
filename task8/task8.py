from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import subprocess
from collections import Counter

question = "Is John the grandfather of David?"
print(f"Question: {question}\n")

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

template = """You are a Prolog translator. Translate the user's yes/no question into a single ground Prolog query (a query with NO variables, only lowercase atoms).
ONLY output the raw Prolog query string. Do not include markdown, formatting, periods, or any conversational text.

Question: {question}"""

prompt = PromptTemplate.from_template(template)
output_parser = StrOutputParser()
chain = prompt | chat_model | output_parser

print("--- 5 Queries made using LangChain ---")
translations = []

for i in range(1, 6):
    query = chain.invoke({"question": question})
    clean_query = query.strip().rstrip('.')
    translations.append(clean_query)
    print(f"Query {i}: {clean_query}")
print()

prolog_file = "familyKB.pl"
prolog_results = []

print("--- Results after running each query through prolog ---")

for i, query in enumerate(translations, 1):
    prolog_goal = f"forall({query}, writeln({query}))"
    try:
        result = subprocess.run(
            ["swipl", "-q", "-s", prolog_file, "-g", prolog_goal, "-t", "halt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True 
        )
        output = result.stdout.strip()
        
        if output:
            prolog_results.append(output)
            print(f"Test {i} yielded: {output}")
        else:
            prolog_results.append("Unsure / No match")
            print(f"Test {i} yielded: Unsure / No Match")
            
    except subprocess.CalledProcessError:
        #crash handler
        prolog_results.append("Error")
        print(f"Query {i} yielded: Error (bad syntax)")
print()

# k-majority vote to determine best results
vote_counts = Counter(prolog_results)
final_answer = vote_counts.most_common(1)[0][0]

print("--- K-Majority Vote Final Result ---")
for ans, count in vote_counts.items():
    print(f"Votes: {count} | Answer: {ans}")

print(f"\nFinal Answer: {final_answer}")

trace_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

trace_template = """You are a logical inference engine.
Based strictly on the provided Prolog Knowledge Base and the evaluated query,
provide a step by step logical inference trace proving the result.
- DO NOT use conversational filler (e.g., "We first need to check...", "Let's take...").
- DO NOT show failed branches or backtracking (e.g., do not show testing incorrect parents).
- ONLY list the successful chain of facts and rules that directly lead to the conclusion.
- Keep each step to a single, concise formal statement.

Knowledge Base:
{knowledge_base}

Question: {question}
Winning Prolog Query: {query}
Prolog Answer: {answer}

Output format:
Trace:
1. (Fact 1)
2. (Fact 2)
3. (Rule) -> (Conclusion)
...
Conclusion: (True or False) - The answer is [Final Answer]
"""

trace_prompt = PromptTemplate.from_template(trace_template)
trace_chain = trace_prompt | trace_model | output_parser

with open(prolog_file, "r") as file:
    kb = file.read()

winning_query = translations[0]
print("---Trace---")
trace_output = trace_chain.invoke({
    "knowledge_base": kb,
    "question": question,
    "query": winning_query,
    "answer": final_answer
})

print(trace_output)