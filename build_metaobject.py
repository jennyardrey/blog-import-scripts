import pandas as pd
import re
from bs4 import BeautifulSoup
from bs4.element import Tag

# Load the blog import file
blog_df = pd.read_excel('updated_blog_import.xlsx')

# List to hold rows for the final output DataFrame
output_rows = []

# Fixed values for Information Box Color, Font Color, Command, Status, and Definitions
info_box_color = "#fada4a"
info_box_font_color = "#1c1c1c"
cta_style = "btn btn--tertiary"
command_value = "MERGE"
status_value = "active"
definition_handle = "past_box"
definition_name = "Past Box"

# Helper function to clean HTML tags
def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text()

# Process each row in the blog_df
for index, row in blog_df.iterrows():
    # Generate the handle from the Title column, converting to lowercase and replacing spaces with dashes
    handle = row['Title'].strip().lower().replace(" ", "-") if pd.notna(row['Title']) else f"object_{index+1}"

    # Upper Description
    upper_description = clean_html(row['Excerpt']) if pd.notna(row['Excerpt']) else ''

    # Extract USPs from <ul><li> elements in text_content
    text_content = row['text_content'] if pd.notna(row['text_content']) else ''
    soup = BeautifulSoup(text_content, "html.parser")
    usps = [clean_html(li.get_text()) for li in soup.select("ul li")]
    usp_values = {f"USP{i+1}": usps[i] if i < len(usps) else '' for i in range(5)}

    # Lower Description - get all text after </ul> including any inline elements
    lower_description = ''
    ul_tag = soup.find("ul")

    if ul_tag:
        # Get all content until the next block element
        content_parts = []
        current_node = ul_tag.next_sibling

        while current_node and not (
            isinstance(current_node, Tag) and
            current_node.name in ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol']
        ):
            if isinstance(current_node, (str, Tag)):
                # If it's a span, get its full content including any nested tags
                if isinstance(current_node, Tag) and current_node.name == 'span':
                    content_parts.append(str(current_node))
                else:
                    content_parts.append(str(current_node))
            current_node = current_node.next_sibling

        if content_parts:
            # Join all parts and parse as HTML to properly handle nested elements
            combined_content = ''.join(content_parts)
            content_soup = BeautifulSoup(combined_content, "html.parser")
            lower_description = content_soup.get_text().strip()

    # Debug prints for Lower Description
    print("\nDEBUG - Lower Description:")
    print(f"Found ul tag: {ul_tag is not None}")
    print(f"Raw content parts: {content_parts}")
    print(f"Combined content: {combined_content if 'combined_content' in locals() else 'None'}")
    print(f"Final lower description: {lower_description}")

    # Information Box Content - get content after h2 until first link or empty line
    info_box_title = ''
    info_box_content = ''
    h2_tag = soup.find("h2", class_="h3")

    if h2_tag:
        info_box_title = clean_html(h2_tag.get_text())

        # Get all content up to the first <a> tag
        content_parts = []
        current_node = h2_tag.next_sibling

        while current_node and not (
            isinstance(current_node, Tag) and
            (current_node.name == 'a' or current_node.name == 'p')
        ):
            if isinstance(current_node, (str, Tag)):
                content_parts.append(str(current_node))
            current_node = current_node.next_sibling

        if content_parts:
            combined_content = ''.join(content_parts)
            content_soup = BeautifulSoup(combined_content, "html.parser")
            info_box_content = content_soup.get_text().strip()

    # Debug prints for Information Box
    print("\nDEBUG - Information Box:")
    print(f"Raw content parts: {content_parts}")
    print(f"Final info box content: {info_box_content}")

    # Print relevant HTML structure
    print("\nRelevant HTML structure:")
    if h2_tag:
        print(str(h2_tag.parent)[:500])  # Print first 500 chars of parent div

    # CTA URL
    cta_url = ''
    cta_button = soup.find("a", class_="button white")
    if cta_button and 'href' in cta_button.attrs:
        cta_url = cta_button['href']

    # Add each field and value pair for this object to the output
    fields = {
        'Upper Description': upper_description,
        **usp_values,
        'Lower Description': lower_description,
        'Information Box Color': info_box_color,
        'Information Box Font Color': info_box_font_color,
        'Information Box Title': info_box_title,
        'Information Box Content': info_box_content,
        'CTA Text': info_box_title,
        'CTA URL': cta_url,
        'CTA Style': cta_style
    }

    # Append each field/value pair as a new row in output_rows
    for field, value in fields.items():
        output_rows.append({
            'Handle': handle,
            'Command': command_value,
            'Status': status_value,
            'Definition: Handle': definition_handle,
            'Definition: Name': definition_name,
            'Field': field,
            'Value': value
        })

# Convert output_rows list to a DataFrame
output_df = pd.DataFrame(output_rows)

# Save to a new Excel file
output_file = 'processed_metaobjects_expanded-3.xlsx'
output_df.to_excel(output_file, index=False)
print(f"New metaobjects file created: {output_file}")
