import re

def extract(text):
    try:
        text = text.lower()
        tags = re.findall(r"(?:#)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)", text)
        return tags
    except Exception as e:
        print(e.__class__)
        return []
    
    
def assign_tags(post):
    tags = extract(post.content)
    print(tags)
    for tag in tags:
        tag = tag.lstrip("#")
        post.tags.add(tag)
    
def update_tags(post, old_content):
    previous_tags = extract(old_content)
    current_tags = extract(post.content)
    diff = list(set(previous_tags) ^ set(current_tags))
    old_tags, new_tags = [], []
    for x in diff:
        if x in previous_tags:
            old_tags.append(x) 
        else:
            new_tags.append(x)
    for t in old_tags:
        post.tags.remove(t)
    for t in new_tags:
        post.tags.add(t)
    
    