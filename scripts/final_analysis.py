from pathlib import Path
from itertools import combinations
import math
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.inspection import permutation_importance

ROOT=Path(__file__).resolve().parents[1]
TABLES=ROOT/'outputs'/'tables'; FIGS=ROOT/'outputs'/'figures'
TABLES.mkdir(parents=True, exist_ok=True); FIGS.mkdir(parents=True, exist_ok=True)
project=pd.read_csv(ROOT/'data'/'processed'/'EQEPD_Cleaned_Project_Level.csv')
phase=pd.read_csv(ROOT/'data'/'processed'/'EQEPD_Engineered_Phase_Level.csv')
valid=phase.dropna(subset=['Baseline_Effort','Actual_Effort','Productivity_Improvement_Pct']).copy()
phases=['Test Planning','Test Design','Automation Development','Test Execution','Regression Testing','Defect Management']

# helpers

def rank_biserial_from_u(u, n1, n2):
    return 2*u/(n1*n2)-1

def cohens_d(a,b):
    n1,n2=len(a),len(b)
    s1=np.var(a,ddof=1); s2=np.var(b,ddof=1)
    pooled=np.sqrt(((n1-1)*s1+(n2-1)*s2)/(n1+n2-2))
    return (np.mean(a)-np.mean(b))/pooled

def rq1_metrics(df,label):
    a=df.loc[df.AI_Used=='Yes','Productivity_Improvement_Pct'].dropna().values
    b=df.loc[df.AI_Used=='No','Productivity_Improvement_Pct'].dropna().values
    mw=stats.mannwhitneyu(a,b,alternative='two-sided')
    welch=stats.ttest_ind(a,b,equal_var=False)
    return {
        'Sensitivity': label,
        'AI_N':len(a),'Traditional_N':len(b),
        'AI_Mean_Pct':np.mean(a),'Traditional_Mean_Pct':np.mean(b),
        'Difference_Points':np.mean(a)-np.mean(b),
        'Mann_Whitney_U':mw.statistic,'Mann_Whitney_p':mw.pvalue,
        'Welch_t':welch.statistic,'Welch_p':welch.pvalue,
        'Cohens_d':cohens_d(a,b),
        'Rank_Biserial':rank_biserial_from_u(mw.statistic,len(a),len(b)),
        'AI_Total_Hours_Saved':df.loc[df.AI_Used=='Yes','Effort_Saved'].sum(),
        'Traditional_Total_Hours_Saved':df.loc[df.AI_Used=='No','Effort_Saved'].sum(),
    }

sens=[]
sens.append(rq1_metrics(valid,'Primary - all valid observations'))
# Winsorized outcome at 1/99, retaining all records
w=valid.copy(); lo,hi=w.Productivity_Improvement_Pct.quantile([.01,.99]); w['Productivity_Improvement_Pct']=w.Productivity_Improvement_Pct.clip(lo,hi)
sens.append(rq1_metrics(w,'Outcome winsorized at 1st/99th percentiles'))
# denominator thresholds
sens.append(rq1_metrics(valid[valid.Baseline_Effort>=5].copy(),'Baseline effort >= 5 hours'))
sens.append(rq1_metrics(valid[valid.Baseline_Effort>=10].copy(),'Baseline effort >= 10 hours'))
# IQR-excluded sensitivity
q1,q3=valid.Productivity_Improvement_Pct.quantile([.25,.75]); iqr=q3-q1; low=q1-1.5*iqr; high=q3+1.5*iqr
sens.append(rq1_metrics(valid[(valid.Productivity_Improvement_Pct>=low)&(valid.Productivity_Improvement_Pct<=high)].copy(),'Exclude 1.5-IQR outcome extremes'))
rq1sens=pd.DataFrame(sens)
rq1sens.to_csv(TABLES/'Final_RQ1_Sensitivity_Analysis.csv',index=False)

