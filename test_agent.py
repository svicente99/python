## python ##

#  code assembled with DeepSeek hints (May, 15th 2026)

import requests
import json

def call_llm(messages):
	response = requests.post(
		"http://localhost:11434/api/chat",
		json = {
			"model": "deepseek-r1:1.5b", 
			"messages": messages, 
			"stream": False, 
			"think": False			# Disables thinking mode
		}
	)
	
	# Check if request was successful
	if response.status_code != 200: 
		error_data = response.json()
		raise Exception(f"Ollama API error (status {response.status_code}): {error_data.get('error', 'Unknown error')}")
	
	data = response.json()
	
	# Check for error in response body (some errors return 200 but contain error field)
	if "error" in data:
		raise Exception(f"Ollama model error: {data['error']}")
	
	# Now safe to access message content, but first verify if something is still wrong
	if "message" not in data:
		raise ValueError(f"Unexpected response format: {data}")	
	
	# Finally, the answer can be returned
	return data["message"]["content"]

# Define your tools
def calculator(expression):
    return str(eval(expression))

def get_current_time():
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# Simple ReAct loop
def run_agent(question):
    scratchpad = ""
    for step in range(5):
        prompt = f"""You are an AI agent. Follow this format exactly:

Question: {question}
{scratchpad}
Thought: (what you need to do)
Action: (tool name: calculator or get_current_time)
Action Input: (input for the tool)
Final Answer: (your final response when done)

Available tools:
- calculator -> Performs math, e.g., "calculator" with input "12 * (3 + 7)"
- get_current_time -> Gets current time, no input needed

Now, this is the answer:"""

        response = call_llm([{"role": "user", "content": prompt}])
        
        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()
        
        if "Action:" in response and "Action Input:" in response:
            action = response.split("Action:")[1].split("\n")[0].strip()
            action_input = response.split("Action Input:")[1].split("\n")[0].strip()
            
            if action == "calculator":
                result = calculator(action_input)
            elif action == "get_current_time":
                result = get_current_time()
            else:
                result = "Tool not found"
            
            scratchpad = response + f"\nObservation: {result}\n"
    
    return "Max steps reached"

# Try it
print(run_agent("What time is it? Also calculate 12 * (3 + 7)"))
