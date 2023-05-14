#!/bin/bash

# TODO add more models
#declare -a models=("bepler" "esm1b" "glove" "fasttext" "plus_rnn" "prottrans_bert_bfd")
declare -a models=("esm1b" "plus_rnn")
declare -a architectures=("A" "B" "C")
#declare -a codification=("" _FFT)
declare -a codification=()
save_model=1
env_name="tf-py38"
#---------PATHS-----------
data_path="./data-filtered/"
sampled_path="../data/"
bio_embeddings_data="../bio-embeddings/kegg-data-encoded/"
distance_evaluation="../distance_evaluation/testing_scripts/"

#---------SCRIPTS---------
balance_script="./scripts/sampling/extract-primary-balanced-data.py"
generate_script="../kegg-api-training/generate-data.py"
split_script="../kegg-api-training/split_data.py"
code_properties_script="../distance_evaluation/testing_scripts/testing_encoders.py"
ml_script="../source_code/training_classic_ml/training_class_models.py"
cnn_script="../source_code/training_cnn/run_cnn_model_protein.py"

#---------DATA-----------
encoders="../distance_evaluation/encoders/clustering_encoders.csv"
base_name="sequences"

#-----COLUMN NAMES-------
seq_col="sequence_aa"
response_col="response"
id_col="sequence_id"

save_model=1
curr_dir=` pwd `
total_data=3866683

mkdir ${sampled_path}
exec &> >(tee ${sampled_path}log.txt)

source ~/miniconda3/etc/profile.d/conda.sh
conda activate ${env_name}

