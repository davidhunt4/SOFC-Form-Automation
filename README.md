# SOFC Form Automation

## Description

This automates the filling of SOFC forms for the Student Engineers' Council, supporting **eCheck Request** and **eCredit Card Payment Request** forms. File uploads (receipt, bank statement) within the forms still need to be done manually at this time.

The program proceeds **chronologically** through unprocessed payments in the SEC Expense Report and gives users the choice whether or not to process each one.

## Setup

1. Clone this repository into Visual Studio Code.
2. Get `.env` and `handy-cell-478015-u7-397b5b7f6c77.json` and from someone who has them.
3. Put those files into this folder on your device.
4. Run `pip install -r requirements.txt` in VSCode terminal.

## Usage

1. Open VSCode terminal and run `python sofc_form_automation.py`
2. Chrome window will open - make sure you can see both Chrome and your terminal.
3. Respond to the first prompt and ensure inputs appear properly in Chrome:
```
Process Invoice submitted by John Smith ($XX.XX)? (yes/no): yes
Entered 'Student Engineers' Council' into field #0
Entered 'ACCOUNT NUMBER' into field #1
Entered 'PURPOSE OF PURCHASE' into field #17
Entered 'XX.XX' into field #26
Entered 'SUBACCOUNT NUMBER' into field #2
Entered 'VENDOR NAME' into field #7
Entered 'PHONE NUMBER' into field #8
Entered 'ADDRESS LINE 1' into field #9
Entered 'ADDRESS LINE 2' into field #11
```
4. Upload receipt / bank statement / any other attachments as necessary.
5. Submit the form, verify email, and sign the form.
6. Respond to the next prompt in your terminal:
```
Form Submitted and Signed? (yes/no): yes
```
7. Repeat steps 3-7 until you receive confirmation that all payments are processed: 
```
All rows completed!
```

## Notes

- To stop the program at any time, go to the terminal and press `Ctrl+C`.
- SOFC Approval to Charge payments are not supported at this time.