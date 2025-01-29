import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        """Initialize the class by loading and processing posts."""
        self.df = None
        self.unique_tags = set()
        self.load_posts(file_path)

    def load_posts(self, file_path):
        """Loads and processes posts from a JSON file."""
        try:
            with open(file_path, encoding="utf-8") as file:
                posts = json.load(file)

            # Normalize JSON data into a DataFrame
            self.df = pd.json_normalize(posts)

            # Add a 'length' column based on line counts
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)

            # Collect unique tags
            self.df["tags"] = self.df["tags"].apply(lambda x: x if isinstance(x, list) else [])
            self.unique_tags = set(tag for tags in self.df["tags"] for tag in tags)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading posts: {e}")

    def get_filtered_posts(self, length, language, tag):
        """
        Filters posts based on the provided length, language, and tag.
        
        Args:
            length (str): "Short", "Medium", or "Long".
            language (str): Language of the post (e.g., "English" or "Hinglish").
            tag (str): Tag to filter posts by.

        Returns:
            list: Filtered posts as dictionaries.
        """
        filtered_df = self.df[
            (self.df["tags"].apply(lambda tags: tag in tags)) & 
            (self.df["language"] == language) & 
            (self.df["length"] == length)
        ]
        return filtered_df.to_dict(orient="records")

    @staticmethod
    def categorize_length(line_count):
        """
        Categorizes the length of a post based on line count.
        
        Args:
            line_count (int): Number of lines in the post.

        Returns:
            str: "Short", "Medium", or "Long".
        """
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        """
        Retrieves all unique tags from the dataset.

        Returns:
            list: A sorted list of unique tags.
        """
        return sorted(self.unique_tags)


if __name__ == "__main__":
    # Example usage
    try:
        fs = FewShotPosts(file_path="data/processed_posts.json")
        print("Available Tags:", fs.get_tags())
        posts = fs.get_filtered_posts(length="Medium", language="Hinglish", tag="Job Search")
        print("Filtered Posts:", posts)
    except Exception as e:
        print(f"An error occurred: {e}")
