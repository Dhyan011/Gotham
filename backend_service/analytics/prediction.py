from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import numpy as np

def forecast_spatial_crimes(X_train, y_train, X_test):
    """
    Random Forest spatial forecast.
    X_train: [[lat, lng, month, day_of_week], ...]
    """
    if not X_train or not y_train:
        return []
        
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    return clf.predict_proba(X_test)

def predict_repeat_offense(X_train, y_train, X_test):
    """
    Repeat offense GBT classifier.
    X_train: [[prior_offenses, severity_avg, avg_days_between_crimes], ...]
    """
    if not X_train or not y_train:
        return []
        
    clf = GradientBoostingClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    probs = clf.predict_proba(X_test)
    return [p[1] for p in probs] # Probability of positive class

if __name__ == "__main__":
    pass