# power analysis using conservative small-to-moderate d=.30, 2:1 allocation ratio
power=TTestIndPower(); req_n_ai=math.ceil(power.solve_power(effect_size=.30, alpha=.05, power=.80, ratio=2.0, alternative='two-sided'))
req_n_trad=math.ceil(req_n_ai*2)
power_tbl=pd.DataFrame([{'Assumed_Effect_Size_d':.30,'Alpha':.05,'Power':.80,'Allocation_Traditional_to_AI':2.0,'Required_AI_N':req_n_ai,'Required_Traditional_N':req_n_trad,'Required_Total_N':req_n_ai+req_n_trad,'Observed_AI_N':int((valid.AI_Used=='Yes').sum()),'Observed_Traditional_N':int((valid.AI_Used=='No').sum())}])
power_tbl.to_csv(TABLES/'Final_Minimum_Sample_Size_Power_Check.csv',index=False)

# RQ2 robustness and phase priority
ai=valid[valid.AI_Used=='Yes'].copy()
groups=[g.Productivity_Improvement_Pct.values for _,g in ai.groupby('QE_Phase')]
kw=stats.kruskal(*groups)
k=len(groups); n=len(ai); eps2=max(0,(kw.statistic-k+1)/(n-k))
# threshold sensitivity >=5h
ai5=ai[ai.Baseline_Effort>=5]
groups5=[g.Productivity_Improvement_Pct.values for _,g in ai5.groupby('QE_Phase')]
kw5=stats.kruskal(*groups5); eps25=max(0,(kw5.statistic-k+1)/(len(ai5)-k))
rq2sens=pd.DataFrame([
    {'Sensitivity':'Primary - all AI-assisted valid observations','N':len(ai),'Kruskal_Wallis_H':kw.statistic,'p_value':kw.pvalue,'Epsilon_Squared':eps2},
    {'Sensitivity':'AI-assisted observations with baseline >=5 hours','N':len(ai5),'Kruskal_Wallis_H':kw5.statistic,'p_value':kw5.pvalue,'Epsilon_Squared':eps25},
])
rq2sens.to_csv(TABLES/'Final_RQ2_Sensitivity_Analysis.csv',index=False)

phase_summary=ai.groupby('QE_Phase').agg(AI_Activities=('Productivity_Improvement_Pct','size'),Mean_Productivity_Improvement_Pct=('Productivity_Improvement_Pct','mean'),Median_Productivity_Improvement_Pct=('Productivity_Improvement_Pct','median'),Mean_Effort_Saved=('Effort_Saved','mean'),Total_Effort_Saved=('Effort_Saved','sum'),Total_Baseline_Effort=('Baseline_Effort','sum')).reset_index()
phase_summary['Aggregate_Effort_Reduction_Pct']=100*phase_summary.Total_Effort_Saved/phase_summary.Total_Baseline_Effort
priority_map={'Regression Testing':'Scale now','Test Design':'Scale now','Automation Development':'Scale now','Defect Management':'Controlled expansion','Test Planning':'Targeted pilot','Test Execution':'Targeted pilot'}
phase_summary['Recommended_Adoption_Tier']=phase_summary.QE_Phase.map(priority_map)
phase_summary=phase_summary.sort_values('Mean_Productivity_Improvement_Pct',ascending=False)
phase_summary.to_csv(TABLES/'Final_Phase_Priority_and_Business_Value.csv',index=False)

# RQ3 stability models
reg=valid.copy().rename(columns={'AI_Used_Flag':'AI_Flag','Baseline_Effort':'Baseline','User story count':'User_Stories','test case count':'Test_Cases','QE_Phase':'Phase','Application_Name':'Application','Team_Name':'Team'})
base_formula='Productivity ~ AI_Flag + Baseline + User_Stories + Test_Cases + Year + Sprint_Number + C(Phase) + C(Complexity) + C(Application)'

