import os

for root, _, files in os.walk(r'd:\My Projects\ExpenseAI'):
    for file in files:
        if file.endswith('.html') or file.endswith('.py') or file.endswith('.css') or file.endswith('.md'):
            if 'venv' in root or '.git' in root or '__pycache__' in root:
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace Vyra with Vyra
            new_content = content.replace('Vyra', 'Vyra')
            new_content = new_content.replace('Vyra', 'Vyra')
            new_content = new_content.replace('Vyra', 'Vyra')
            new_content = new_content.replace('Smart Personal Wealth Management Platform', 'Smart Personal Wealth Management Platform')
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {path}")
