#!/usr/bin/env python
"""
Perform basic cleaning on the data and save  the reults in Weights & Biases
"""
import argparse
import logging
import os

import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading Artifact")
    artifact_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_path)

    logger.info("Dropping Outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Saving the data after cleaning")
    file_name = "clean_sample.csv"
    df.to_csv(file_name, index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    artifact.add_file(file_name)

    logger.info("Logging Artifact")
    run.log_artifact(artifact)

    os.remove(file_name)




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Fully qualified name for the artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name for the W&B artifact that will be created",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the artifact to create",
        required=True
    )
    
    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for the artifact",
        required=True
    )
    
    parser.add_argument(
        "--min_price", 
        type=float,
        help="The minimum price for cleaning outliers",
        required=True
    )
        
    parser.add_argument(
        "--max_price", 
        type=float,
        help="The maximum price for cleaning outliers",
        required=True
    )


    args = parser.parse_args()

    go(args)
