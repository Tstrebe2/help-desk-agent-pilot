from langchain_community.llms import FakeListLLM

def get_llm_response(prompt):
    fake_llm = FakeListLLM(responses=[
                               "Hello", 
                               "This app is currently under development.", 
                               "Please check back later."
                            ])
    response = fake_llm.invoke(prompt)
    return response