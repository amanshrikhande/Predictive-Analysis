
# Aircraft Engine Remaining Useful Life (RUL) Prediction

**Course:** Predictive Analytics  
**Project type:** End-to-end Predictive Analytics / Knowledge Discovery in Databases (KDD)  
**Dataset:** NASA C-MAPSS FD001, FD002, FD003 and FD004

## 1. Project Overview

Aircraft engines operate under changing conditions, and sensor measurements can contain patterns associated with changes in engine condition. This project estimates how many operating cycles remain before an engine reaches its recorded failure endpoint. This estimate is called **Remaining Useful Life (RUL)**.

The project develops and evaluates traditional machine-learning regression models using four subsets of the NASA C-MAPSS benchmark dataset: FD001, FD002, FD003 and FD004. It covers data understanding, preprocessing, target creation, model training, validation, test prediction, evaluation and interpretation.


## 2. Problem Statement

**Given an engine's recorded cycle number, operating settings and sensor measurements, estimate its Remaining Useful Life in operating cycles.**

The model learns from historical training engine trajectories for which RUL labels can be calculated. It then uses the latest available observation of each test engine to predict RUL.

The model directly predicts RUL; it does not directly predict the unknown failure cycle. An estimated failure cycle can be derived by adding predicted RUL to the last observed cycle, but this is a calculation based on the RUL estimate.

## 3. Objectives

- Apply the main stages of the Predictive Analytics / KDD process.
- Load and examine all four C-MAPSS subsets.
- Perform exploratory data analysis (EDA) to understand engine lifetimes and sensor data.
- Create RUL labels from complete training trajectories.
- Prepare model features and split training/validation data by engine ID.
- Train and compare traditional regression algorithms.
- Select a model based on validation performance.
- Predict RUL for test engines and compare predictions with benchmark reference values.
- Interpret results using error metrics, individual prediction errors and Random Forest feature importance.
- Export results for the project report and presentation.

## 4. Dataset

The project uses the NASA C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) turbofan engine degradation benchmark.

Each observation includes:
- **Engine ID (`unit_number`):** identifies the engine.
- **Cycle (`time_in_cycles`):** recorded operating-cycle number.
- **Three operating settings:** describe operating conditions.
- **21 sensor measurements:** record measured engine characteristics.

The original data files are whitespace-separated and do not include a header row. The notebook assigns column names when loading the files.

### Dataset subsets

| Subset | Training file | Test file | Reference RUL file |
|---|---|---|---|
| FD001 | `train_FD001.txt` | `test_FD001.txt` | `RUL_FD001.txt` |
| FD002 | `train_FD002.txt` | `test_FD002.txt` | `RUL_FD002.txt` |
| FD003 | `train_FD003.txt` | `test_FD003.txt` | `RUL_FD003.txt` |
| FD004 | `train_FD004.txt` | `test_FD004.txt` | `RUL_FD004.txt` |

The FD subsets differ in operating conditions and fault modes. Each subset is processed separately so model and evaluation results remain associated with the correct subset.

**Dataset setup:** Place all 12 text files in a folder named `dataset` next to the notebook, or update `DATA_DIR` in the notebook to point to the correct folder.

### What the files mean

- **Training file:** contains engine histories used to create RUL labels and train models.
- **Test file:** contains partial engine histories. The final failure cycle is not directly provided in this file.
- **Reference RUL file:** contains benchmark RUL values for test engines. These values are used after predictions have been generated, for evaluation; they are not model input features.

## 5. RUL Target Creation

For each row in a training engine's history:

`RUL = maximum recorded training cycle for that engine - current cycle`

For example, if an engine's maximum recorded training cycle is 200, the row at cycle 150 receives an RUL label of 50 cycles.

Training labels are calculated from complete training histories. Test histories are partial, so their RUL is predicted by the model and later compared with the reference RUL file.

## 6. KDD / Predictive Analytics Workflow

1. **Problem identification:** define RUL estimation as a regression problem.
2. **Data selection:** load FD001, FD002, FD003 and FD004 training, test and reference RUL files.
3. **Data understanding:** inspect dimensions, engine counts, missing values, summary statistics and distributions of final training cycles.
4. **Data preprocessing:** remove constant features and prepare input columns.
5. **Data transformation:** calculate training RUL labels and separate input features from the target.
6. **Train-validation split:** split by engine ID so all rows for one engine stay together.
7. **Data mining / modelling:** fit and compare three traditional regression algorithms.
8. **Evaluation:** calculate MAE, RMSE and R² on validation and benchmark test data.
9. **Interpretation:** review model comparisons, individual errors and Random Forest feature importance.
10. **Knowledge presentation:** show tables and plots and export CSV results.

## 7. Data Preparation

- Engine ID is used for grouping and tracking engines, not as a predictive input.
- RUL is the target variable and is excluded from the feature matrix.
- Cycle number, operating settings and selected sensor measurements are used as input features.
- Constant features are removed because they do not vary across observations.
- The validation split is performed by engine ID using an approximately 80:20 training-validation split.
- `SimpleImputer` with the median strategy is used inside model pipelines.
- `StandardScaler` is used for Linear Regression; tree-based models do not require feature scaling.
- Preprocessing is fitted on training data and then applied to validation/test data to reduce data leakage.

## 8. Predictive Models

