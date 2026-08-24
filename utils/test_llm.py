from app.schema_loader import extract_schema

from app.llm import generate_sql

def main():


    sql =generate_sql("How many students are enrolled in each program?")
    print(sql)

if __name__ =="__main__":
    main()