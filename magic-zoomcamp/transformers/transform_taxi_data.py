if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    #print(f'Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()})
    data.columns = (data.columns
                    .str.replace(' ','_')
                    .str.lower()
                    )
    
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    
    print("Rows with zero passengers:", data['passenger_count'].isin([0]).sum())
    print("Rows with zero distance:", data['trip_distance'].isin([0]).sum())
    # print("Rows where vendor id is blank:", data['vendorid'].isnull().sum())
    # print("Rows where vendor id is 1 or 2:", data['vendorid'].isin([1,2]).sum())
    print("Rows where vendor id is 1, 2, or blank:", (data['vendorid'].isin([1,2]) | data['vendorid'].isnull()).sum())

    return data[(data['passenger_count'] >0) & (data['trip_distance'] >0)]


@test
def test_output(output, *args):
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero distance'
    #assert (output['vendorid'].isin([1,2]) or output['vendorid'].isnull()).sum() == len(data.index), 'There are rides with zero distance'