# From 35k to 100k
for samples in {35000..35000..5000};
do
    mkdir -p ${sampled_path}${samples}

    if [[ ! -f "${sampled_path}${samples}/sequences.csv" ]];
    then
        echo "Executing: ${balance_script}"
        python3 ${balance_script} ${data_path} "${sampled_path}${samples}/" ${base_name} ${samples}
    else
        echo "Sampling ${samples} already executed, skiping"
    fi

    for model in ${models[@]}; do
        if [[ ! -f "${sampled_path}${samples}/${model}.csv" ]];
        then
            n_encoded_data=`ls -l ${bio_embeddings_data}${model}*.npz 2>/dev/null | wc -l `
            echo ${n_encoded_data}
            if [[ ${n_encoded_data} -gt 1 ]];
            then
                for i in $( seq 1 $n_encoded_data ); do
                    echo "Executing ${generate_script} ${i}"
                    python3 ${generate_script} "${sampled_path}${samples}/" ${base_name} ${bio_embeddings_data} ${model} "${sampled_path}${samples}/" ${total_data} ${i} ${n_encoded_data}
                done
            else
                echo "Executing: ${generate_script}"
                python3 ${generate_script} "${sampled_path}${samples}/" ${base_name} ${bio_embeddings_data} ${model} "${sampled_path}${samples}/"
            fi
        else
            echo "Data ${model} already generated, skiping"
        fi

        if [[ ! (`ls -l ${sampled_path}${samples}/test/*${model}.csv 2>/dev/null | wc -l ` == 2 && `ls -l ${sampled_path}${samples}/train/*${model}.csv 2>/dev/null | wc -l ` == 2 ) ]];
        then
            echo "Executing: ${split_script}"
            python3 ${split_script} "${sampled_path}${samples}/" ${model} response 30 "${sampled_path}${samples}/"
        else
            echo "Data ${model} already splitted, skipping"
        fi
    done

    #Insertar tilde invertida
    #         .                                                              .
    #if [[ ! (ls -l ${sampled_path}${samples}/Group_*.csv 2>/dev/null | wc -l  == 16 ) ]];
    #then
    #    cd ${distance_evaluation}
    #    parallel -u "python3 testing_encoders.py '${curr_dir}/${sampled_path}${samples}/sequences.csv' Group_{.} ${curr_dir}/${encoders} '${curr_dir}/${sampled_path}${samples}/' ${seq_col} ${response_col} ${id_col}" ::: $( seq 0 7 )
    #    cd ${curr_dir}/
    #else
        #    echo "NLP Data already generated, skipping"
    #fi

    #for i in {0..7}; do
    #             .                                                                                  .         .                                                                                   .
    #    if [[ ! (ls -l ${sampled_path}${samples}/test/*Group_${i}_encoding.csv 2>/dev/null | wc -l  == 2 && ls -l ${sampled_path}${samples}/train/*Group_${i}_encoding.csv 2>/dev/null | wc -l  == 2 ) ]];
    #    then
    #        python3 ${split_script} "${sampled_path}${samples}/" Group_${i}_encoding ${response_col} 30 "${sampled_path}${samples}/"
    #    else
    #        echo "Data Group_${i} already splitted, skipping"
    #    fi
    #done

    mkdir -p ${sampled_path}${samples}/results/ml/
    # Change scale
    for model in ${models[@]}; do
        for i in {0..0}; do
            if [[ ! -f "${sampled_path}${samples}/results/ml/${model}_scale_${i}.csv" ]];
            then
                python3 ${ml_script} "${sampled_path}${samples}/train/X_train_${model}.csv" \
                    "${sampled_path}${samples}/train/y_train_${model}.csv" \
                    "${sampled_path}${samples}/test/X_test_${model}.csv" \
                    "${sampled_path}${samples}/test/y_test_${model}.csv" \
                    ${i} 10 ${save_model} "${sampled_path}${samples}/results/ml/${model}_scale_${i}.csv"
            elsen
                echo "Model ${model} + Scale ${i} for ML Classic already trained, skipping"
            fi
        done
    done
    #for i in {0..7}; do
    #    for j in {0..1}; do
    #        for k in "${codification[@]}"; do
    #            if [[ ! -f "${sampled_path}${samples}/results/ml/group${i}${k}_scale_${j}.csv" ]];
    #            then
    #                python3 ${ml_script} "${sampled_path}${samples}/train/X_train_Group_${i}_encoding${k}.csv" \
    #                    "${sampled_path}${samples}/train/y_train_Group_${i}_encoding${k}.csv" \
    #                    "${sampled_path}${samples}/test/X_test_Group_${i}_encoding${k}.csv" \
    #                    "${sampled_path}${samples}/test/y_test_Group_${i}_encoding${k}.csv" \
    #                    ${j} 10 ${save_model} "${sampled_path}${samples}/results/ml/group${i}${k}_scale_${j}.csv"
    #            else
    #                echo "Group_${i}${k} + scale ${j} for ML Classic already trained, skipping"
    #            fi
    #        done
    #    done
    #done
  
  
    # Only if I want to save disk space
    #|rm ${sampled_path}${samples}/*.csv
  
  
    mkdir -p ${sampled_path}${samples}/results/dl/
  
    for model in ${models[@]}; do
        for architecture in ${architectures[@]}; do
            mkdir -p ${sampled_path}${samples}/results/dl/CNN_${architecture}/
            for i in {0..0}; do
                if [[ ! -f "${sampled_path}${samples}/results/dl/CNN_${architecture}/${model}_scale_${i}.csv" ]];
                then
                    python3 ${cnn_script} "${sampled_path}${samples}/train/X_train_${model}.csv" \
                        "${sampled_path}${samples}/train/y_train_${model}.csv" \
                        "${sampled_path}${samples}/test/X_test_${model}.csv" \
                        "${sampled_path}${samples}/test/y_test_${model}.csv" \
                        ${architecture} "${sampled_path}${samples}/results/dl/CNN_${architecture}/${model}_scale_${i}.json" ${model} ${save_model} ${i}
                else
                    echo "Model ${model} + Scale ${i} for CNN_${architecture} already trained, skipping"
                fi
            done
        done
    done
    #for i in {0..7}; do
    #    for architecture in ${architectures[@]}; do
    #        mkdir -p ${sampled_path}${samples}/results/dl/CNN_${architecture}/
    #        for j in {0..1}; do
    #            for k in "${codification[@]}"; do
    #                if [[ ! -f "${sampled_path}${samples}/results/dl/CNN_${architecture}/group${i}${k}_scale_${j}.csv" ]];
    #                then
    #                    python3 ${cnn_script} "${sampled_path}${samples}/train/X_train_Group_${i}_encoding${k}.csv" \
    #                        "${sampled_path}${samples}/train/y_train_Group_${i}_encoding${k}.csv" \
    #                        "${sampled_path}${samples}/test/X_test_Group_${i}_encoding${k}.csv" \
    #                        "${sampled_path}${samples}/test/y_test_Group_${i}_encoding${k}.csv" \
    #                        ${architecture} "${sampled_path}${samples}/results/dl/CNN_${architecture}/group${i}${k}_scale_${j}.json" Group_${i}${k} ${save_model} ${j}
    #                else
    #                    echo "Group_${i}${k} + scale ${j} for CNN_${architecture} already trained, skipping"
    #                fi
    #            done
    #        done
    #    done
    #done
done
conda deactivate
