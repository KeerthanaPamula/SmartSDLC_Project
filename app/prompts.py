REQUIREMENT_ANALYSIS_PROMPT = (
    "You are a software analyst. From the following project description, identify and list:\n"
    "1. Functional Requirements\n"
    "2. Non-Functional Requirements\n\n"
    "Project Description:\n{project_description}\n"
)

CODE_GENERATION_PROMPT = (
    "You are a code generation assistant.\n"
    "Given the software requirement below, generate clean, modular {language} code using the {framework} framework.\n"
    "Include comments and best practices.\n\n"
    "Requirement:\n{requirements}\n"
)

TEST_CASE_GENERATION_PROMPT = (
    "You are a software testing assistant.\n"
    "Based on the following code or user story, generate both unit test cases and functional test cases.\n"
    "Use a standard format for test cases and include assertions if applicable.\n\n"
    "Input:\n{context}\n"
)

