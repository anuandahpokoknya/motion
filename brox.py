def parse_transaction_logs(raw_logs):
    if not isinstance(raw_logs, list):
        raise TypeError("Raw logs must be list")
    
    categories = ['transfer', 'withdrawal', 'login_fail']
    
    for log in raw_logs:
        if not isinstance(log, str):
            raise TypeError("log must be string")
        temp = [l.strip() for l in log.split("|")]
        if temp[0].startswith("TX-") and len(temp[0][3:]) == 4 and temp[0][3:].isdecimal():
            tx_id = temp[0]
        elif temp[1].startswith("USR-") and temp[1][3:].isdecimal():
            user_id = temp[1]
        elif len(temp[2]) == 2 and temp[2].isalpha():
            country = temp[2].upper()
        elif temp[3] and temp[3].lower() in categories:
            category = temp[3].lower()
        try:
            amount = 0 if category == 'login_fail' else float(temp[4])
        except:
            continue

        else:continue
            
            
            
        



logss = [
    " TX-1001 | USR-02 | id | TRANSFER | 500.00 ",
    " TX-1002 | USR-02 | sg | WITHDRAWAL | 600.00 ",
    " TX-1003 | USR-02 | my | LOGIN_FAIL | 0 ",
    " TX-1004 | USR-01 | id | TRANSFER | 1100.00 ",
    " TX-1005 | USR-01 | id | LOGIN_FAIL | 0 ",
    " TX-9999 | USR-01 | id | TRANSFER | -50.00 ",     # Ditolak: nominal negatif
    " TX-12   | USR-03 | us | TRANSFER | 100.00 ",     # Ditolak: digit TX kurang dari 4
    " TX-1006 | USR-03 | u1 | TRANSFER | 100.00 "      # Ditolak: kode negara mengandung angka
]