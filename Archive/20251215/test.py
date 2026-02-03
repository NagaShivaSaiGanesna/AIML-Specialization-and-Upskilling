from langchain.prompts import PromptTemplate
# Define a template with a placeholder
template = PromptTemplate.from_template("Tell me a joke about {topic}")
# Fill the placeholder dynamically
result = template.format(topic="cats")
print(result)
# Output: Tell me a joke about cats