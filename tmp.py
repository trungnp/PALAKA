import pandas as pd
df = pd.read_sas('spm_pu_2022.sas7bdat', encoding='utf-8')
# Remove error data
df = df[df['st'] != 99]
# Count cases in each state
case_count_by_state = df['st'].value_counts()
# Normalize to percentage
case_pct_by_state = case_count_by_state/df.shape[0]
# Calculate distribution of each state in a sample of 200k rows, round down
sample_case_dist_by_state = (case_pct_by_state*200000).astype(int)
# Get random rows from the original dataset for each state based on the distribution above
sample = [df[df['st'] == i].sample(j, random_state=0) for i,j in sample_case_dist_by_state.items()]
# Form the new dataset
f = pd.concat(sample, ignore_index=True)


fips = pd.read_csv('fips2county.tsv', sep='\t')
fips = fips.rename(columns={'StateFIPS': 'st'})
fips = fips[['st', 'StateAbbr']].drop_duplicates()
df = f.merge(fips, on='st', how='left')

# df = df.drop('Unnamed: 0', axis=1)
df.to_csv('sample.csv', header=True, index=False)

print(1)