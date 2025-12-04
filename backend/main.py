from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

from cleaning_model import load_data_from_filelike, run_cleaning_pipeline

app = FastAPI()

# Allow Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/clean-data")
async def clean_data(
    file: UploadFile = File(...),
    drop_rows: bool = Form(True),
    drop_columns: bool = Form(True),
    clean_strings: bool = Form(True),
    impute_cats: bool = Form(True),
    impute_nums: bool = Form(True),
):
    try:
        # Load DataFrame from uploaded file
        df = load_data_from_filelike(file.file, file.filename)

        # Run cleaning pipeline with user-selected steps
        cleaned_df = run_cleaning_pipeline(
            df,
            drop_columns=drop_columns,
            drop_rows=drop_rows,
            clean_strings=clean_strings,
            impute_cats=impute_cats,
            impute_nums=impute_nums,
        )

        # Return cleaned CSV as download
        buffer = io.StringIO()
        cleaned_df.to_csv(buffer, index=False)
        buffer.seek(0)

        output_filename = f"cleaned_{file.filename.rsplit('.', 1)[0]}.csv"
        headers = {
            "Content-Disposition": f'attachment; filename="{output_filename}"'
        }

        return StreamingResponse(
            buffer,
            media_type="text/csv",
            headers=headers,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
