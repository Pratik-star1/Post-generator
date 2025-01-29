import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    """Processes LinkedIn posts by extracting metadata and unifying tags."""
    try:
        # Load raw posts
        with open(raw_file_path, encoding="utf-8") as file:
            posts = json.load(file)

        # Enrich posts with metadata
        enriched_posts = []
        for post in posts:
            metadata = extract_metadata(post["text"])
            post_with_metadata = {**post, **metadata}  # Merge original post with metadata
            enriched_posts.append(post_with_metadata)

        # Unify tags across all posts
        unified_tags = unify_tags(enriched_posts)
        for post in enriched_posts:
            current_tags = post["tags"]
            new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
            post["tags"] = list(new_tags)

        # Save processed posts to file if a path is provided
        if processed_file_path:
            with open(processed_file_path, "w", encoding="utf-8") as outfile:
                json.dump(enriched_posts, outfile, indent=4)
        
        return enriched_posts

    except Exception as e:
        print(f"An error occurred: {e}")
        raise


def extract_metadata(post_text):
    """Extracts metadata (line count, language, and tags) from a post."""
    template = """
    You are given a LinkedIn post. Extract the following details:
    1. Return a valid JSON. No preamble.
    2. JSON should have exactly three keys: line_count, language, and tags.
    3. tags is an array of text tags. Extract a maximum of two tags.
    4. Language should be either "English" or "Hinglish" (Hindi + English).
    
    Post: 
    {post_text}
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke(input={"post_text": post_text})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except OutputParserException as e:
        print(f"Error parsing metadata: {e}")
        return {"line_count": 0, "language": "Unknown", "tags": []}


def unify_tags(posts_with_metadata):
    """Unifies and maps tags from all posts to create a shorter list."""
    unique_tags = set(tag for post in posts_with_metadata for tag in post["tags"])
    unique_tags_list = ",".join(unique_tags)

    template = """
    Unify the following tags:
    1. Merge similar tags into a single unified tag (e.g., "Jobseekers" and "Job Hunting" → "Job Search").
    2. Each tag should use Title Case.
    3. Return a JSON object mapping original tags to unified tags (e.g., {"Jobseekers": "Job Search", "Motivation": "Motivation"}).
    4. No preamble.

    Tags:
    {tags}
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke(input={"tags": unique_tags_list})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except OutputParserException as e:
        print(f"Error parsing unified tags: {e}")
        return {tag: tag for tag in unique_tags}  # Return tags unchanged if parsing fails


if __name__ == "__main__":
    processed_posts = process_posts("data/raw_posts.json", "data/processed_posts.json")
    print(f"Processed {len(processed_posts)} posts successfully.")
