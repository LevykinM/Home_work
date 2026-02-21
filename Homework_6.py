import json

purchases = {}

with open('purchase_log.txt', 'r', encoding='utf-8') as p_file:
    next(p_file)

    for line in p_file:
        line = line.strip()
        if not line:
            continue

        data = json.loads(line)
        purchases[data['user_id']] = data['category']

with open('visit_log.csv', 'r', encoding='utf-8') as v_file, \
     open('funnel.csv', 'w', encoding='utf-8') as f_file:

    f_file.write('user_id,source,category\n')
    next(v_file)

    for line in v_file:
        user_id, source = line.strip().split(',')

        if user_id in purchases:
            category = purchases[user_id]
            f_file.write(f'{user_id},{source},{category}\n')