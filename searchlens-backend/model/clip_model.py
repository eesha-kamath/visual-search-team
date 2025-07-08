import os
import io
import torch
import clip
import pandas as pd
from PIL import Image

# Initialize CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Path setup for Google Drive folder structure
BASE_DIR = "/content/drive/MyDrive/WalmartSparkathon"
CATEGORIES_CSV = os.path.join(BASE_DIR, "categories.csv")

def run_clip_on_image(image_bytes: bytes) -> dict:
    try:
        # Step 1: Load & preprocess image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_input = preprocess(image).unsqueeze(0).to(device)

        # Step 2: Load category prompts
        cat_df = pd.read_csv(CATEGORIES_CSV)
        categories = cat_df["category"].dropna().tolist()
        text_inputs = clip.tokenize(categories).to(device)

        # Step 3: Get category similarity
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            text_features = model.encode_text(text_inputs)

            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            similarities = (image_features @ text_features.T).squeeze(0)
            top_idx = similarities.argmax().item()
            top_category = categories[top_idx]

        # Step 4: Load attribute prompts
        attr_csv = os.path.join(BASE_DIR, f"{top_category.lower().replace(' ', '_')}_attributes.csv")
        raw_attr_df = pd.read_csv(attr_csv)

        # Step 5: Filter valid "facet: value" prompts only
        valid_rows = []
        for p in raw_attr_df['prompt']:
            if isinstance(p, str) and p.count(':') == 1:
                facet, value = p.split(':', 1)
                facet = facet.strip().lower()
                value = value.strip().lower()
                if facet and value:
                    valid_rows.append((p.strip(), facet, value))

        if not valid_rows:
            return {"error": "No valid attribute prompts found in the CSV."}

        attr_df = pd.DataFrame(valid_rows, columns=["prompt", "facet_name", "value"])

        # Remove unwanted keywords
        unwanted = ['sort', 'delivery', 'size', 'pickup', 'seller', 'price', 'best match', 'location', 'category', 'departments']
        attr_df = attr_df[~attr_df.apply(lambda row: any(k in row['facet_name'] or k in row['value'] for k in unwanted), axis=1)]
        attr_df = attr_df.drop_duplicates()

        attribute_prompts = attr_df["prompt"].tolist()

        # Step 6: Get top attribute matches
        attr_tokens = clip.tokenize(attribute_prompts).to(device)
        with torch.no_grad():
            attr_features = model.encode_text(attr_tokens)
            attr_features /= attr_features.norm(dim=-1, keepdim=True)
            scores = (image_features @ attr_features.T).squeeze(0)
            top_probs, top_idxs = scores.topk(4)

        top_attributes = [attribute_prompts[i] for i in top_idxs]

        return {
            "category": top_category,
            "attributes": top_attributes
        }

    except Exception as e:
        return {"error": str(e)}
