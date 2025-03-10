import os
import time

import fire
import numpy as np
import pandas as pd
import wandb
from fastcore.xtras import save_pickle
from gptjchem.peftclassifier import PEFTClassifier
from gptchem.evaluator import evaluate_classification
from pycm import ConfusionMatrix
from sklearn.model_selection import train_test_split

def create_string_without_solventPerc(df):
    q = "a MOF made out of {ligand} and {metal} in {solvents} for {time} hours at {temperature} degrees Celcius (inorganic salt {salt}, additives {additives})"
    all = []
    for i, entry in df.iterrows():
        string = q.format(
            ligand= entry['ligand'],
            metal = entry['metal'],
            solvents = entry['solvents_noPerc'],
            temperature = entry['T'],
            time = entry['time'],
            salt = entry['inorganic_salt'],
            additives = entry['additional']
            )
        all.append(string)
    df['synthesis_noSolvPerc'] = all
    return df

def create_string_solvents(df):
    all_solvent_strings= []
    for _, entry in df.iterrows():
        solvent_string = []
        for i in range(1, 4):
            sol = f'solvent{i}'
            #perc = f'vv_solvent{i}'
            if not isinstance(entry[sol], float):
                solvent = f'{entry[sol]}'
                solvent_string.append(solvent)
    
        solvent_string = ' and '.join(solvent_string)
        all_solvent_strings.append(solvent_string)

    df['solvents_noPerc'] = all_solvent_strings
    return df


DATA_FILE = '../experiments/Supervised/20240402_syntheses_UTF8.csv'

MAX_TEST_DATA = 50

def train_test(train_size: int = 300, random_state: int = 42, model = 'EleutherAI/gpt-j-6b', num_epochs = 30, target = 'is_successful', representation = 'synthesis' ):
    if not os.path.exists("out"):
        os.makedirs("out")
    if not os.path.exists("predictions"):
        os.makedirs("predictions")

    df = pd.read_csv(DATA_FILE)

    create_string_solvents(df)
    create_string_without_solventPerc(df)

    data_summary = {
        'datafile':DATA_FILE,
        'target':target,
        'representation' : representation
    }

    config = {
        "property_name": "success of synthesis",
        "tune_settings": {"num_train_epochs": num_epochs, "learning_rate": 3e-4},
        "tokenizer_kwargs": {"cutoff_len": 128},
        "base_model": model,
        "batch_size": 4,
        "inference_batch_size": 2,
    }


    wandb.init(
        # set the wandb project where this run will be logged
        project="gpt-challenge-classif-solvents",
        # track hyperparameters and run metadata
        config={
            "model": model,
            "target": target,
            **config,
            "train_size": train_size,
            "num_epochs": num_epochs,
        },
        tags=["classification", "solvents", model],
    )


    df = df.dropna(subset=[representation, target])
    
    df_train, df_test = train_test_split(
        df,
        train_size=train_size,
        test_size= min(len(df)-train_size, MAX_TEST_DATA),
        random_state=random_state,
        stratify=df[target].astype(int).values,
    )

    print(len(df_train), len(df_test))

    classifier = PEFTClassifier(
        **config,
    )

    classifier.fit(df_train[representation], df_train[target])

    predictions =[]
    for i in range(0, len(df_test[representation]), 15):
        preds = classifier._predict(df_test[representation].iloc[i:i+15])
        preds = np.array(preds[0]).astype(int)
        predictions.extend(preds)
    print(f"predictions {predictions}")

    df_test['prediction'] = predictions
    df_test['partition'] = 'test'
    df_test = df_test[[representation, target, 'partition', 'prediction']]


    df_train['prediction'] = [999] * len(df_train)
    df_train['partition'] = 'train'
    df_train = df_train[[representation, target, 'partition', 'prediction']]
    df_all = pd.concat([df_train, df_test])
    df_all.to_csv(os.path.join('predictions', f'predictions_seed{random_state}_{target}_{representation}_{num_epochs}epoch.csv'))

    #predictions = classifier._predict(df_test[representation])

    predictions = np.array(predictions)

    #predictions = np.array(predictions[0])

    nan_prediction_mask = np.isnan(predictions)
    num_nan_predictions = nan_prediction_mask.sum()

    true = df_test[target][~nan_prediction_mask].astype(int).values

    results = evaluate_classification(true, predictions[~nan_prediction_mask])
    results_w_float_values = {k: v for k, v in results.items() if isinstance(v, float)}
    print(f"results: {results}")

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    wandb.log(results_w_float_values)
    wandb.log({f"num_nan_predictions": num_nan_predictions})

    save_pickle(
        os.path.join("out", f"{timestamp}_{train_size}_{num_epochs}_predictions.pkl"),
        {"results":results, "predictions": predictions, "true": true, "train_size": train_size, "config": config, 'data_summary':data_summary,},
    )

if __name__ == "__main__":
    fire.Fire(train_test)
