import json
import os
import shutil
import argparse

def fix_coco_file(path, contributor="Unknown", categories=None):
    """
    Fixes a COCO-style annotation file by:
    - Adding an 'info' field if missing
    - Optionally adding a 'categories' field if categories list is provided
    - Backing up the original file with `_old.json` suffix

    Args:
        path (str): Path to the original JSON file.
        contributor (str): Name of the dataset contributor.
        categories (list[dict] or None): COCO categories to insert, or None to skip.
    """
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    old_path = os.path.join(dirname, filename.replace(".json", "_old.json"))
    fixed_path = path
    
    # Load the JSON first to check if 'info' exists
    with open(path, 'r') as f:
        data = json.load(f)

    if 'info' in data:
        print("Nothing to fix: 'info' field already exists.")
        return
        
    # Backup the original file
    shutil.move(path, old_path)
    print(f"🔁 Renamed {filename} → {os.path.basename(old_path)}")

    # Load content
    with open(old_path, 'r') as f:
        data = json.load(f)

    # Add 'info' field if missing
    if 'info' not in data:
        data['info'] = {
            "description": f"{filename.replace('.json', '').capitalize()} set",
            "version": "1.0",
            "year": 2025,
            "contributor": contributor,
            "date_created": "2025-06-14"
        }

    # Add 'categories' only if user provides them
    if categories and isinstance(categories, list):
        data['categories'] = categories

    # Save the fixed JSON
    with open(fixed_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Fixed and saved: {filename}\n")


def main():
    parser = argparse.ArgumentParser(description="Fix a COCO-style JSON annotation file.")
    parser.add_argument("path", help="Path to the COCO JSON file.")
    parser.add_argument("--contributor", default="Unknown", help="Name of the dataset contributor.")
    parser.add_argument("--categories", type=str, default=None,
                        help="Path to JSON file containing a list of COCO categories.")

    args = parser.parse_args()

    categories = None
    if args.categories:
        with open(args.categories, 'r') as f:
            categories = json.load(f)

    fix_coco_file(args.path, contributor=args.contributor, categories=categories)

if __name__ == "__main__":
    main()