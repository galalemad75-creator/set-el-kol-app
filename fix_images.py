#!/usr/bin/env python3
"""Fix duplicate images in set-el-kol-app fallback recipes."""

import re
import json
import urllib.request
import time

FILE = 'docs/index.html'

# Read the file
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all fallback recipes (between FALLBACK_RECIPES = [ and the closing ];)
# Find all strMealThumb entries and their surrounding context
pattern = r'(idMeal:"(fb\d+)",strMeal:"([^"]*)",strCategory:"([^"]*)",strArea:"[^"]*",\s*\n\s*strMealThumb:")([^"]*)(")'

matches = list(re.finditer(pattern, content))
print(f"Found {len(matches)} fallback recipes")

# Build image usage map
image_count = {}
for m in matches:
    img = m.group(5)
    image_count[img] = image_count.get(img, 0) + 1

print(f"\nDuplicate images:")
for img, count in sorted(image_count.items(), key=lambda x: -x[1]):
    if count > 1:
        print(f"  {count}x: {img.split('/')[-1]}")

# Fetch unique images per category from TheMealDB
def fetch_category_images(category):
    """Get unique images for a category from TheMealDB."""
    cat_map = {
        'Chicken': 'Chicken', 'Beef': 'Beef', 'Lamb': 'Lamb',
        'Seafood': 'Seafood', 'Dessert': 'Dessert', 'Pasta': 'Pasta',
        'Side': 'Side', 'Breakfast': 'Breakfast',
        'Miscellaneous': 'Miscellaneous', 'Vegetarian': 'Vegetarian',
        'Vegan': 'Vegan'
    }
    api_cat = cat_map.get(category, 'Miscellaneous')
    try:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={api_cat}"
        req = urllib.request.Request(url, headers={'User-Agent': 'SetElKol/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if data.get('meals'):
                return [m['strMealThumb'] for m in data['meals']]
    except Exception as e:
        print(f"  Error fetching {api_cat}: {e}")
    return []

# Get images for each category we need
categories_needed = set()
for m in matches:
    categories_needed.add(m.group(4))

print(f"\nFetching images for categories: {categories_needed}")
category_images = {}
for cat in categories_needed:
    imgs = fetch_category_images(cat)
    category_images[cat] = imgs
    print(f"  {cat}: {len(imgs)} images available")
    time.sleep(0.3)

# Track which images we've already used in replacements
used_images = set()
for m in matches:
    img = m.group(5)
    if image_count[img] == 1:  # unique images are already "used"
        used_images.add(img)

# Now fix duplicates
replacements = []
for m in matches:
    img = m.group(5)
    recipe_id = m.group(2)
    recipe_name = m.group(3)
    category = m.group(4)
    
    if image_count[img] > 1:  # This is a duplicate
        # Try to find a unique image from the same category
        found = False
        for candidate in category_images.get(category, []):
            if candidate not in used_images:
                replacements.append((recipe_id, recipe_name, img, candidate))
                used_images.add(candidate)
                found = True
                break
        
        if not found:
            # Try from any category
            for cat, imgs in category_images.items():
                for candidate in imgs:
                    if candidate not in used_images:
                        replacements.append((recipe_id, recipe_name, img, candidate))
                        used_images.add(candidate)
                        found = True
                        break
                if found:
                    break
        
        if not found:
            print(f"  WARNING: No unique image found for {recipe_name}")

print(f"\nReplacing {len(replacements)} duplicate images:")
for recipe_id, name, old, new in replacements:
    old_file = old.split('/')[-1]
    new_file = new.split('/')[-1]
    print(f"  {name}: {old_file} → {new_file}")

# Apply replacements
for recipe_id, name, old_img, new_img in replacements:
    # Replace the specific image for this recipe
    # Need to be careful to only replace the right one
    old_pattern = f'idMeal:"{recipe_id}",strMeal:"{name}",strCategory:'
    idx = content.find(old_pattern)
    if idx >= 0:
        # Find the strMealThumb after this
        thumb_start = content.find('strMealThumb:"', idx)
        if thumb_start >= 0:
            thumb_start += len('strMealThumb:"')
            thumb_end = content.find('"', thumb_start)
            if thumb_end >= 0:
                old_in_file = content[thumb_start:thumb_end]
                if old_in_file == old_img:
                    content = content[:thumb_start] + new_img + content[thumb_end:]
                    print(f"  ✓ Fixed: {name}")
                else:
                    print(f"  ✗ Mismatch for {name}: expected {old_img}, found {old_in_file}")

# Write back
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Done! File updated: {FILE}")

# Verify no more duplicates
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Count images in fallback section
fallback_start = content.find('FALLBACK_RECIPES')
fallback_end = content.find('];', fallback_start)
fallback_section = content[fallback_start:fallback_end]

imgs = re.findall(r'strMealThumb:"([^"]*)"', fallback_section)
img_counts = {}
for img in imgs:
    img_counts[img] = img_counts.get(img, 0) + 1

print(f"\nRemaining duplicates:")
dupes = [(c, img) for img, c in img_counts.items() if c > 1]
if dupes:
    for count, img in sorted(dupes, reverse=True):
        print(f"  {count}x: {img.split('/')[-1]}")
else:
    print("  None! All images are unique! 🎉")
