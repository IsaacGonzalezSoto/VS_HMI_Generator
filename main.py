
import csv
from typing import List
from lxml import etree

class XMLModifier:
    """
    A class to handle modifications to an XML file. It focuses on adding groups based on dynamic
    generation and removing existing groups before inserting new ones.
    """

    def __init__(self, template_file: str):
        """
        Initializes the XMLModifier class by loading an XML template.

        :param template_file: Path to the XML template file.
        """
        # Load the XML file and get the root element
        self.tree = etree.parse(template_file)
        self.root = self.tree.getroot()
        
        # Clean existing groups from the template before adding new ones
        self.clean_existing_groups()

    def clean_existing_groups(self) -> None:
        """
        Removes all <group> elements from the root of the XML template.
        """
        groups_to_remove = [group for group in list(self.root) if group.tag == 'group']
        for group in groups_to_remove:
            self.root.remove(group)
        print("Cleaned all existing <group> elements from the template.")

    def create_cylinder_group(self, data: List[str], idx: int) -> etree.Element:
        """
        Creates a new cylinder group XML node based on the provided data.

        :param data: List of data values from a CSV row.
        :param idx: Index of the current group (used for unique identification).
        :return: A new XML Element representing the cylinder group.
        """
        # Create the main group element for the cylinder
        group = etree.Element("group", name=f"Group36_Cylinder_{idx}", visible="true", wallpaper="false", isReferenceObject="false")

        # Create the panel element
        panel = etree.SubElement(group, "panel", name=f"Cyl_Error{idx}", height="80", width="96", left="317", top="140",
                                 visible="true", isReferenceObject="false", backStyle="solid", patternStyle="none", 
                                 backColor="red", patternColor="white", blink="false", description="", borderColor="red", 
                                 borderStyle="raisedInset", borderWidth="5", borderUsesBackColor="true", endColor="white", 
                                 gradientStop="50", gradientDirection="gradientDirectionHorizontal", 
                                 gradientShadingStyle="gradientHorizontalFromRight")

        # Add animations to the panel
        animations = etree.SubElement(panel, "animations")
        etree.SubElement(animations, "animateVisibility", expression=data[4], expressionTrueState="visible")

        # Create a sub-group for indicators
        indicators_group = etree.SubElement(group, "group", name=f"Cyl_Indicators{idx}", visible="true", isReferenceObject="false")

        # Create the Text Indicator multistate element
        text_indicator = etree.SubElement(indicators_group, "multistateIndicator", name=f"Text_Indicator{idx}",
                                          height="20", width="80", left="321", top="172", visible="true", isReferenceObject="false",
                                          backStyle="solid", borderStyle="inset", borderUsesBackColor="true", borderWidth="2", 
                                          description="", shape="rectangle", triggerType="value", currentStateId="0", captionOnBorder="false",
                                          setLastStateId="2")

        # Add states to the Text Indicator
        states = etree.SubElement(text_indicator, "states")
        state_error = etree.SubElement(states, "state", stateId="Error", backColor="red", borderColor="white", patternColor="white",
                                       patternStyle="none", blink="false", endColor="white", gradientStop="50", 
                                       gradientDirection="gradientDirectionHorizontal", gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_error, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", underline="false",
                         strikethrough="false", caption="", color="black", backColor="black", backStyle="transparent", 
                         alignment="middleCenter", wordWrap="true", blink="false")

        state_0 = etree.SubElement(states, "state", stateId="0", value="0", backColor="black", borderColor="white", 
                                   patternColor="white", patternStyle="none", blink="false", endColor="white", 
                                   gradientStop="50", gradientDirection="gradientDirectionHorizontal", gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_0, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", underline="false",
                         strikethrough="false", caption=data[0], color="white", backColor="#3F3F3F", backStyle="transparent", 
                         alignment="middleCenter", wordWrap="true", blink="false")

        state_1 = etree.SubElement(states, "state", stateId="1", value="1", backColor="black", borderColor="white", patternColor="white", 
                                   patternStyle="none", blink="false", endColor="white", gradientStop="50", 
                                   gradientDirection="gradientDirectionHorizontal", gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_1, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", underline="false", 
                         strikethrough="false", caption=data[1], color="white", backColor="navy", backStyle="transparent", 
                         alignment="middleCenter", wordWrap="true", blink="false")

        # Add the connection element
        connections = etree.SubElement(text_indicator, "connections")
        etree.SubElement(connections, "connection", name="Indicator", expression=data[4])

        # Create a Text element
        etree.SubElement(indicators_group, "text", name=f"Cyl_Text_Id{idx}", height="28", width="61", left="321", top="144", visible="true", 
                         isReferenceObject="false", backStyle="solid", backColor="blue", foreColor="white", wordWrap="false", 
                         sizeToFit="true", alignment="middleLeft", fontFamily="Arial", charHeight="14", charWidth="6", bold="false", 
                         italic="false", underline="false", strikethrough="false", caption=data[2])

        # Add the Home Indicator multistate element
        home_indicator = etree.SubElement(indicators_group, "multistateIndicator", name=f"Home_Indicator{idx}",
                                        height="20", width="30", left="351", top="193", visible="true", 
                                        isReferenceObject="false", backStyle="solid", borderStyle="inset", 
                                        borderUsesBackColor="true", borderWidth="2", description="", 
                                        shape="rectangle", triggerType="value", currentStateId="1", 
                                        captionOnBorder="false", setLastStateId="2")

        # Adding states for Home_Indicator
        home_states = etree.SubElement(home_indicator, "states")

        # State 0 with caption from column 4 (data[3])
        state_0_home = etree.SubElement(home_states, "state", stateId="0", value="0", backColor="black", 
                                        borderColor="white", patternColor="white", patternStyle="none", 
                                        blink="false", endColor="white", gradientStop="50", 
                                        gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")

        etree.SubElement(state_0_home, "caption", fontFamily="Arial", fontSize="9", bold="true", 
                        italic="false", underline="false", strikethrough="false", caption=data[3], 
                        color="white", backColor="#3F3F3F", backStyle="transparent", 
                        alignment="middleCenter", wordWrap="true", blink="false")

        # State 1 with the same caption from column 4 (data[3])
        state_1_home = etree.SubElement(home_states, "state", stateId="1", value="1", backColor="yellow", 
                                        borderColor="white", patternColor="white", patternStyle="none", 
                                        blink="false", endColor="white", gradientStop="50", 
                                        gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")

        etree.SubElement(state_1_home, "caption", fontFamily="Arial", fontSize="9", bold="true", 
                        italic="false", underline="false", strikethrough="false", caption=data[3], 
                        color="black", backColor="navy", backStyle="transparent", 
                        alignment="middleCenter", wordWrap="true", blink="false")

        # Adding the connection from column 5 (data[4])
        home_connections = etree.SubElement(home_indicator, "connections")
        etree.SubElement(home_connections, "connection", name="Indicator", expression=data[4])


        # Add the Work Indicator multistate element
        work_indicator = etree.SubElement(indicators_group, "multistateIndicator", name=f"Work_Indicator{idx}",
                                        height="20", width="30", left="321", top="193", visible="true", 
                                        isReferenceObject="false", backStyle="solid", borderStyle="inset", 
                                        borderUsesBackColor="true", borderWidth="2", description="", 
                                        shape="rectangle", triggerType="value", currentStateId="1", 
                                        captionOnBorder="false", setLastStateId="2")

        # Adding states for Work_Indicator
        work_states = etree.SubElement(work_indicator, "states")

        # State 0 with caption from column 6 (data[5])
        state_0_work = etree.SubElement(work_states, "state", stateId="0", value="0", backColor="black", 
                                        borderColor="white", patternColor="white", patternStyle="none", 
                                        blink="false", endColor="white", gradientStop="50", 
                                        gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")

        etree.SubElement(state_0_work, "caption", fontFamily="Arial", fontSize="9", bold="true", 
                        italic="false", underline="false", strikethrough="false", caption=data[5], 
                        color="white", backColor="#3F3F3F", backStyle="transparent", 
                        alignment="middleCenter", wordWrap="true", blink="false")

        # State 1 with the same caption from column 6 (data[5])
        state_1_work = etree.SubElement(work_states, "state", stateId="1", value="1", backColor="lime", 
                                        borderColor="white", patternColor="white", patternStyle="none", 
                                        blink="false", endColor="white", gradientStop="50", 
                                        gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")

        etree.SubElement(state_1_work, "caption", fontFamily="Arial", fontSize="9", bold="true", 
                        italic="false", underline="false", strikethrough="false", caption=data[5], 
                        color="black", backColor="navy", backStyle="transparent", 
                        alignment="middleCenter", wordWrap="true", blink="false")

        # Adding the connection from column 7 (data[6])
        work_connections = etree.SubElement(work_indicator, "connections")
        etree.SubElement(work_connections, "connection", name="Indicator", expression=data[6])


        # Return the constructed group element
        return group

    def append_group(self, group_node: etree.Element) -> None:
        """
        Appends a new group node to the root of the XML.

        :param group_node: The new group node to append.
        """
        self.root.append(group_node)
        print(f"Appended new group {group_node.get('name')}")

    def save(self, output_file: str) -> None:
        """
        Saves the modified XML document to a specified file with pretty printing enabled.

        :param output_file: Path to the output file where the updated XML will be saved.
        """
        with open(output_file, 'wb') as f:
            # Convert the XML tree to a string with pretty_print enabled
            xml_string = etree.tostring(self.root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
            f.write(xml_string)
        print(f"Saved updated XML with pretty printing to {output_file}")


class CSVReader:
    """
    A class to handle reading of CSV files.
    """

    @staticmethod
    def read_csv(file_path: str) -> List[List[str]]:
        """
        Reads a CSV file and returns its content as a list of rows, with each row represented as a list of strings.

        :param file_path: Path to the CSV file.
        :return: A list of rows, where each row is a list of strings from the CSV file.
        """
        data = []
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        print(f"Read {len(data)} rows from the CSV file.")
        return data


class CylinderGroupProcessor:
    """
    A class to process cylinder groups using the CSV data and XML modification functionalities.
    """

    def __init__(self, xml_modifier: XMLModifier, csv_reader: CSVReader, csv_file: str):
        """
        Initializes the CylinderGroupProcessor with instances of XMLModifier, CSVReader, and the path to the CSV file.

        :param xml_modifier: An instance of the XMLModifier class for handling XML modifications.
        :param csv_reader: An instance of the CSVReader class for reading CSV data.
        :param csv_file: Path to the CSV file containing cylinder group data.
        """
        self.xml_modifier = xml_modifier
        self.csv_reader = csv_reader
        self.csv_file = csv_file

    def process_groups(self) -> None:
        """
        Processes each row of the CSV file, creating and appending new groups to the XML document.
        """
        # Read CSV data
        caption_rows = self.csv_reader.read_csv(self.csv_file)

        # Loop through each CSV row and create/append the corresponding group
        for idx, row in enumerate(caption_rows, start=1):
            print(f"Processing cylinder group {idx}")
            print(f"Data for group {idx}: {row}")
            new_group = self.xml_modifier.create_cylinder_group(row, idx)
            self.xml_modifier.append_group(new_group)


if __name__ == "__main__":
    # Paths to files
    xml_file = 'IO_Status_Cylinder_Template.xml'  # XML template file name
    csv_file = 'captions.csv'  # CSV file name containing data
    output_file = 'updated_hmi_file.xml'  # Output file to save the modified XML

    # Create instances of necessary classes
    xml_modifier = XMLModifier(xml_file)
    csv_reader = CSVReader()

    # Create the processor and process cylinder groups
    group_processor = CylinderGroupProcessor(xml_modifier, csv_reader, csv_file)
    group_processor.process_groups()

    # Save the final XML to a file
    xml_modifier.save(output_file)
