# from medium https://medium.com/@almeidneto/sound-pattern-recognition-with-python-9aff69edce5d


from scipy.io.wavfile import read
def calc_distances(sound_file):
    #The minimun value for the sound to be recognized as a knock
    min_val = 800

    fs, data = read(sound_file)
    data_size = len(data)

    #The number of indexes on 0.15 seconds
    focus_size = int(0.15 * fs)

    focuses = []
    distances = []
    idx = 0

    while idx < len(data):
        if data[idx] > min_val:
            mean_idx = idx + focus_size // 2
            focuses.append(float(mean_idx) / data_size)
            if len(focuses) > 1:
                last_focus = focuses[-2]
                actual_focus = focuses[-1]
                distances.append(actual_focus - last_focus)
            idx += focus_size
        else:
            idx += 1
    return distances
print(calc_distances('test_recording.wav'))
