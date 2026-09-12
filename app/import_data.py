import pandas as pd

from app.database import SessionLocal
from app.models.work import LokSabhaWork, RajyaSabhaWork


RAJYA_FILE = "data/rajya_sabha_final_processed_ml_master.csv"
LOK_FILE = "data/lok_sabha_final_processed_ml_master.xlsx"


COMMON_FIELDS = {
    "work_id",
    "sabha",
    "work_category",
    "work",
    "state",
    "mp_name",
    "work_description",
    "recommended_date",
    "recommended_amount_rs",
    "sanctioned_date",
    "sanctioned_amount_rs",
    "work_status",
    "completed",
    "completion_date",
    "amount_disbursed_rs",
    "allocated_amount_rs",
    "image",
}


def convert_date(value):
    if pd.isna(value):
        return None

    return pd.to_datetime(value, errors="coerce").date()


def clean_number(value):
    if pd.isna(value):
        return None

    try:
        return float(value)
    except:
        return None


def clean_boolean(value):
    if pd.isna(value):
        return None

    if isinstance(value, bool):
        return value

    return str(value).lower() in [
        "true",
        "yes",
        "1",
        "completed"
    ]


def clean_extra_data(row):
    extra = {}

    for column in row.index:

        if column in COMMON_FIELDS:
            continue

        value = row[column]

        if pd.isna(value):
            extra[column] = None

        elif isinstance(value, pd.Timestamp):
            extra[column] = value.isoformat()

        else:
            extra[column] = value

    return extra


def create_common_data(row, sabha):

    return {
        "work_id": (
            None
            if pd.isna(row.get("work_id"))
            else str(row.get("work_id"))
        ),

        "sabha": sabha,

        "work_category": row.get("work_category"),
        "work": row.get("work"),
        "state": row.get("state"),
        "mp_name": row.get("mp_name"),
        "work_description": row.get("work_description"),

        "recommended_date": convert_date(
            row.get("recommended_date")
        ),

        "recommended_amount_rs": clean_number(
            row.get("recommended_amount_rs")
        ),

        "sanctioned_date": convert_date(
            row.get("sanctioned_date")
        ),

        "sanctioned_amount_rs": clean_number(
            row.get("sanctioned_amount_rs")
        ),

        "work_status": row.get("work_status"),

        "completed": clean_boolean(
            row.get("completed")
        ),

        "completion_date": convert_date(
            row.get("completion_date")
        ),

        "amount_disbursed_rs": clean_number(
            row.get("amount_disbursed_rs")
        ),

        "allocated_amount_rs": clean_number(
            row.get("allocated_amount_rs")
        ),

        "image": row.get("image"),

        "extra_data": clean_extra_data(row),
    }


def import_rajya_sabha():

    print("Reading Rajya Sabha dataset...")

    df = pd.read_csv(RAJYA_FILE)

    db = SessionLocal()

    try:

        for _, row in df.iterrows():

            data = create_common_data(
                row,
                "Rajya Sabha"
            )

            work = RajyaSabhaWork(**data)

            db.add(work)

        db.commit()

        print(
            f"Imported {len(df)} Rajya Sabha records."
        )

    except Exception as e:

        db.rollback()

        print("Rajya Sabha import failed:")
        print(e)

    finally:

        db.close()


def import_lok_sabha():

    print("Reading Lok Sabha dataset...")

    df = pd.read_excel(LOK_FILE)

    db = SessionLocal()

    try:

        for _, row in df.iterrows():

            data = create_common_data(
                row,
                "Lok Sabha"
            )

            work = LokSabhaWork(**data)

            db.add(work)

        db.commit()

        print(
            f"Imported {len(df)} Lok Sabha records."
        )

    except Exception as e:

        db.rollback()

        print("Lok Sabha import failed:")
        print(e)

    finally:

        db.close()


def main():

    import_rajya_sabha()

    import_lok_sabha()


if __name__ == "__main__":
    main()