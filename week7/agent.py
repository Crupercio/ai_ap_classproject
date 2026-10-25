from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, tool

# Custom tool: the docstring and Args section are what the agent reads
@tool
def gpa_calculator(grades: str, credits: str) -> str:
    """Calculates a weighted GPA on a 4.0 scale from letter grades and credit hours.
    Use this when the user wants a GPA or asks what their GPA would be.

    Args:
        grades: Comma-separated letter grades, like "A,B+,A-"
        credits: Comma-separated credit hours in the same order, like "3,4,3"
    """
    points = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
              "C+": 2.3, "C": 2.0, "C-": 1.7, "D": 1.0, "F": 0.0}
    g = [x.strip().upper() for x in grades.split(",")]
    c = [float(x) for x in credits.split(",")]
    if len(g) != len(c):
        return "Error: number of grades and credits must match."
    if any(x not in points for x in g):
        return "Error: unknown letter grade."
    total = sum(points[a] * b for a, b in zip(g, c))
    return f"GPA: {total / sum(c):.2f}"

# Point smolagents at Ollama instead of Hugging Face
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5:7b",
    api_base="http://localhost:11434",
    num_ctx=8192,
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), gpa_calculator],  # 2 tools, 1 custom
    model=model,
    max_steps=8,  # cap steps so it can't loop forever
)

if __name__ == "__main__":
    import sys
    agent.run(sys.argv[1])