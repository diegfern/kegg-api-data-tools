# kegg-api-data-tools
Some scripts used for serveral tasks in Enzyme Classification project

# In regard run.sh
This bash script requires a conda environment with python 3.8 named "tf-py38"and 3 projects:
- Downloaded data using KEGG: https://github.com/diegfern/kegg_api_async
- Distance Evaluation, a private project provided by David Medina
- KEGG API Training: https://github.com/diegfern/kegg-api-training
- Bio embeddings data using the codings scripts in : https://github.com/diegfern/KEGG-encoding
- source_code a private project provided by David Medina containing Machine Learning and Deep Learning Models

The folder names I used was the following:
```bash
.
├── PycharmProjects
    ├── kegg-api-data-tools
    ├── kegg-api-training
    ├── bio-embeddings
    ├── distance_evaluation
    ├── source_code
  ```
 Note that bio-embeddings is the previous name for KEGG-encoding repository

# Tools
- Dallago, C., Schütze, K., Heinzinger, M., Olenyi, T., Littmann, M., Lu, A. X., Yang, K. K., Min, S., Yoon, S., Morton, J. T., & Rost, B. (2021). Learned embeddings from deep learning to visualize and predict protein sets. Current Protocols, 1, e113. doi: 10.1002/cpz1.113
- Medina-Ortiz, D., Contreras, S., Amado-Hinojosa, J., Torres-Almonacid, J., Asenjo, J. A., Navarrete, M., & Olivera-Nappa, Á. (2022). Generalized Property-Based Encoders and Digital Signal Processing Facilitate Predictive Tasks in Protein Engineering. Frontiers in Molecular Biosciences, 9. doi: 10.3389/fmolb.2022.898627
