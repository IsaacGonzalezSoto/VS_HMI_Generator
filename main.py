import csv
from lxml import etree

class XMLModifier:
    def __init__(self, template_file: str, group_template_file: str):
        # Load the XML file
        self.tree = etree.parse(template_file)
        self.root = self.tree.getroot()

        # Load the cylinder group template from a text file
        with open(group_template_file, 'r') as f:
            self.group_template = f.read()

        # Clean existing groups from the template before adding new ones
        self.clean_existing_groups()

    def clean_existing_groups(self):
        # Find all direct child <group> elements and remove them from the root
        for group in list(self.root):
            if group.tag == 'group':  # Ensure we are removing only <group> tags
                self.root.remove(group)
        print("Cleaned all existing <group> elements from the template.")

    def create_cylinder_group(self, data, idx):
        # Dynamically format the template with the appropriate data from CSV
        group_content = self.group_template.format(idx, *data)

        # Parse the group content into XML format
        return etree.fromstring(group_content)

    def append_group(self, group_node):
        # Append the group node to the root level
        self.root.append(group_node)  # Append to the root node
        print(f"Appended new group {group_node.get('name')}")

    def save(self, output_file: str):
        # Save the modified XML to a new file
        self.tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

class CSVReader:
    @staticmethod
    def read_csv(file_path: str) -> list:
        # Read the CSV file and return rows with captions and expressions
        captions = []
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                captions.append(row)  # Append all CSV columns
        return captions

if __name__ == "__main__":
    xml_file = 'IO Status Cylinder Template.xml'  # The XML template file name
    csv_file = 'captions.csv'  # The CSV file name
    output_file = 'updated_hmi_file.xml'  # Output file to save changes
    group_template_file = 'cylinder_template.xml'  # The group template text file

    # Load the XML modifier and CSV reader
    xml_modifier = XMLModifier(xml_file, group_template_file)
    csv_reader = CSVReader()

    # Read the CSV file
    caption_rows = csv_reader.read_csv(csv_file)

    # Ensure we have multiple groups and are processing each properly
    for idx, row in enumerate(caption_rows, start=1):
        print(f"Processing cylinder group {idx}")
        print(f"Data for group {idx}: {row}")
        new_group = xml_modifier.create_cylinder_group(row, idx)
        xml_modifier.append_group(new_group)

    # Save the updated XML to a new file
    xml_modifier.save(output_file)
    print(f"Updated XML with multiple cylinders saved to {output_file}")
