import pandas as pd

# Load the original file
past_boxes_merchandise_df = pd.read_csv('past-boxes-merchandise.csv')

# List to hold rows for the transformed DataFrame
output_rows = []

# Iterate over rows of the original dataframe
for index, row in past_boxes_merchandise_df.iterrows():
    # Extract key identifiers
    handle = row['handle']
    title = row['Product Title']

    # Add each field as a new row in the output
    fields = {
        'title': row['Title'],
        'content': row['Content'],
        'usp_title_1': row['USP Title 1'],
        'usp_image_1': row['USP Image 1'],
        'usp_title_2': row['USP Title 2'],
        'usp_image_2': row['USP Image 2'],
        'usp_title_3': row['USP Title 3'],
        'usp_image_3': row['USP Image 3'],
        'usp_title_4': row['USP Title 4'],
        'usp_image_4': row['USP Image 4'],
        'usp_title_5': row['USP Title 5'],
        'usp_image_5': row['USP Image 5']
    }

    # Append rows for each field
    for field, value in fields.items():
        output_rows.append({
            'Handle': handle,
            'Command': 'MERGE',
            'Definition: Handle': 'merchandise',
            'Definition: Name': 'Merchandise',
            'Field': field,
            'Value': value
        })

# Convert the transformed data into a DataFrame
transformed_df = pd.DataFrame(output_rows)

# Save the transformed data to a new file
output_file_path = 'parsed_past_boxes_metaobject_data.csv'
transformed_df.to_csv(output_file_path, index=False)

print(f"Transformed data has been saved to {output_file_path}")
