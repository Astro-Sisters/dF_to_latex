'''
Functions to play with pandas tables and get latex tables

To do:
- Finish documentation
- Generalize to add different columns or rows numbers

@Author: P. Palma-Bifani
'''
import numpy as np
import pandas as pd
import corner
import pickle

def formating_posteriors_values(latex_list_param, samples_directory, quantiles=[0.16, 0.5, 0.84], cifrassignificativas=[1,1,1], evidence=True):
    '''
    Desk
    
    Inputs:
    latex_list_param_name (str) :names of the parameters, just for control for now...
    samples_directory (str) :file name with path in string format
    quantiles                   (=[0.16, 0.5, 0.84])
    cifrassignificativas        (=[1,1,1])
    bayesian_evidence           (=True)

    Outputs:
    latex_params_list a list of strings that can be apppend for a latex table and the bayesian evidence params if wanted

    '''
    ## Open the sample
    with open(samples_directory, 'rb') as f1:
        result  = pickle.load(f1)
        samples = result.samples
        weights = result.weights
        
    ## Calculate quadriles and save param+deviation as string
    latex_params_list = []
    # once per variable
    for l in range(len(latex_list_param)):
        q16, q50, q84 = corner.quantile(samples[:,l], quantiles)
        qsub, qup     = np.abs(q50-q16), np.abs(q84-q50)

        latex_value_1 = round(q50, cifrassignificativas[l])
        latex_value_2 = round(qup, cifrassignificativas[l])
        latex_value_3 = round(qsub, cifrassignificativas[l])
        latex_value = '$' + str(latex_value_1) + '^{+' +  str(latex_value_2) + '}_{-' +str(latex_value_3) +'}$'
        latex_params_list.append(latex_value)
    
    if evidence == True:
            sample_logz = round(result['logz'],1)
            sample_logzerr = round(result['logzerr'],1)
            sample_h = round(result['h'],1)

            logz_value = '{logz} ± {logzerr}'.format(logz=sample_logz, logzerr=sample_logzerr)
            latex_params_list.append(logz_value)

            h_value    = '{h}'.format(h=sample_h )
            latex_params_list.append(h_value)

    return latex_params_list



def latex_pandas_table( latex_list_param, samples_directory,  evidencee=True):
    ''' Here
    '''

    columns_latex = ['Index']
    for i in range(len(latex_list_param)):
        columns_latex.append( latex_list_param[i])
    columns_latex.append('log(z)')
    columns_latex.append('h')
    
    latex_table = pd.DataFrame(columns = columns_latex)


    ## get strings\
    for m in range(len(samples_directory)):

        row_model = str(m)

        latex_posteriors_asym   = formating_posteriors_values(latex_list_param, samples_directory[m], cifrassignificativas=[1,2,2,2], evidence=evidencee)
        
        latex_row = [row_model] + latex_posteriors_asym
        latex_row_good = np.array(latex_row)

        # Append row to the DataFrame using append()
        latex_table2 = latex_table.append(pd.Series(latex_row_good, index=latex_table.columns), ignore_index=True)

    return latex_table2, columns_latex