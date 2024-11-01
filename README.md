# Blog Content Update Scripts

This repository contains two Python scripts for processing and updating blog content with product information.

## Scripts Overview

### 1. update_blog_content.py

This script processes blog content and product data, merging them together to create updated content with proper product references.

#### Key Features:

- Reads blog content from Excel/CSV files
- Processes product data and matches it with blog content
- Updates placeholders in the content with actual product information
- Handles various text formats and HTML content
- Exports updated content to a new Excel file

#### Placeholders Handled:

- `[post_title]` - Replaced with blog post title
- `[linked_product field="title"]` - Replaced with product title
- `[linked_product field="type"]` - Replaced with product type
- `[linked_product field="link" class="..."]` - Replaced with HTML anchor tag
- `[post_date format="F Y"]` - Replaced with formatted date

### 2. build_metaobject.py

This script processes HTML content to extract specific components and structure them in a consistent format.

#### Key Features:

- Parses HTML content using BeautifulSoup4
- Extracts specific content sections:
  - Lower Description (text after bullet points)
  - Information Box Content (product information)
  - Information Box Title
  - CTA Text
- Handles various HTML structures including:
  - Nested elements
  - Inline HTML tags
  - Text nodes
  - Styled spans

## Requirements

bash
pip3 install pandas
pip3 install beautifulsoup4

## Usage

### Update Blog Content

```bash
python3 update_blog_content.py
```

### Build Meta Objects

```bash
python3 build_metaobject.py
```

## Content Processing Rules

### Lower Description

- Extracts text content after the closing `</ul>` tag
- Handles both plain text and HTML content
- Preserves text within anchor tags and spans
- Stops at the next block-level element

### Information Box Content

- Extracts content after `<h2>` tag
- Handles both loose text and paragraphs
- Preserves formatting while removing HTML tags
- Stops at the first link or empty line

## Edge Cases Handled

1. HTML Content:

   - Nested anchor tags
   - Styled spans
   - Mixed content (text nodes and HTML elements)
   - Various class attributes

2. Text Formatting:
   - Instagram handles in anchor tags
   - Product references
   - Dates in various formats
   - Special characters and spaces

## Output

The scripts generate:

1. Updated blog content with resolved placeholders
2. Structured meta object data
3. Clean text content with preserved formatting

## Debug Information

Both scripts include debug logging to help track:

- Content extraction progress
- HTML parsing results
- Text cleaning operations
- Final output formatting

## Maintenance

When making updates:

- Test against various HTML structures
- Verify placeholder replacements
- Check for regression in existing functionality
- Monitor debug output for unexpected behavior
  """
