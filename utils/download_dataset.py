import asyncio
import os
import json
import httpx
# from services.comments import get_comment 

# Get a comment from Regulations.gov API 
async def get_comment(comment_id):
    regulations_api_key = "fUhDOvth3SkvSvVWLym8oJfQHc5CKbHqv92gPanf"
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={regulations_api_key}"
        response = await client.get(comment_api)
        return response
    

# Initialize database file
db_file = "/Users/peace/Developer/Machine Learning/Research/mscc/database/database.json"

async def download(db_file):
    # def download()
    if os.path.exists(db_file):
        with open(db_file, 'r') as file:
            # Load JSON content
            data = json.load(file)

            # Load comment content
            for i in range(1, 10371):
                comment_id = f"{i:04d}"
                print("ID ", comment_id)

                # Fetch comment data
                response = await get_comment("COLC-2023-0006-"+comment_id)

                # Check if the comment id exist
                if response.status_code != 200 : 
                    print(f"Kipped! Comment ID {comment_id}  Not Found\n")
                    continue

                # Load the comment object to JSON file
                comment_object = response.json()

                # Add the new object to the existing data
                data.append(comment_object)
            
        # Write the updated data back to the JSON file
        with open(db_file, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print(f"Error: File not found {db_file}")
        
asyncio.run(download(db_file))