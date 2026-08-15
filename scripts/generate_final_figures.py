from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt, math
from sklearn.model_selection import GroupShuffleSplit
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parents[1]; FIG=ROOT/'outputs'/'figures'; T=ROOT/'outputs'/'tables'
# Figure 11 business value
ps=pd.read_csv(T/'Final_Phase_Priority_and_Business_Value.csv').sort_values('Total_Effort_Saved')
plt.figure(figsize=(9,5.5)); plt.barh(ps['QE_Phase'],ps['Total_Effort_Saved']); plt.title('Total Effort Saved by AI-Assisted QE Phase'); plt.xlabel('Total Effort Saved (hours)'); plt.ylabel('QE Phase'); plt.tight_layout(); plt.savefig(FIG/'Figure_11_Total_Effort_Saved_by_Phase.png',dpi=300,bbox_inches='tight'); plt.close()
# Figure 13 importance stability
im=pd.read_csv(T/'Final_Permutation_Importance_Stability.csv').head(10).sort_values('Importance_Mean_Across_Splits')
plt.figure(figsize=(9,6)); plt.barh(im['Feature'],im['Importance_Mean_Across_Splits'],xerr=im['Importance_SD_Across_Splits']); plt.title('Random Forest Feature Importance Stability'); plt.xlabel('Mean decrease in R² after permutation'); plt.ylabel('Feature'); plt.tight_layout(); plt.savefig(FIG/'Figure_13_Permutation_Feature_Importance_Stability.png',dpi=300,bbox_inches='tight'); plt.close()
# Figure 14 repeated grouped holdout
rep=pd.read_csv(T/'Final_Repeated_Grouped_Holdout_All_Splits.csv'); models=['Linear Regression','Random Forest','Gradient Boosting']; data=[rep.loc[rep.Model==m,'R2'].values for m in models]
plt.figure(figsize=(8,5)); plt.boxplot(data,tick_labels=models); plt.title('Repeated Sprint-Grouped Holdout R² Across 10 Splits'); plt.ylabel('R²'); plt.xticks(rotation=15); plt.tight_layout(); plt.savefig(FIG/'Figure_14_Repeated_Grouped_Holdout_R2.png',dpi=300,bbox_inches='tight'); plt.close()
# Figure 12 actual vs predicted canonical RF
project=pd.read_csv(ROOT/'data'/'processed'/'EQEPD_Cleaned_Project_Level.csv'); phases=['Test Planning','Test Design','Automation Development','Test Execution','Regression Testing','Defect Management']
for p in phases:
 b=f'Baseline effort ({p})'; project[f'Baseline_Share_{p}']=project[b]/project['Total_Baseline_Effort']; project[f'AI_Exposure_{p}']=project[f'AI_{p}']*project[f'Baseline_Share_{p}']
md=project.dropna(subset=['Overall_Productivity_Improvement_Pct']).copy(); lo,hi=md.Overall_Productivity_Improvement_Pct.quantile([.01,.99]); md['Target_Productivity']=md.Overall_Productivity_Improvement_Pct.clip(lo,hi)
baseline_cols=[f'Baseline effort ({p})' for p in phases]; features=['Application_Name','Complexity','Year','Sprint_Number','User story count','test case count','Story_to_Test_Ratio','AI_Phase_Count','Total_Baseline_Effort']+baseline_cols+[f'AI_{p}' for p in phases]+[f'Baseline_Share_{p}' for p in phases]+[f'AI_Exposure_{p}' for p in phases]
X=md[features]; y=md.Target_Productivity; groups=md['Sprint #']; cat=[c for c in features if X[c].dtype=='object']; num=[c for c in features if c not in cat]
pre=ColumnTransformer([('numeric',Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]),num),('categorical',Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('encoder',OneHotEncoder(handle_unknown='ignore'))]),cat)])
rf=Pipeline([('preprocessor',pre),('model',RandomForestRegressor(n_estimators=400,max_depth=10,min_samples_leaf=2,max_features=.8,random_state=42,n_jobs=1))]); tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(X,y,groups=groups)); rf.fit(X.iloc[tr],y.iloc[tr]); pred=rf.predict(X.iloc[te]); actual=y.iloc[te]
plt.figure(figsize=(6.5,6)); plt.scatter(actual,pred,alpha=.7); mn=min(actual.min(),pred.min()); mx=max(actual.max(),pred.max()); plt.plot([mn,mx],[mn,mx],linestyle='--'); plt.title('Actual vs Predicted Productivity - Random Forest'); plt.xlabel('Actual Productivity Improvement (%)'); plt.ylabel('Predicted Productivity Improvement (%)'); plt.tight_layout(); plt.savefig(FIG/'Figure_12_Actual_vs_Predicted_Productivity.png',dpi=300,bbox_inches='tight'); plt.close()
print('generated final figures')
