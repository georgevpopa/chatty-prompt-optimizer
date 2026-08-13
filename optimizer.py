import openai
import json
import os
from pydantic import BaseModel

class ParsedIntent(BaseModel):
    task_verb: str
    subject: str
    context: str
    constraints: list[str]
    output_format: str
    tone_persona: str

async def extract_intent(raw_input: str) -> dict:
    """Step 2: Lightweight LLM extracts intent into JSON schema using Groq (Free)"""
    
    # Uses the OpenAI SDK pointed to Groq's API
    client = openai.AsyncOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    
    # IMPROVED: Explicitly told the LLM to use arrays and gave examples
    system_prompt = """You are a prompt parsing engine. Extract the user's intent into a strict JSON object with these exact keys:
    - task_verb (string, e.g., "write", "analyze", "compare")
    - subject (string, what the task is about)
    - context (string, background info needed)
    - constraints (array of strings, e.g., ["rule1", "rule2"]. If none, use empty array [])
    - output_format (string, e.g., "JSON", "markdown table", "prose")
    - tone_persona (string, e.g., "expert", "friendly")
    If a field is not found, use "Not specified" (except constraints, which must be an empty array []). Output ONLY valid JSON."""

    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_input}
        ],
        response_format={"type": "json_object"}
    )
    
    intent_data = json.loads(response.choices[0].message.content)
    
    # SAFETY NET: Fix LLM mistakes before Pydantic validation
    if isinstance(intent_data.get("constraints"), str):
        # If LLM returned a string instead of a list, wrap it in a list
        intent_data["constraints"] = [intent_data["constraints"]]
    elif not isinstance(intent_data.get("constraints"), list):
        # If it's anything else (None, int), force empty list
        intent_data["constraints"] = []
        
    return intent_data

def compile_prompt(parsed_intent: dict, target_model: str) -> str:
    """Step 3 & 4: Rule Engine applies model heuristics and compiles"""
    
    # Added safety check in case Pydantic still fails, we can fallback
    try:
        pi = ParsedIntent(**parsed_intent)
    except Exception:
        # Fallback: manually map if validation still somehow fails
        pi = ParsedIntent(
            task_verb=parsed_intent.get("task_verb", "execute"),
            subject=parsed_intent.get("subject", "the request"),
            context=parsed_intent.get("context", "Not specified"),
            constraints=parsed_intent.get("constraints", []),
            output_format=parsed_intent.get("output_format", "prose"),
            tone_persona=parsed_intent.get("tone_persona", "expert")
        )
    
    # Base Compilation
    compiled = f"**Role:** {pi.tone_persona}\n\n"
    compiled += f"**Instruction:** {pi.task_verb} the following: {pi.subject}\n\n"
    
    # Model-Specific Heuristics (Rule Engine)
    if target_model == "anthropic":
        compiled += f"<context>\n{pi.context}\n</context>\n\n"
        if pi.constraints:
            compiled += f"<constraints>\n" + "\n".join(f"- {c}" for c in pi.constraints) + "\n</constraints>\n\n"
    else: # Default to OpenAI markdown style
        compiled += f"## Context\n{pi.context}\n\n"
        if pi.constraints:
            compiled += f"## Constraints\n" + "\n".join(f"- {c}" for c in pi.constraints) + "\n\n"
        
    compiled += f"**Output Format:** {pi.output_format}"
    
    # Anchor original intent to prevent drift
    compiled += f"\n\n**Original User Request (Anchor):** {pi.subject}"
    
    return compiled

async def optimize_prompt(raw_input: str, target_model: str) -> str:
    # Step 1 & 2: Parse
    intent_data = await extract_intent(raw_input)
    # Step 3 & 4: Compile
    final_prompt = compile_prompt(intent_data, target_model)
    return final_prompt