def fit_reg(label, outcome, formula=base_formula):
    d=reg.copy(); d['Productivity']=outcome(d)
    m=smf.ols(formula,data=d).fit(cov_type='cluster',cov_kwds={'groups':d['Sprint #']})
    ci=m.conf_int().loc['AI_Flag']
    return {'Specification':label,'N':int(m.nobs),'R2':m.rsquared,'Adj_R2':m.rsquared_adj,'AI_Coefficient_Points':m.params['AI_Flag'],'AI_CI_Lower':ci[0],'AI_CI_Upper':ci[1],'AI_p_value':m.pvalues['AI_Flag']}

results=[]
results.append(fit_reg('Primary: 1/99 winsorized outcome, application controls',lambda d: d.Productivity_Improvement_Pct.clip(*d.Productivity_Improvement_Pct.quantile([.01,.99]).values)))
results.append(fit_reg('Raw outcome, application controls',lambda d:d.Productivity_Improvement_Pct))
results.append(fit_reg('5/95 winsorized outcome, application controls',lambda d: d.Productivity_Improvement_Pct.clip(*d.Productivity_Improvement_Pct.quantile([.05,.95]).values)))
team_formula='Productivity ~ AI_Flag + Baseline + User_Stories + Test_Cases + Year + Sprint_Number + C(Phase) + C(Complexity) + C(Team)'
results.append(fit_reg('1/99 winsorized outcome, team controls',lambda d: d.Productivity_Improvement_Pct.clip(*d.Productivity_Improvement_Pct.quantile([.01,.99]).values),team_formula))
reduced_formula='Productivity ~ AI_Flag + Baseline + User_Stories + Test_Cases + Year + C(Phase) + C(Complexity)'
results.append(fit_reg('1/99 winsorized outcome, reduced context controls',lambda d: d.Productivity_Improvement_Pct.clip(*d.Productivity_Improvement_Pct.quantile([.01,.99]).values),reduced_formula))
rq3stab=pd.DataFrame(results)
rq3stab.to_csv(TABLES/'Final_RQ3_Regression_Stability.csv',index=False)

# predictive setup
for phase_name in phases:
    b=f'Baseline effort ({phase_name})'
    project[f'Baseline_Share_{phase_name}']=project[b]/project['Total_Baseline_Effort']
    project[f'AI_Exposure_{phase_name}']=project[f'AI_{phase_name}']*project[f'Baseline_Share_{phase_name}']
model_data=project.dropna(subset=['Overall_Productivity_Improvement_Pct']).copy()
tlo,thi=model_data.Overall_Productivity_Improvement_Pct.quantile([.01,.99]); model_data['Target_Productivity']=model_data.Overall_Productivity_Improvement_Pct.clip(tlo,thi)
baseline_cols=[f'Baseline effort ({p})' for p in phases]
feature_cols=['Application_Name','Complexity','Year','Sprint_Number','User story count','test case count','Story_to_Test_Ratio','AI_Phase_Count','Total_Baseline_Effort']+baseline_cols+[f'AI_{p}' for p in phases]+[f'Baseline_Share_{p}' for p in phases]+[f'AI_Exposure_{p}' for p in phases]
X=model_data[feature_cols]; y=model_data.Target_Productivity; groups_s=model_data['Sprint #']
cat=[c for c in feature_cols if X[c].dtype=='object']; num=[c for c in feature_cols if c not in cat]

def prep():
    return ColumnTransformer([('numeric',Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]),num),('categorical',Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('encoder',OneHotEncoder(handle_unknown='ignore'))]),cat)])

def model_dict(seed=42):
    return {
        'Linear Regression':LinearRegression(),
        'Random Forest':RandomForestRegressor(n_estimators=400,max_depth=10,min_samples_leaf=2,max_features=.8,random_state=seed,n_jobs=1),
        'Gradient Boosting':GradientBoostingRegressor(n_estimators=350,learning_rate=.03,max_depth=2,min_samples_leaf=3,subsample=.9,random_state=seed),
    }

def make_pipeline(est):
    return Pipeline([('preprocessor',prep()),('model',est)])

