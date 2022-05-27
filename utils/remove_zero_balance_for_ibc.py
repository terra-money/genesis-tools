import csv
import os.path

cur_path = os.path.abspath(os.path.dirname(__file__))


def remove_zero_balance(name: str):
    pre_attack_path = os.path.join(cur_path, '../src/ibc/pre_attack_' + name + '.csv')
    pre_attack_without_zero_path = os.path.join(cur_path, '../src/ibc/pre_attack_without_zero_balance_' + name + '.csv')
    imp = open(pre_attack_path, newline='')
    out = open(pre_attack_without_zero_path, 'w')
    csv_writer = csv.writer(out)

    lines = csv.reader(imp, delimiter=',')
    header = next(lines)
    csv_writer.writerow(header)
    for row in lines:
        amount = int(float(row[3]) * 1_000_000)
        if amount != 0:
            csv_writer.writerow(row)
    imp.close()
    out.close()

    post_attack_path = os.path.join(cur_path, '../src/ibc/post_attack_' + name + '.csv')
    post_attack_without_zero_path = os.path.join(cur_path, '../src/ibc/post_attack_without_zero_balance_' + name + '.csv')
    imp = open(post_attack_path, newline='')
    out = open(post_attack_without_zero_path, 'w')
    csv_writer = csv.writer(out)

    lines = csv.reader(imp, delimiter=',')
    header = next(lines)
    csv_writer.writerow(header)
    for row in lines:
        amount = int(float(row[3]) * 1_000_000)
        if amount != 0:
            csv_writer.writerow(row)
    imp.close()
    out.close()

if __name__ == '__main__':
    remove_zero_balance('osmo')
    remove_zero_balance('crescent')
    remove_zero_balance('sifchain')
    