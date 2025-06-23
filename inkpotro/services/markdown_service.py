# Import join function to safely create file paths
from os.path import join

# Service class to handle saving markdown blog posts with front matter
class MarkdownService:
    # This method can be called without creating an instance of the class
    @staticmethod
    def save_post(data: dict, folder: str):
        # Construct YAML front matter for the markdown post
        frontmatter = (
            "---\n"
            f"title: '{data['title']}'\n"
            f"date: {data['date']}\n"
            f"author: '{data['author']}'\n"
            f"draft: {str(data.get('draft', False)).lower()}\n"
            "tags:\n" +
            ''.join([f"  - {tag.strip()}\n" for tag in data["tags"]]) +
            "categories:\n" +
            ''.join([f"  - {cat.strip()}\n" for cat in data["categories"]]) +
            "---\n\n"
        )

        # Combine front matter and content
        markdown_content = frontmatter + data["content"]

        # Generate a file name by converting title to lowercase, replacing spaces with underscores, and adding .md extension
        filename = data["title"].strip().lower().replace(" ", "_") + ".md"

        # Create full file path by joining folder path with filename
        filepath = join(folder, filename)

        # Write the markdown content to the specified file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(markdown_content)