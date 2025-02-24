from datetime import timedelta

import pandas as pd

from .data_loader import load_data





def remove_duplicate_vessels(df):
    """Pre-processing to remove duplicate vessel name"""
    for i in range(len(df['Vessel'])):
        if df['Vessel'][i] == 'SAHARE  "MSAH"' or df['Vessel'][i] == 'HR SAHARE "MSAH"' or df['Vessel'][i] == 'HR SAHARE  "MSAH"' or df['Vessel'][i] == ' HR SAHARE  "MSAH"':
            df['Vessel'][i] = 'HR SAHARE "MSAH"'
        elif df['Vessel'][i] == 'SARERA  "MSAR"' or df['Vessel'][i] == 'HR SARERA "MSAR"' or df['Vessel'][i] == 'HR SARERA  "MSAR"'  :
            df['Vessel'][i] ='HR SARERA "MSAR"'
        elif df['Vessel'][i] == 'HR FARHA "MHRF"' or df['Vessel'][i] == 'HR FARHA  "MHRF"' :
            df['Vessel'][i] ='HR FARHA "MHRF"'
        else:
            df['Vessel'][i] = df['Vessel'][i]
    

    return df



def remove_backslashes(vessel_list):
    return [vessel.replace('\\', '') for vessel in vessel_list]


def get_last_info(df, vessel_name) :
    return df[df['Vessel'] == vessel_name].iloc[-1]


def format_timestamp(timestamp):
    # Ensure the input is a pandas Timestamp
    if not isinstance(timestamp, pd.Timestamp):
        raise ValueError("Input must be a pandas Timestamp")
    
    # Format the timestamp
    return timestamp.strftime('%a-%d/%m')



    


def get_voyage_s(last_info):
    


    previous_voyage = last_info['Voyage-S']

    integer_part_str = ''.join([char for char in previous_voyage if char.isdigit()])
    integer_part_int = int(integer_part_str)

    next_voyage = integer_part_int + 1
    number_of_zeros = 4 - len(str(next_voyage))
    return '0' * number_of_zeros + str(next_voyage) + 'S'




def get_voyage_n(last_info):
    


    previous_voyage = last_info['Voyage-N']

    integer_part_str = ''.join([char for char in previous_voyage if char.isdigit()])
    integer_part_int = int(integer_part_str)

    next_voyage = integer_part_int + 1
    number_of_zeros = 4 - len(str(next_voyage))
    return '0' * number_of_zeros + str(next_voyage) + 'N'




def get_eta_cmb(last_info):

    n = 5 # use probabilistic/ml model later
    last_date = last_info['ETD CGP-2']
    return last_date + timedelta(days=n)



def get_etb_cmb(last_info):

    n = 1 # use probabilistic/ml model later
    last_date = get_eta_cmb(last_info)
        
        
        
    return last_date + timedelta(days=n)
    




def get_etd_cmb(last_info):

    n = 1 # use probabilistic/ml model later
    last_date = get_etb_cmb(last_info)
    return last_date + timedelta(days=n)
    


def get_eta_cgp(last_info):

    n = 5 # use probabilistic/ml model later
    last_date = get_etd_cmb(last_info)
    return last_date + timedelta(days=n)


def get_etb_cgp(last_info):

    n = 1 # use probabilistic/ml model later
    last_date = get_eta_cgp(last_info)
    return last_date + timedelta(days=n)
    


def get_etd_cgp(last_info):

    n = 3 # use probabilistic/ml model later
    last_date = get_etb_cgp(last_info)
    return last_date + timedelta(days=n)
    




def generate_samples(df,available_vessels):
        
    samples = []

    for vessel in available_vessels :
        last_info = get_last_info(df = df, vessel_name = vessel)
        print('last_info:',last_info)
        
        new_record = {  'Wk/ ETB CGP' : int(last_info['Wk/ ETB CGP']) + 1,
                        'Service': last_info['Service'],
                        'Vessel' : last_info['Vessel'],
                        'Voyage-S':	get_voyage_s(last_info),
                        'ETA CGP':	format_timestamp(last_info['ETA CGP-2']),
                        'ETB CGP':	format_timestamp(last_info['ETB CGP-2']),
                        'ETD CGP':	format_timestamp(last_info['ETD CGP-2']),
                        'Voyage-N':	get_voyage_n(last_info),
                        'ETA CMB' :	format_timestamp(get_eta_cmb(last_info)),
                        'ETB CMB' :	format_timestamp(get_etb_cmb(last_info)),
                        'ETD CMB' :	format_timestamp(get_etd_cmb(last_info)),
                        'ETA CGP-2' : format_timestamp(get_eta_cgp(last_info)),
                        'ETB CGP-2' : format_timestamp(get_etb_cgp(last_info)),	
                        'ETD CGP-2': format_timestamp(get_etd_cgp(last_info))}
        
        samples.append(new_record)
        


    
    
    return samples


# def main() :
#     df = load_data()
#     df = remove_duplicate_vessels(df)
#     available_vessels = ['HR SAHARE "MSAH"']
#     samples = generate_samples(df,available_vessels)
#     print(samples)



# if __name__ == '__main__':
#     main()


                                
