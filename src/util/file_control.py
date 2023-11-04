import re
import os
import csv
import json
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

class FileControl:

    @staticmethod
    def make_regex_pattern(table, column, size, prints=False):
        p = "(" + table + r"""[\r\n\t\s\w(),\[\]\/<>"'@=.]+Name=""" + "\"" + column + "\"" + r"""\sType="nvarchar"\sSize=")""" + size
        if prints:
            print(p)
        return p

    @staticmethod
    def filter_files(rootdir, filter_pattern):
        flt = re.compile(filter_pattern)
        filtered_files = []
        for root, dirs, files in os.walk(rootdir):

            for file in files:
                searched_file = f"{root}\\{file}"

                if flt.search(searched_file) == None:
                    continue

                filtered_files.append(searched_file)
                print(searched_file)
                # return filtered_files

        return filtered_files

    @staticmethod
    def replace_strings_in_files(find_what_pattern, file_paths, replace_with, test_mode=False):
        fw = re.compile(find_what_pattern)

        for file_path in file_paths:

            # Replace
            try:
                # In case of exception that the process tries to read invalid start byte
                with open(file_path, "rt", encoding="utf-8") as fin:
                    data = fin.read()

                    match = re.search(find_what_pattern, data)
                    if match == None:
                        continue

                    # Replace strings
                    # This makes the file readable/writable for the owner
                    os.chmod(file_path, S_IWUSR | S_IREAD)
                    data = fw.sub(match.group(1) + replace_with, data)

                    if test_mode == True:
                        continue

                    with open(file_path, "wt", encoding="utf-8") as fout:
                        fout.write(data)

            except Exception as e:
                print(e)
                print(f"{file_path} can't be read.")

        @staticmethod
        def replace_in_file(file_path, compiled_regex_patten: re.Match, replace_with, test_mode=False):
            # Read
            data = ""
            try:  # In case of exception that the process tries to read invalid start byte
                with open(file_path, "rt", encoding="utf-8") as fin:
                    data = fin.read()

            except Exception as e:
                print(e)
                print(f"{file_path} can't be read.")

            # Replace
            # This makes the file readable/writable for the owner
            os.chmod(file_path, S_IWUSR | S_IREAD)
            new_data = compiled_regex_patten.sub(replace_with, data)

            if test_mode:
                return

            # Write
            with open(file_path, "wt", encoding="utf-8") as fout:
                fout.write(new_data)

    @staticmethod
    def read_text_file(file_path):
        # Using readline()
        with open(file_path, 'r') as f:
            count = 0
            lines = []
            while True:
                count += 1

                # Get next line from file
                line = f.readline()

                # if line is empty
                # end of file is reached
                if not line:
                    break
                lines.append(line.strip())
        return lines

    @staticmethod
    def create_csv(columns, file_name="sample"):
        with open(f'{file_name}.csv', mode='w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(columns)

    @staticmethod
    def convert_csv_to_json(csv_file_path):
        # get a csv file name
        pattern = r"\\*([\w\d].+\.)csv$"
        match = re.search(pattern, csv_file_path)
        json_file_path = match.group(1) + "json" if match != None else "sample.json"

        # convert the csv file to a json
        data = {}
        with open(csv_file_path, encoding='utf-8') as csvf:
            csv_reader = csv.DictReader(csvf)

            line_count = 0
            for row in csv_reader:

                data[str(line_count)] = row
                line_count += 1

        with open(json_file_path, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

    @staticmethod
    def get_json_file(json_file_path):
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            return data

    @staticmethod
    def write_text_file(path, lines):
        with open(f'{path}.txt', mode='w') as txtfile:
            txtfile.write('\n'.join(lines) + '\n')

    @staticmethod
    def contains(text, pattern="", compiled_pattern=None):
        if compiled_pattern == None:
            compiled_pattern = re.compile(pattern)

        result = compiled_pattern.search(text)
        return (result != None)

    @staticmethod
    def find_with_multiple_regex_patterns(text, patterns):
        for p in patterns:
            contains = (re.search(p, text) != None)
            if contains:
                return True

        return False