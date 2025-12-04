"use client";

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [dropRows, setDropRows] = useState(true);
  const [dropColumns, setDropColumns] = useState(true);
  const [cleanStrings, setCleanStrings] = useState(true);
  const [imputeCats, setImputeCats] = useState(true);
  const [imputeNums, setImputeNums] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("drop_rows", String(dropRows));
    formData.append("drop_columns", String(dropColumns));
    formData.append("clean_strings", String(cleanStrings));
    formData.append("impute_cats", String(imputeCats));
    formData.append("impute_nums", String(imputeNums));

    const res = await fetch("http://localhost:8000/clean-data", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      console.error("Error cleaning data");
      return;
    }

    // Get cleaned CSV blob and trigger download
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "cleaned_data.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <main style={{ padding: 20 }} className="text-center">
      <h1 className="text-4xl mb-5">Data Cleaning Tool</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            File:
            <input
              type="file"
              accept=".csv,.xls,.xlsx"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  setFile(e.target.files[0]);
                }
              }}
              className="bg-gray-900 p-10 rounded-3xl"
            />
          </label>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={dropRows}
              onChange={(e) => setDropRows(e.target.checked)}
            />
            Drop blank rows
          </label>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={dropColumns}
              onChange={(e) => setDropColumns(e.target.checked)}
            />
            Drop blank columns
          </label>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={cleanStrings}
              onChange={(e) => setCleanStrings(e.target.checked)}
            />
            Clean gibberish strings
          </label>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={imputeCats}
              onChange={(e) => setImputeCats(e.target.checked)}
            />
            Impute categorical values
          </label>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={imputeNums}
              onChange={(e) => setImputeNums(e.target.checked)}
            />
            Impute numeric values (KNN)
          </label>
        </div>

        <button type="submit" className="bg-green-700 px-3 py-1.5 rounded-xl">
          Clean Data
        </button>
      </form>
    </main>
  );
}
