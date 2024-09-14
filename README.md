# HMI Cylinder Status Generator

This project automates the generation of HMI (Human-Machine Interface) status indicators for cylinders. It reads configuration data from an Excel file and generates an XML structure that includes error panels and multistate indicators for home and work statuses.


![image](https://github.com/user-attachments/assets/1c642fb3-110f-471c-8ac7-e3418960c2aa)

## Features

- **Excel-Based Configuration**: Easily configure HMI cylinder status from an Excel sheet.
- **Automated XML Generation**: Generates the necessary XML structure for HMI applications.
- **Multiple Indicators**: Creates panels for error indicators, as well as multistate indicators for home and work statuses.
- **Customizable**: Modify the Excel sheet to generate unique XML groups and indicators for each cylinder.

Caption for Text Indicator (State 0)	Caption for Text Indicator (State 1)	Cylinder Label Text	Home Indicator State	Home Indicator Connection Expression	Work Indicator State	Work Indicator Connection Expression	Panel Visibility
S01RVM1.I3	CYL 66BR	"CYL 66 BR 
10th CLAMP"	b66	{[CLx]S01_S04HMI1.O.Sta[4].InputStatus[2].10}	b67	{[CLx]S01_S04HMI1.O.Sta[4].InputStatus[2].11}	{[CLx]SxxStaAct[x].ErrCode.x}
S01RVM1.I4	CYL 88BR	"CYL 88 BR
12th CLAMP"	b86	{[CLx]S01_S04HMI1.O.Sta[4].InputStatus[2].13}	b87	{[CLx]S01_S04HMI1.O.Sta[4].InputStatus[2].11}	{[CLx]SxxStaAct[x].ErrCode.x}
![image](https://github.com/user-attachments/assets/139c7462-c20d-48a0-80b1-93022928847c)






## Prerequisites

- Python 3.6 or higher
- The following Python packages:
  - `openpyxl` for reading Excel files
  - `lxml` for XML generation

You can install them using:

```bash
pip install openpyxl lxml
