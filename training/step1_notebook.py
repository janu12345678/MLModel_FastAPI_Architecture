import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Dynamically resolve project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def train_baseline_model():
    print("[STEP 1] Training Random Forest Classifier for Loan Approval Risk...")

    # Load processed dataset
    data_path = os.path.join(PROJECT_ROOT, "data", "loan_data_processed.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    df = pd.read_csv(data_path)

    # Define features (22 features after engineering)
    features = [
        'Age', 'AnnualIncome', 'CreditScore', 'EmploymentStatus',
        'EducationLevel', 'LoanAmount', 'LoanDuration',
        'MonthlyDebtPayments', 'CreditCardUtilizationRate',
        'DebtToIncomeRatio', 'BankruptcyHistory', 'LoanPurpose',
        'PreviousLoanDefaults', 'PaymentHistory', 'LengthOfCreditHistory',
        'SavingsAccountBalance', 'CheckingAccountBalance',
        'TotalLiabilities', 'JobTenure', 'NetWorth',
        'LoanToIncomeRatio', 'SavingsToLoanRatio'
    ]

    X = df[features]
    y = df['LoanApproved']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train
    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    preds = model.predict(X_test)

    print("\nAccuracy Score:", accuracy_score(y_test, preds))
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    # Feature Importances
    print("\nFeature Importances:")
    importances = model.feature_importances_
    for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True):
        print(f"  {feat:<30} {imp:.4f}")

    # Save model
    model_dir = os.path.join(PROJECT_ROOT, "app")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully at {model_path}")


if __name__ == "__main__":
    train_baseline_model()