The notebook compares three standard regression algorithms. No deep-learning methods are used.

### Linear Regression
Learns a weighted mathematical equation relating input features to RUL. For a new observation, it applies learned coefficients to the feature values to produce an RUL estimate. It serves as a simple baseline.

### Decision Tree Regressor
Learns feature-based threshold rules that split training observations into groups with similar RUL values. A test observation follows these rules until it reaches a leaf that supplies the predicted RUL. The baseline uses maximum depth 12 and minimum leaf size 5.

### Random Forest Regressor
Trains multiple decision trees using bootstrap samples and randomly selected subsets of features. It averages tree predictions to produce a final RUL estimate. The baseline uses 100 trees, maximum depth 20 and minimum leaf size 2.

### Model selection
The notebook compares models using validation MAE for each FD subset. The model with the lowest validation MAE is selected for that subset, then refitted on all labelled training rows before test prediction. Test reference RUL values are not used to select the model.

## 9. Evaluation Metrics

- **Mean Absolute Error (MAE):** average absolute difference between predicted and reference RUL, in cycles. Lower is better.
- **Root Mean Squared Error (RMSE):** square root of average squared error, in cycles. It gives larger errors greater influence. Lower is better.
- **R² score:** indicates how much variation in reference RUL is explained by predictions. Values closer to 1 generally indicate a better fit; a negative score is possible.

The notebook reports validation metrics for all models and test metrics for the selected model on each subset. Test results can differ from validation results because they are calculated on different engine observations.

## 10. Results and Interpretation

Run the notebook to generate the actual metrics. Do not assume fixed scores: results depend on the executed code and data files.

The notebook produces:
- A dataset summary for FD001–FD004.
- Validation MAE, RMSE and R² for each model and subset.
- Test MAE, RMSE and R² for the selected model on each subset.
- Per-engine reference RUL, predicted RUL and absolute error.
- Top Random Forest feature-importance rankings for each subset.
- Plots comparing validation MAE and visualizing important features.

When discussing results, identify which model performed best on validation data, compare test errors across subsets, examine engines with large errors, and describe the highest-ranked features. Feature importance is a model-based measure of predictive contribution; it does not establish that a feature causes degradation.

## 11. Repository Structure

Recommended layout:

```text
Predictive-Analysis/
└── CA3/
    ├── Aircraft_RUL_Predictive_Analytics_Simplified.ipynb
    ├── README.md
    ├── dataset/
    │   ├── train_FD001.txt
    │   ├── test_FD001.txt
    │   ├── RUL_FD001.txt
    │   ├── train_FD002.txt
    │   ├── test_FD002.txt
    │   ├── RUL_FD002.txt
    │   ├── train_FD003.txt
    │   ├── test_FD003.txt
    │   ├── RUL_FD003.txt
    │   ├── train_FD004.txt
    │   ├── test_FD004.txt
    │   └── RUL_FD004.txt
    └── outputs/
        ├── validation_model_comparison.csv
        ├── test_model_metrics.csv
        ├── test_rul_predictions_all_datasets.csv
        └── random_forest_feature_importance.csv
```

The `outputs` folder is created by the notebook when it runs. Generated CSV files may be committed if you want the repository to include results.

## 12. Requirements

Python 3.10 or later is recommended. Install dependencies:

```bash
pip install numpy pandas matplotlib scikit-learn jupyter
```

## 13. How to Run

1. Clone or download the repository.
2. Ensure the notebook and `dataset` folder are in the expected locations.
3. Install the required packages.
4. Launch Jupyter Notebook or JupyterLab:

   ```bash
   jupyter notebook
   ```

5. Open `Aircraft_RUL_Predictive_Analytics_Simplified.ipynb`.
6. Run all cells from top to bottom.
7. Review the generated tables and charts.
8. Find exported CSV files in the `outputs/` folder.

If the notebook cannot find the dataset, edit `DATA_DIR` in the dataset-location cell.

## 14. Limitations and Responsible Interpretation

- C-MAPSS is a simulated benchmark, not live aircraft telemetry.
- Prediction errors vary across engines and dataset subsets.
- The model output is an estimate in dataset operating cycles, not hours, flights or a guaranteed failure time.
- This academic project is not a certified system for real-world aircraft maintenance or safety decisions.

## 15. Conclusion

This project demonstrates an end-to-end Predictive Analytics / KDD workflow for aircraft-engine RUL prediction. It processes four C-MAPSS datasets, creates training RUL labels, prepares features, compares Linear Regression, Decision Tree and Random Forest models, evaluates predictions with standard regression metrics, and interprets results using prediction errors and feature importance.

The final model estimates remaining operating cycles from the latest available sensor observation of each test engine. The notebook and exported results provide evidence for the project report and individual presentation.

## References

1. NASA Prognostics Center of Excellence, C-MAPSS turbofan engine degradation simulation dataset. Use the dataset source/link supplied with your downloaded data or course materials.
2. Scikit-learn documentation: https://scikit-learn.org/stable/
3. Pandas documentation: https://pandas.pydata.org/docs/
4. Matplotlib documentation: https://matplotlib.org/stable/

---

**Academic note:** Understand the preprocessing, model selection, metrics and interpretation steps before presenting the project. Verify numerical results by running the notebook on your dataset files.
