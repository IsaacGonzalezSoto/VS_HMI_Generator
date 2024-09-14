# HMI Cylinder Status Generator

This project automates the generation of HMI (Human-Machine Interface) status indicators for cylinders. It reads configuration data from an Excel file and generates an XML structure that includes error panels and multistate indicators for home and work statuses.


![image](https://github.com/user-attachments/assets/1c642fb3-110f-471c-8ac7-e3418960c2aa)

## Features

- **Excel-Based Configuration**: Easily configure HMI cylinder status from an Excel sheet.
- **Automated XML Generation**: Generates the necessary XML structure for HMI applications.
- **Multiple Indicators**: Creates panels for error indicators, as well as multistate indicators for home and work statuses.
- **Customizable**: Modify the Excel sheet to generate unique XML groups and indicators for each cylinder.


![image](https://github.com/user-attachments/assets/139c7462-c20d-48a0-80b1-93022928847c)








## Prerequisites

- Python 3.6 or higher
- The following Python packages:
  - `openpyxl` for reading Excel files
  - `lxml` for XML generation

You can install them using:

```bash
pip install openpyxl lxml
