from app.schema_loader import extract_schema
from app.schema_format import format_schema
def main():

    schema=extract_schema()
    schema_formatted = format_schema(schema)
    print(schema_formatted )

if __name__ =="__main__":
    main()