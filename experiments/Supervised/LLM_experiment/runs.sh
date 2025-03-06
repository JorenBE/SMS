for run in 1 2 3
do
for target in is_successful
do
for representation in synthesis_noSolvPerc
do
for epoch in 200
do
for train_size in 300
do
echo MOF synthesis run $run $target $representation Epoch $epoch Train size $train_size 
python run_experiments_sh.py $train_size $run EleutherAI/gpt-j-6b $epoch $target $representation

done
done
done
done
done