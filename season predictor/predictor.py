import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV

# get season info
def get_season(season_path):
    season = pd.read_excel(season_path, sheet_name='arabica_ratings_raw')
    columns = season.loc[0]
    season = season.rename(columns=columns)
    # columns = season.columns[2]
    # season = season[columns]
    season = season.loc[1:]
    season['season'] = np.random.randint(1, 13, season.shape[0])
    season = season['season']
    season = season.reset_index()
    season.drop('index', inplace=True, axis=1)
    return season

# get coffee data anc clean
def get_data(data_path):
    data = pd.read_csv(data_path)
    data = data[['quality_score','Processing Method','Aroma','Flavor', 'Aftertaste', 'Acidity',
                'Body', 'Balance', 'Uniformity', 'Clean Cup', 'Sweetness', 'Cupper Points','Total Cup Points','Moisture',
                'Category One Defects', 'Quakers', 'Color', 'Category Two Defects']]
    data['Total Cup Points'] = data['Total Cup Points'].apply(lambda x: float(x.replace('Sample', '')))
    data['Moisture'] = data['Moisture'].apply(lambda x: float(x.replace('%', '')))
    data['Category One Defects'] = data['Category One Defects'].apply(lambda x: float(x.replace('full defects', '')))
    data['Category Two Defects'] = data['Category Two Defects'].apply(lambda x: float(x.replace('full defects', '')))
    data['Quakers'] = data['Quakers'].fillna(0)
    data['Processing Method'] = data['Processing Method'].fillna('Unknown')
    data['Color'] = data['Color'].fillna('Unknown')
    Color = pd.get_dummies(data[['Color']], prefix=['Color'])
    Processing_Method = pd.get_dummies(data[['Processing Method']], prefix=['Processing Method'])
    data = pd.concat([data, Color, Processing_Method], axis=1)
    data = data.drop(columns=['Processing Method', 'Color'])

    return data

def train(data, season):
    # 30% examples in test data
    train, test, train_labels, test_labels = train_test_split(data, season, 
                                                            stratify = season,
                                                            test_size = 0.3, 
                                                            random_state = 42)

    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 20, num = 5)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf,
                'bootstrap': bootstrap}

    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    rf = RandomForestClassifier()
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    # Fit the random search model
    rf_random.fit(train, train_labels)

    def evaluate(model, test_features, test_labels):
        predictions = model.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * np.mean(errors / test_labels)
        accuracy = 100 - mape
        print('Model Performance')
        print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
        print('Accuracy = {:0.2f}%.'.format(accuracy))
        return predictions, accuracy

    random_accuracy = evaluate(rf_random.best_estimator_, test, test_labels['season'])
    rf_random.best_estimator_
    return rf_random.best_estimator_, random_accuracy

def predict(model, test_path):
    test_data = get_data(test_path)
    predictions = model.predict(test_data)
    test_data['predicted_season'] = predictions
    output_path = test_path.split('.')[0] + '-predicted.csv'
    test_data.to_csv(output_path, index=False)

    return predictions

if __name__ == "__main__":
    season_path = 'data.xlsx'
    season = get_season(season_path)

    data_path = 'arabica_ratings_raw.csv'
    data = get_data(data_path)

    best_random, random_accuracy = train(data=data, season=season)

    test_path = 'test.csv'
    predict(best_random, test_path)
    