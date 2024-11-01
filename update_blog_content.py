import pandas as pd
import re
from datetime import datetime

# Load the two spreadsheets into DataFrames
blog_df = pd.read_excel('blog-import.xlsx')
product_df = pd.read_excel('product-data.xlsx')

# After loading the DataFrames, convert product_df's product_id to integer first to remove decimals
product_df['product_id'] = product_df['product_id'].fillna('').astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)

# Initialize a list to log rows with missing or invalid product IDs
skipped_rows = []

# Function to extract the product ID from the `linked_product` column
def extract_product_id(linked_product, row_index):
    if isinstance(linked_product, str):  # Check if linked_product is a string
        match = re.search(r's:\d+:"(\d+)"', linked_product)
        if match:
            return match.group(1)
        else:
            # Log row if it does not match the expected format
            skipped_rows.append((row_index, linked_product, "No match found"))
            return None
    else:
        # Log row if linked_product is missing or not a string
        skipped_rows.append((row_index, linked_product, "Not a string or missing"))
        return None

# Apply extraction with logging for each row
blog_df['product_id'] = blog_df.apply(lambda row: extract_product_id(row['linked_product'], row.name), axis=1)

# Check the extracted product IDs
valid_product_ids = blog_df['product_id'].dropna().unique()
print("Extracted product IDs from blog_df:", valid_product_ids)

# Ensure `product_id` columns are both strings before merging
blog_df['product_id'] = blog_df['product_id'].astype(str)
product_df['product_id'] = product_df['product_id'].astype(str)

# Check product_ids in product_df
print("Product IDs in product_df:", product_df['product_id'].unique())

# Now, proceed with merging as before
merged_df = blog_df.merge(product_df, left_on='product_id', right_on='product_id', how='left')

# Debugging: Check merged DataFrame columns and sample rows
print("Merged DataFrame columns:", merged_df.columns.tolist())
print("Sample of merged DataFrame:")
print(merged_df[['Title', 'product_title', 'post_type', 'guid']].head(10))

# Define a function to replace placeholders in the `text_content` column
def replace_placeholders(text, post_title, product_title, post_type, link, post_date):
    # Convert all replacement values to strings, defaulting to empty string if NaN
    post_title = str(post_title) if pd.notna(post_title) else ''
    product_title = str(product_title) if pd.notna(product_title) else ''
    post_type = str(post_type) if pd.notna(post_type) else ''
    link = str(link) if pd.notna(link) else ''

    # Format the date if it exists
    if pd.notna(post_date):
        try:
            # Convert string to datetime object
            date_obj = pd.to_datetime(post_date)
            # Format as "Month Year"
            post_date = date_obj.strftime('%B %Y')
        except:
            post_date = ''
    else:
        post_date = ''

    # Replace placeholders with corresponding values
    text = text.replace('[post_title]', post_title)
    text = text.replace('[linked_product field="title"]', product_title)
    text = text.replace('[linked_product field="type"]', post_type)

    # Handle the link replacement with regex to capture any class variations
    if pd.notna(link):
        # Find all instances of the linked_product shortcode with link field
        link_patterns = re.finditer(r'\[linked_product field="link"([^]]*)\]', text)
        for match in link_patterns:
            shortcode = match.group(0)  # The full matched shortcode
            class_attr = match.group(1)  # The part that contains class="whatever"

            # Extract class value if it exists
            class_value = ''
            class_match = re.search(r'class="([^"]*)"', class_attr)
            if class_match:
                class_value = class_match.group(1)

            # Build the HTML anchor tag
            if class_value:
                html_link = f'<a href="{link}" class="{class_value}">{product_title}</a>'
            else:
                html_link = f'<a href="{link}">{product_title}</a>'

            # Replace this specific instance of the shortcode
            text = text.replace(shortcode, html_link)

    text = text.replace('[post_date format="F Y"]', post_date)
    return text

# Apply the replacement function to each row with error handling
def apply_replacements(row):
    try:
        return replace_placeholders(
            row['text_content'],
            row['Title'],
            row['product_title'],
            row['post_type'],
            row['guid'],
            row['Date']  # Add the Date field from blog_df
        )
    except Exception as e:
        print(f"Error processing row {row.name}: {e}")
        return row['text_content']  # Return original text if an error occurs

merged_df['text_content'] = merged_df.apply(apply_replacements, axis=1)

# Drop the helper 'product_id' column
merged_df = merged_df.drop(columns=['product_id'])

# Save the updated DataFrame to a new Excel file
output_file = 'updated_blog_import.xlsx'
merged_df.to_excel(output_file, index=False)

# Log any skipped rows
if skipped_rows:
    print("Rows with missing or invalid 'linked_product' values:")
    for row in skipped_rows:
        print(f"Row index: {row[0]}, Value: {row[1]}, Reason: {row[2]}")
else:
    print("All rows processed successfully.")

print(f"Updated blog content saved to {output_file}")
