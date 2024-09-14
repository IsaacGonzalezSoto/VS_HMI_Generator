from typing import List, Dict
import openpyxl
from lxml import etree


class XMLModifier:
    """
    A class to handle modifications to an XML file. It specifically focuses on adding groups
    based on a template and removing existing groups before inserting new ones.
    """

    def __init__(self, template_file: str):
        """
        Initializes the XMLModifier class by loading an XML template.

        :param template_file: Path to the XML template file.
        """
        self.tree = etree.parse(template_file)
        self.root = self.tree.getroot()
        self.clean_existing_groups()

    def clean_existing_groups(self) -> None:
        """
        Removes all <group> elements from the root of the XML template.
        """
        groups_to_remove = [group for group in list(self.root) if group.tag == 'group']
        for group in groups_to_remove:
            self.root.remove(group)
        print("Cleaned all existing <group> elements from the template.")

    def create_cylinder_group(self, data: Dict[str, str], idx: int) -> etree.Element:
        """
        Creates a new cylinder group XML node based on the data provided.

        :param data: A dictionary with the Excel data (one row) where keys are column headers.
        :param idx: Index of the current group (used for unique identification).
        :return: A new XML Element representing the cylinder group.
        """
        # Print the keys for debugging (optional)
        print(f"Keys in data: {data.keys()}")

        # Ensure the data dictionary has the required keys from the Excel file
        data = {key: data.get(key, '') for key in [
            'Caption for Text Indicator (State 0)', 'Caption for Text Indicator (State 1)', 'Cylinder Label Text', 
            'Home Indicator State', 'Home Indicator Connection Expression', 
            'Work Indicator State', 'Work Indicator Connection Expression', 'Panel Visibility'
        ]}

        # Create the main group element for the cylinder
        group = etree.Element("group", name=f"Group36_Cylinder_{idx}", visible="true", wallpaper="false", isReferenceObject="false")

        # Add the Cyl_Error panel
        panel = etree.SubElement(group, "panel", name=f"Cyl_Error{idx}", height="80", width="96", left="317", top="140", visible="true", 
                                isReferenceObject="false", backStyle="solid", patternStyle="none", backColor="red", patternColor="white", 
                                blink="false", description="", borderColor="red", borderStyle="raisedInset", borderWidth="5", 
                                borderUsesBackColor="true", endColor="white", gradientStop="50", gradientDirection="gradientDirectionHorizontal", 
                                gradientShadingStyle="gradientHorizontalFromRight")

        # Add animations for error visibility
        error_expression = data.get('Panel Visibility', '')  
        animations = etree.SubElement(panel, "animations")
        etree.SubElement(animations, "animateVisibility", expression=error_expression, expressionTrueState="visible")

        # Create the indicators group inside the main group
        indicators_group = etree.SubElement(group, "group", name=f"Cyl_Indicators{idx}", visible="true", isReferenceObject="false")
        
        ### Add the <text> element for Cylinder Label Text
        cyl_text_caption = data.get('Cylinder Label Text', 'CYL Text')  # Default caption if empty
        text_element = etree.SubElement(indicators_group, "text", name=f"Cyl_Text_Id{idx}", height="28", width="61", left="321", top="144",
                                    visible="true", isReferenceObject="false", backStyle="solid", backColor="blue", foreColor="white", 
                                    wordWrap="false", sizeToFit="true", alignment="middleLeft", fontFamily="Arial", charHeight="14", 
                                    charWidth="6", bold="false", italic="false", underline="false", strikethrough="false", 
                                    caption=cyl_text_caption)
        # Add the Text Indicator multistate element
        text_indicator = etree.SubElement(indicators_group, "multistateIndicator", name=f"Text_Indicator{idx}", height="20", width="80", 
                                        left="321", top="172", visible="true", isReferenceObject="false", backStyle="solid", 
                                        borderStyle="inset", borderUsesBackColor="true", borderWidth="2", description="", shape="rectangle", 
                                        triggerType="value", currentStateId="0", captionOnBorder="false", setLastStateId="2")

        # Add states to the text indicator
        states = etree.SubElement(text_indicator, "states")

        # State 0 (normal state) - from "Caption for Text Indicator (State 0)"
        state_0 = etree.SubElement(states, "state", stateId="0", value="0", backColor="black", borderColor="white", patternColor="white", 
                                patternStyle="none", blink="false", endColor="white", gradientStop="50", 
                                gradientDirection="gradientDirectionHorizontal", gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_0, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", underline="false", 
                        strikethrough="false", caption=data.get('Caption for Text Indicator (State 0)', ''), color="white", backColor="#3F3F3F", 
                        backStyle="transparent", alignment="middleCenter", wordWrap="true", blink="false")

        # State 1 - from "Caption for Text Indicator (State 1)"
        state_1 = etree.SubElement(states, "state", stateId="1", value="1", backColor="black", borderColor="white", patternColor="white", 
                                patternStyle="none", blink="false", endColor="white", gradientStop="50", 
                                gradientDirection="gradientDirectionHorizontal", gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_1, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", underline="false", 
                        strikethrough="false", caption=data.get('Caption for Text Indicator (State 1)', ''), color="white", backColor="navy", 
                        backStyle="transparent", alignment="middleCenter", wordWrap="true", blink="false")


        # Assign correct Home and Work indicator values
        home_caption = data.get('Home Indicator State', '')  # Correct Home data
        home_expression = data.get('Home Indicator Connection Expression', '')  # Correct Home expression
        work_caption = data.get('Work Indicator State', '')  # Correct Work data
        work_expression = data.get('Work Indicator Connection Expression', '')  # Correct Work expression

        # Home Indicator (on the left, green when active)
        home_indicator = etree.SubElement(indicators_group, "multistateIndicator", name=f"Home_Indicator{idx}", height="20", width="30", 
                                        left="321", top="193", visible="true", isReferenceObject="false", backStyle="solid", 
                                        borderStyle="inset", borderUsesBackColor="true", borderWidth="2", description="", shape="rectangle", 
                                        triggerType="value", currentStateId="1", captionOnBorder="false", setLastStateId="2")

        home_states = etree.SubElement(home_indicator, "states")

        # State 0 for Home Indicator (off - black)
        state_0_home = etree.SubElement(home_states, "state", stateId="0", value="0", backColor="black", borderColor="white", 
                                        patternColor="white", patternStyle="none", blink="false", endColor="white", 
                                        gradientStop="50", gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_0_home, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", 
                        underline="false", strikethrough="false", caption=home_caption, color="white", 
                        backColor="#3F3F3F", backStyle="transparent", alignment="middleCenter", wordWrap="true", blink="false")

        # State 1 for Home Indicator (on - green)
        state_1_home = etree.SubElement(home_states, "state", stateId="1", value="1", backColor="lime", borderColor="white", 
                                        patternColor="white", patternStyle="none", blink="false", endColor="white", 
                                        gradientStop="50", gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_1_home, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", 
                        underline="false", strikethrough="false", caption=home_caption, color="black", 
                        backColor="navy", backStyle="transparent", alignment="middleCenter", wordWrap="true", blink="false")

        # Add Home indicator connections
        home_connections = etree.SubElement(home_indicator, "connections")
        etree.SubElement(home_connections, "connection", name="Indicator", expression=home_expression)

        # Work Indicator (on the right, yellow when active)
        work_indicator = etree.SubElement(indicators_group, "multistateIndicator", name=f"Work_Indicator{idx}", height="20", width="30", 
                                        left="351", top="193", visible="true", isReferenceObject="false", backStyle="solid", 
                                        borderStyle="inset", borderUsesBackColor="true", borderWidth="2", description="", 
                                        shape="rectangle", triggerType="value", currentStateId="1", captionOnBorder="false", 
                                        setLastStateId="2")

        work_states = etree.SubElement(work_indicator, "states")

        # State 0 for Work Indicator (off - black)
        state_0_work = etree.SubElement(work_states, "state", stateId="0", value="0", backColor="black", borderColor="white", 
                                        patternColor="white", patternStyle="none", blink="false", endColor="white", 
                                        gradientStop="50", gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_0_work, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", 
                        underline="false", strikethrough="false", caption=work_caption, color="white", 
                        backColor="#3F3F3F", backStyle="transparent", alignment="middleCenter", wordWrap="true", blink="false")

        # State 1 for Work Indicator (on - yellow)
        state_1_work = etree.SubElement(work_states, "state", stateId="1", value="1", backColor="yellow", borderColor="white", 
                                        patternColor="white", patternStyle="none", blink="false", endColor="white", 
                                        gradientStop="50", gradientDirection="gradientDirectionHorizontal", 
                                        gradientShadingStyle="gradientHorizontalFromRight")
        etree.SubElement(state_1_work, "caption", fontFamily="Arial", fontSize="9", bold="true", italic="false", 
                        underline="false", strikethrough="false", caption=work_caption, color="black", 
                        backColor="navy", backStyle="transparent", alignment="middleCenter", wordWrap="true", blink="false")

        # Add Work indicator connections
        work_connections = etree.SubElement(work_indicator, "connections")
        etree.SubElement(work_connections, "connection", name="Indicator", expression=work_expression)

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
        Saves the modified XML document to a specified file.

        :param output_file: Path to the output file where the updated XML will be saved.
        """
        self.tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"Saved updated XML to {output_file}")


class ExcelReader:
    """
    A class to handle reading of Excel files.
    """

    @staticmethod
    def read_excel(file_path: str) -> List[Dict[str, str]]:
        """
        Reads an Excel file and returns its content as a list of dictionaries.

        :param file_path: Path to the Excel file.
        :return: A list of dictionaries, each representing a row in the Excel file.
        """
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        data = []
        headers = [cell.value for cell in sheet[1]]  # Read header row
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {headers[i]: row[i] for i in range(len(headers))}
            data.append(row_data)
        print(f"Read {len(data)} rows from the Excel file.")
        return data


if __name__ == "__main__":
    # Paths to files
    xml_file = 'IO_Status_Cylinder_Template.xml'  # XML template file name
    excel_file = 'captions.xlsx'  # Excel file name containing data
    output_file = 'updated_hmi_file.xml'  # Output file to save the modified XML

    # Create instances of necessary classes
    xml_modifier = XMLModifier(xml_file)
    excel_reader = ExcelReader()

    # Read data from Excel
    caption_rows = excel_reader.read_excel(excel_file)

    # Loop through each Excel row and create/append the corresponding group
    for idx, row in enumerate(caption_rows, start=1):
        print(f"Processing cylinder group {idx}")
        new_group = xml_modifier.create_cylinder_group(row, idx)
        xml_modifier.append_group(new_group)

    # Save the final XML to a file
    xml_modifier.save(output_file)
