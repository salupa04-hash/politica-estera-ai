import os
from datetime import datetime

output_file = "politica_estera_AI_finale.csv"

new_df = pd.DataFrame(results)

# Aggiungiamo data di estrazione
new_df["Data_estrazione"] = datetime.utcnow().strftime("%Y-%m-%d")

# Se file già esiste → carica e unisci
if os.path.exists(output_file):
    old_df = pd.read_csv(output_file, sep=";")
    combined = pd.concat([old_df, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["Link"])
else:
    combined = new_df

combined.to_csv(output_file, index=False, sep=";")
