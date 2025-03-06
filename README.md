# MOF Synthesis Dataset

## Overview

The field of metal-organic frameworks (MOFs) is expanding swiftly. Despite prolific work in this area, insight into planning syntheses and the development of predictive tools—similar to those in organic synthesis—remains largely elusive. This project aims to address that gap by providing a carefully curated dataset that supports the development of in silico predictive tools for MOF synthesis.

## Abstract

The field of metal-organic frameworks is expanding swiftly. Despite prolific work, however, insight into planning syntheses and associated predictive tools akin to organic synthesis are still largely lacking. To harness state-of-the-art in in silico tools to surpass the trial-and-error approach in material discovery, pertaining datasets are needed. Multiple larger text-mined datasets are available on MOF solvothermal syntheses. However, data extraction noise, lack of reported negative trials, locally defined ligand name abbreviations, and the lack of matching crystal structures in other databases limit their applicability. In this work, these issues are addressed by manual data curation. We report a dataset of 484 datapoints, consciously crafted to respond to the needs of training machine learning models, which will facilitate the development of predictive tools. Furthermore, it complements text-mined datasets and may allow for validating and enhancing text-mining algorithms.

## Motivation

- **Advancing MOF Research:** By providing high-quality, manually curated data, this dataset is designed to enable the development of predictive tools that can streamline MOF synthesis.
- **Improving In Silico Methods:** With 484 carefully verified datapoints, the dataset serves as a benchmark for training machine learning models, which can improve synthesis planning.
- **Complementing Existing Resources:** The dataset addresses limitations found in larger text-mined datasets, such as data extraction noise and inconsistent naming conventions, offering a reliable resource for both model training and algorithm validation.

## Dataset Description

- **Number of Data Points:** 484
- **Data Quality:** Manually curated to ensure accuracy and consistency.
- **Features:** Detailed records of MOF solvothermal syntheses, including both positive and negative trials.
- **Use Cases:** 
  - Training machine learning models for predictive synthesis.
  - Validating and enhancing text-mining algorithms.
  - Assisting researchers in the rational design of MOF syntheses.

## Getting Started

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/JorenBE/SMS.git
cd SMS