# canonical seed 42 results
split=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42); tr,te=next(split.split(X,y,groups=groups_s))
canon=[]; fitted={}; preds={}
for name,est in model_dict(42).items():
    pipe=make_pipeline(est); pipe.fit(X.iloc[tr],y.iloc[tr]); pr=pipe.predict(X.iloc[te])
    canon.append({'Model':name,'MAE':mean_absolute_error(y.iloc[te],pr),'RMSE':math.sqrt(mean_squared_error(y.iloc[te],pr)),'R2':r2_score(y.iloc[te],pr)})
    fitted[name]=pipe; preds[name]=pr
canon=pd.DataFrame(canon).sort_values('R2',ascending=False); canon.to_csv(TABLES/'Final_Model_Performance_Seed42.csv',index=False)

# grouped 5-fold CV, new unfitted pipelines
cv=GroupKFold(n_splits=5); cvres=[]
for name,est in model_dict(42).items():
    pipe=make_pipeline(est)
    sc=cross_validate(pipe,X,y,groups=groups_s,cv=cv,scoring={'mae':'neg_mean_absolute_error','rmse':'neg_root_mean_squared_error','r2':'r2'},n_jobs=1)
    cvres.append({'Model':name,'CV_MAE_Mean':-sc['test_mae'].mean(),'CV_MAE_SD':sc['test_mae'].std(),'CV_RMSE_Mean':-sc['test_rmse'].mean(),'CV_RMSE_SD':sc['test_rmse'].std(),'CV_R2_Mean':sc['test_r2'].mean(),'CV_R2_SD':sc['test_r2'].std()})
cvres=pd.DataFrame(cvres).sort_values('CV_R2_Mean',ascending=False); cvres.to_csv(TABLES/'Final_Grouped_Cross_Validation.csv',index=False)

# repeated grouped holdout across 10 split seeds; estimator fixed seed 42 for comparability
rep=[]; imp_rows=[]
for split_seed in range(10):
    tr2,te2=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=split_seed).split(X,y,groups=groups_s))
    split_metrics=[]
    for name,est in model_dict(42).items():
        pipe=make_pipeline(est); pipe.fit(X.iloc[tr2],y.iloc[tr2]); pr=pipe.predict(X.iloc[te2])
        row={'Split_Seed':split_seed,'Model':name,'MAE':mean_absolute_error(y.iloc[te2],pr),'RMSE':math.sqrt(mean_squared_error(y.iloc[te2],pr)),'R2':r2_score(y.iloc[te2],pr),'Train_N':len(tr2),'Test_N':len(te2),'Train_Sprints':groups_s.iloc[tr2].nunique(),'Test_Sprints':groups_s.iloc[te2].nunique()}
        rep.append(row); split_metrics.append(row)
        if name=='Random Forest' and split_seed < 5:
            pi=permutation_importance(pipe,X.iloc[te2],y.iloc[te2],n_repeats=3,random_state=123,scoring='r2',n_jobs=1)
            for f,m,sd in zip(feature_cols,pi.importances_mean,pi.importances_std):
                imp_rows.append({'Split_Seed':split_seed,'Feature':f,'Importance_Mean':m,'Importance_SD_Within_Split':sd})
rep=pd.DataFrame(rep); rep.to_csv(TABLES/'Final_Repeated_Grouped_Holdout_All_Splits.csv',index=False)
summary=rep.groupby('Model').agg(Holdout_Runs=('R2','size'),MAE_Mean=('MAE','mean'),MAE_SD=('MAE','std'),RMSE_Mean=('RMSE','mean'),RMSE_SD=('RMSE','std'),R2_Mean=('R2','mean'),R2_SD=('R2','std'),R2_Min=('R2','min'),R2_Max=('R2','max')).reset_index()
winners=rep.loc[rep.groupby('Split_Seed')['R2'].idxmax()].Model.value_counts()
summary['Best_R2_Run_Count']=summary.Model.map(winners).fillna(0).astype(int)
summary=summary.sort_values('R2_Mean',ascending=False); summary.to_csv(TABLES/'Final_Repeated_Grouped_Holdout_Summary.csv',index=False)

