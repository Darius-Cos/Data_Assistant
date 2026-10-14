import re

def parse_ddl(ddl_content):
    pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["`]?(\w+)["`]?\s*\('
        #Parametrul re.IGNORECASE face ca cautarea sa functioneze atat pentru 
    # 'create table' cat si pentru 'CREATE TABLE' — util deoarece SQL nu este case-sensitive.
    tables = re.findall(pattern, ddl_content, re.IGNORECASE)
    return {"raw_ddl": ddl_content, "table_names": tables}
