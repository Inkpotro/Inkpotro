# Import the 'join' function to create file paths in a platform-independent way
from os.path import join

# Service class for handling Markdown-related operations
class MarkdownService:
    @staticmethod
    def save_post(data: dict, folder: str):
        # Build the YAML frontmatter section using the provided post metadata
        frontmatter = f"""---
cover:
  image: {data['cover_image']}
  alt: {data['cover_alt']}
  relative: false
title: '{data['title']}'
author: '{data['author']}'
date: {data['date']}
tags:
""" + ''.join([f"  - {tag}\n" for tag in data["tags"]]) + f"""draft: {str(data["draft"]).lower()}
categories:
""" + ''.join([f"  - {cat}\n" for cat in data["categories"]]) + "---\n\n"

        # Combine frontmatter with post content
        markdown_content = frontmatter + data["content"]

        # Generate a filename by converting title to lowercase and replacing spaces with underscores
        filename = data["title"].lower().replace(" ", "_") + ".md"

        # Create the full file path using the selected folder and generated filename
        filepath = join(folder, filename)

        # Open the file in write mode with UTF-8 encoding and save the complete markdown content
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(markdown_content)