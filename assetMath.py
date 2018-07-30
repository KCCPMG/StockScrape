import math


def sample_mean(dict_in):
    return sum(dict_in.values())/len(dict_in)


def percentages_table(history):
    # Takes history table [(date, value), (date, value)...]
    # and converts it to percentages table where the value
    # next to a date is the gain (or loss) from the last date
    # so that it outputs [(date, gain), (date, gain)...]
    history.sort(key=lambda tup: tup[0])
    output_table = []
    for i in range(len(history)-1):
        gain = ((history[i+1][1] / history[i][1]) - 1) * 100
        output_table.append((history[i+1][0], gain))
    return output_table


def sample_covariance(asset_dict_a, asset_dict_b):
    # Check to make sure that both assets are using same date range
    a_years = list(asset_dict_a.keys())
    b_years = list(asset_dict_b.keys())
    a_years.sort()
    b_years.sort()

    if len(a_years) != len(b_years):
        print("Different years. Please check data sets.")
        return
    for year in range(len(a_years)):
        if a_years[year] != b_years[year]:
            print("Different years. Please check data sets.")
            return

    a_values = list(asset_dict_a.values())
    b_values = list(asset_dict_b.values())

    mean_a = sample_mean(asset_dict_a)
    mean_b = sample_mean(asset_dict_b)

    output = 0

    for i in range(len(a_values)):
        output += (a_values[i]-mean_a) * (b_values[i]-mean_b) / (len(a_values)-1)

    return output


def sample_standard_deviation(list_in):
    return math.sqrt(sample_variance(list_in))


def population_standard_deviation(list_in):
    return math.sqrt(population_variance(list_in))


def sample_variance(list_in):
    mean = sum(list_in) / len(list_in)
    out = 0
    for num in list_in:
        out += (num - mean) ** 2
    out /= (len(list_in)-1)
    return out


def population_variance(list_in):
    mean = sum(list_in) / len(list_in)
    out = 0
    for num in list_in:
        out += (num - mean) ** 2
    out /= len(list_in)
    return out


def sample_correlation_coefficient(asset_dict_a, asset_dict_b):
    return sample_covariance(asset_dict_a, asset_dict_b) / \
        (sample_standard_deviation(asset_dict_a.values()) *
         sample_standard_deviation(asset_dict_b.values()))

