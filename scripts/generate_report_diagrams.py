from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'outputs'/'figures'; FIG.mkdir(parents=True,exist_ok=True)
# Final repository tree
repo_text='''QM640_EQEPD_Final_GitHub_Repository/\n├── data/\n│   ├── raw/EQEPD_Dataset_v5.xlsx\n│   └── processed/\n│       ├── EQEPD_Cleaned_Project_Level.csv\n│       └── EQEPD_Engineered_Phase_Level.csv\n├── notebooks/\n│   ├── QM640_EQEPD_Final_Analysis.ipynb\n│   └── QM640_EQEPD_Final_Analysis.html\n├── outputs/\n│   ├── figures/\n│   └── tables/\n├── reports/\n│   ├── QM640_Final_Capstone_Report_Satish_Venugopal.docx\n│   ├── QM640_Final_Capstone_Report_Satish_Venugopal.pdf\n│   └── FINAL_SUBMISSION_CHECKLIST.md\n├── scripts/\n│   ├── final_analysis.py\n│   ├── run_notebook.bat\n│   └── run_notebook.sh\n├── README.md\n├── requirements.txt\n├── environment_versions.txt\n└── repository_tree.txt'''
fig,ax=plt.subplots(figsize=(9,5.2)); ax.axis('off'); ax.text(0.02,0.98,repo_text,va='top',ha='left',family='monospace',fontsize=10.5); fig.tight_layout(); fig.savefig(FIG/'Figure_01_Final_Repository_Structure.png',dpi=300,bbox_inches='tight'); plt.close(fig)
# Final workflow
stages=[('Raw EQEPD\nData','459 rows, 24 fields'),('Data Quality\n& Cleaning','457 clean records'),('EDA & Feature\nEngineering','2,705 valid phase rows'),('Hypothesis &\nRobustness Tests','RQ1-RQ3, α=.05'),('Predictive\nModels','LR, RF, GB'),('Grouped Validation\n& Diagnostics','Holdout, CV, stability'),('Business Adoption\nRoadmap','Scale / expand / pilot')]
fig,ax=plt.subplots(figsize=(13.5,3.1)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
xs=[0.07,0.21,0.35,0.49,0.63,0.77,0.91]
for i,((title,sub),x) in enumerate(zip(stages,xs)):
    w=0.115; h=0.36; y=0.43
    box=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.01,rounding_size=0.015',linewidth=1.2,edgecolor='#315b7d',facecolor='#eaf1f7')
    ax.add_patch(box); ax.text(x,y+0.045,title,ha='center',va='center',fontsize=9.2,fontweight='bold'); ax.text(x,y-0.10,sub,ha='center',va='center',fontsize=7.2)
    if i<len(xs)-1:
        ax.add_patch(FancyArrowPatch((x+w/2+0.003,y),(xs[i+1]-w/2-0.003,y),arrowstyle='-|>',mutation_scale=12,linewidth=1.1,color='#315b7d'))
ax.text(0.5,0.88,'End-to-End Final Analytical and Decision-Support Workflow',ha='center',va='center',fontsize=13,fontweight='bold')
ax.text(0.5,0.12,'Statistical association and predictive screening are translated into governed phase-level adoption decisions; no autonomous deployment is proposed.',ha='center',va='center',fontsize=8.2)
fig.tight_layout(); fig.savefig(FIG/'Figure_02_Final_Analytical_Workflow.png',dpi=300,bbox_inches='tight'); plt.close(fig)
# Final grouped holdout model comparison Figure 10
import pandas as pd
m=pd.read_csv(ROOT/'outputs'/'tables'/'Final_Model_Performance_Seed42.csv')
fig,ax=plt.subplots(figsize=(7.5,4.7)); ax.bar(m['Model'],m['R2']); ax.set_title('Grouped Holdout Model Comparison'); ax.set_ylabel('R²'); ax.tick_params(axis='x',rotation=15); fig.tight_layout(); fig.savefig(FIG/'Figure_10_Grouped_Holdout_Model_Comparison_Final.png',dpi=300,bbox_inches='tight'); plt.close(fig)
print('done')
