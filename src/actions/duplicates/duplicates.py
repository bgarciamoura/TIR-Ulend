def sum_duplicates(original_list, destination_list, key):
    index = 0
    date_key = 'created_at' if key == 'investments' else 'due_date'
    for item in original_list:
        previousItem = original_list[index - 1] if index - 1 < len(original_list) else None
        nextItem = original_list[index + 1] if index + 1 < len(original_list) else None
        if previousItem and item[date_key] == previousItem[date_key]:
            continue
        elif nextItem and item[date_key] == nextItem[date_key]:
            if key == 'installments':
              newItem = {
                  'investment_id': item['investment_id'],
                  'due_date': item['due_date'],
                  'amount': str(float(item['amount']) + float(nextItem['amount']))
              }
            else:
              newItem = {
                  'id': item['id'],
                  'created_at': item['created_at'],
                  'amount': str(float(item['amount']) + float(nextItem['amount']))
              }
            destination_list.append(newItem)
            index += 1
        else:
            destination_list.append(item)
        index += 1