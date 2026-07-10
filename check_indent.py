with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    if '{% if ' in line:
        stack.append(('if', i+1))
        print(f"L{i+1}: {'  ' * len(stack)} if")
    elif '{% elif ' in line:
        print(f"L{i+1}: {'  ' * len(stack)} elif")
    elif '{% else %}' in line:
        print(f"L{i+1}: {'  ' * len(stack)} else")
    elif '{% endif %}' in line:
        print(f"L{i+1}: {'  ' * len(stack)} endif")
        if stack:
            stack.pop()
        else:
            print(f"ERROR: EXTRA ENDIF at L{i+1}")
    elif '{% with ' in line:
        stack.append(('with', i+1))
        print(f"L{i+1}: {'  ' * len(stack)} with")
    elif '{% endwith %}' in line:
        print(f"L{i+1}: {'  ' * len(stack)} endwith")
        if stack:
            stack.pop()
        else:
            print(f"ERROR: EXTRA ENDWITH at L{i+1}")

print("Remaining in stack:", stack)