imp=pd.DataFrame(imp_rows)
imp_summary=imp.groupby('Feature').agg(Importance_Mean_Across_Splits=('Importance_Mean','mean'),Importance_SD_Across_Splits=('Importance_Mean','std'),Positive_Importance_Rate=('Importance_Mean',lambda s:(s>0).mean()),Median_Importance=('Importance_Mean','median')).reset_index().sort_values('Importance_Mean_Across_Splits',ascending=False)
imp_summary.to_csv(TABLES/'Final_Permutation_Importance_Stability.csv',index=False)

# residual diagnostics for canonical RF seed42
rf=fitted['Random Forest']; rf_pred=preds['Random Forest']; test=model_data.iloc[te].copy(); test['Observed']=y.iloc[te].values; test['Predicted']=rf_pred; test['Error']=test.Observed-test.Predicted; test['Absolute_Error']=test.Error.abs()
seg=[]
for var in ['Year','Complexity','Application_Name','AI_Phase_Count']:
    g=test.groupby(var).agg(N=('Absolute_Error','size'),MAE=('Absolute_Error','mean'),Bias=('Error','mean'),Observed_Mean=('Observed','mean'),Predicted_Mean=('Predicted','mean')).reset_index().rename(columns={var:'Segment_Value'})
    g.insert(0,'Segment_Variable',var); seg.append(g)
seg=pd.concat(seg,ignore_index=True); seg.to_csv(TABLES/'Final_Random_Forest_Error_by_Segment.csv',index=False)

# adoption roadmap table with evidence summary
road=[]
for _,r in phase_summary.iterrows():
    if r.Recommended_Adoption_Tier=='Scale now': action='Standardise proven use cases, expand coverage, and monitor quality guardrails.'
    elif r.Recommended_Adoption_Tier=='Controlled expansion': action='Expand selectively with human validation and phase-specific acceptance criteria.'
    else: action='Keep as targeted pilots until stronger productivity and quality evidence is collected.'
    road.append({'QE_Phase':r.QE_Phase,'Tier':r.Recommended_Adoption_Tier,'Mean_Productivity_Improvement_Pct':r.Mean_Productivity_Improvement_Pct,'Total_Effort_Saved_Hours':r.Total_Effort_Saved,'Recommended_Action':action})
pd.DataFrame(road).to_csv(TABLES/'Final_AI_Adoption_Roadmap.csv',index=False)

# final headline summary text
print('RQ1 sensitivity')
print(rq1sens[['Sensitivity','AI_N','Traditional_N','AI_Mean_Pct','Traditional_Mean_Pct','Difference_Points','Mann_Whitney_p','Cohens_d']].to_string(index=False))
print('\nPower',power_tbl.to_dict('records')[0])
print('\nRQ2',rq2sens.to_string(index=False))
print('\nPhase summary',phase_summary.to_string(index=False))
print('\nRQ3 stability',rq3stab.to_string(index=False))
print('\nCanonical models',canon.to_string(index=False))
print('\nCV',cvres.to_string(index=False))
print('\nRepeated holdout',summary.to_string(index=False))
print('\nTop importance',imp_summary.head(10).to_string(index=False))
print('\nWorst segments',seg[seg.N>=3].sort_values('MAE',ascending=False).head(10).to_string(index=False))


# execution environment manifest
import sys, matplotlib, scipy, statsmodels, sklearn, openpyxl
env = pd.DataFrame([
    ('Python', sys.version.split()[0]),
    ('NumPy', np.__version__),
    ('Pandas', pd.__version__),
    ('Matplotlib', matplotlib.__version__),
    ('SciPy', scipy.__version__),
    ('Statsmodels', statsmodels.__version__),
    ('scikit-learn', sklearn.__version__),
    ('openpyxl', openpyxl.__version__),
], columns=['Component','Version'])
env.to_csv(TABLES/'Final_Execution_Environment.csv', index=False)
