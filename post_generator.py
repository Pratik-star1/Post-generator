from llm_helper import llm
from few_shot import FewShotPosts

# Initialize FewShotPosts instance
few_shot = FewShotPosts()


def map_length_to_lines(length):
    """Maps the given length to a string description of the number of lines."""
    length_mapping = {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines",
        "Long": "11 to 15 lines"
    }
    return length_mapping.get(length, "Unknown length")


def generate_post(length, language, tag):
    """Generates a LinkedIn post based on the input parameters."""
    prompt = create_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content.strip()


def create_prompt(length, language, tag):
    """Creates a prompt for the LLM using input length, language, and tag."""
    length_str = map_length_to_lines(length)

    prompt = (
        f"Generate a LinkedIn post using the following details. No preamble:\n\n"
        f"1) Topic: {tag}\n"
        f"2) Length: {length_str}\n"
        f"3) Language: {language}\n\n"
        f"If Language is Hinglish, it means a mix of Hindi and English. "
        f"The script for the post should always be in English."
    )

    # Fetch example posts for few-shot learning
    examples = few_shot.get_filtered_posts(length, language, tag)
    if examples:
        prompt += "\n\n4) Use the following examples as a guide for writing style:"
        for i, post in enumerate(examples[:2]):  # Use a maximum of two examples
            prompt += f"\n\nExample {i+1}:\n{post['text']}"

    return prompt


if __name__ == "__main__":
    # Test the function with sample inputs
    test_post = generate_post("Medium", "English", "Mental Health")
    print(test_post)
