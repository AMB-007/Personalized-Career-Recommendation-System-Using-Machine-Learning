"""
Extracts unique careers directly from 'Student Career Recommendation Dataset.csv',
and inspects the available fields and career profiles.
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "Datasets" / "Student Career Recommendation Dataset.csv"

df = pd.read_csv(csv_path)
print("Total rows:", len(df))

# Clean and normalize career_name
df['clean_name'] = df['career_name'].astype(str).str.strip().str.title()
df = df[df['clean_name'] != 'Nan']

# Group by clean career name to aggregate career properties from the dataset
careers_summary = []
for name, group in df.groupby('clean_name'):
    # Extract dominant/mode domain, subdomain, cluster, and career_id
    c_id = group['career_id'].dropna().mode().iloc[0] if len(group['career_id'].dropna()) > 0 else f"CAR{len(careers_summary)+1:05d}"
    domain = group['career_domain'].dropna().astype(str).str.strip().str.title().mode().iloc[0] if len(group['career_domain'].dropna()) > 0 else "General"
    subdomain = group['career_subdomain'].dropna().astype(str).str.strip().str.title().mode().iloc[0] if len(group['career_subdomain'].dropna()) > 0 else "Track 1"
    cluster = group['career_cluster'].dropna().astype(str).str.strip().str.title().mode().iloc[0] if len(group['career_cluster'].dropna()) > 0 else "Cluster 1"
    stream = group['stream'].dropna().astype(str).str.strip().str.title().mode().iloc[0] if len(group['stream'].dropna()) > 0 else "All"
    
    # Calculate average ability and interest components from dataset for this career
    avg_ability = round(float(pd.to_numeric(group['ability_match_component'], errors='coerce').mean()), 2) if 'ability_match_component' in group else 75.0
    avg_interest = round(float(pd.to_numeric(group['interest_match_component'], errors='coerce').mean()), 2) if 'interest_match_component' in group else 75.0
    avg_academic = round(float(pd.to_numeric(group['academic_match_component'], errors='coerce').mean()), 2) if 'academic_match_component' in group else 75.0
    avg_composite = round(float(pd.to_numeric(group['composite_alignment_index'], errors='coerce').mean()), 2) if 'composite_alignment_index' in group else 75.0

    careers_summary.append({
        'career_code': str(c_id).upper(),
        'career_name': name,
        'domain': domain,
        'subdomain': subdomain,
        'cluster': cluster,
        'stream': stream,
        'avg_ability': avg_ability,
        'avg_interest': avg_interest,
        'avg_academic': avg_academic,
        'avg_composite': avg_composite,
        'sample_count': len(group)
    })

df_careers = pd.DataFrame(careers_summary)
print(f"Extracted {len(df_careers)} unique careers from 'Student Career Recommendation Dataset.csv'.")
print("\nFirst 10 careers extracted:")
print(df_careers[['career_code', 'career_name', 'domain', 'subdomain', 'cluster']].head(10))
